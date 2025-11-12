"""
Views para registro de produtos usados em agendamentos
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from agendamentos.models import Agendamento
from core.models import Product
from django.db import transaction
import json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_appointment_products(request, pk):
    """
    Registra produtos usados em um agendamento
    POST /api/appointments/<id>/register-products/
    
    Body: {
        "products": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ]
    }
    
    Atualiza automaticamente o estoque
    """
    try:
        # Buscar agendamento
        appointment = Agendamento.objects.get(pk=pk)
        
        # Verificar permissão
        if not (request.user.is_staff or 
                request.user.role in ['admin', 'owner', 'barber']):
            return Response({
                'error': 'Você não tem permissão para registrar produtos'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Validar dados
        products_data = request.data.get('products', [])
        
        if not products_data or not isinstance(products_data, list):
            return Response({
                'error': 'Lista de produtos inválida'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(products_data) == 0:
            return Response({
                'success': True,
                'message': 'Nenhum produto selecionado'
            })
        
        # Processar em transação
        with transaction.atomic():
            products_used = []
            
            for item in products_data:
                product_id = item.get('product_id')
                quantity = item.get('quantity', 1)
                
                if not product_id or quantity < 1:
                    continue
                
                try:
                    product = Product.objects.select_for_update().get(pk=product_id)
                    
                    # Validar estoque (usando stock_quantity)
                    if product.stock_quantity < quantity:
                        return Response({
                            'error': f'Estoque insuficiente para {product.name}. Disponível: {product.stock_quantity}'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Atualizar quantidade do produto
                    product.stock_quantity -= quantity
                    product.save()
                    
                    products_used.append({
                        'product': product.name,
                        'quantity': quantity,
                        'product_id': product.id
                    })
                    
                except Product.DoesNotExist:
                    return Response({
                        'error': f'Produto {product_id} não encontrado'
                    }, status=status.HTTP_404_NOT_FOUND)
            
            # Salvar produtos usados no campo notes do agendamento (temporário)
            if hasattr(appointment, 'notes'):
                current_notes = appointment.notes or ''
                products_info = f"\n\nProdutos usados: {json.dumps(products_used, ensure_ascii=False)}"
                appointment.notes = current_notes + products_info
                appointment.save()
            
            return Response({
                'success': True,
                'message': f'{len(products_used)} produtos registrados com sucesso',
                'products': products_used
            }, status=status.HTTP_200_OK)
        
    except Agendamento.DoesNotExist:
        return Response({
            'error': 'Agendamento não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Erro ao registrar produtos: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_appointment_products(request, pk):
    """
    Lista produtos usados em um agendamento
    GET /api/appointments/<id>/products/
    """
    try:
        appointment = Agendamento.objects.get(pk=pk)
        
        # Tentar extrair produtos do campo notes
        products = []
        if hasattr(appointment, 'notes') and appointment.notes:
            try:
                # Buscar produtos usados nas notes
                if 'Produtos usados:' in appointment.notes:
                    products_json = appointment.notes.split('Produtos usados:')[-1].strip()
                    products = json.loads(products_json)
            except (json.JSONDecodeError, IndexError):
                pass
        
        return Response({
            'appointment_id': pk,
            'products': products,
            'total': len(products)
        })
        
    except Agendamento.DoesNotExist:
        return Response({
            'error': 'Agendamento não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

