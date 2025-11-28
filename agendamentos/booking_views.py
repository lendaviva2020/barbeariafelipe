"""
Views específicas para o sistema de agendamento (booking)
Compatíveis com o JavaScript fornecido
"""
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.db import models

from servicos.models import Servico
from barbeiros.models import Barbeiro
from cupons.models import Cupom
from .models import Agendamento


@api_view(['GET'])
@permission_classes([AllowAny])
def services_list(request):
    """Lista todos os serviços ativos"""
    try:
        # Filtrar serviços ativos
        # A tabela services do Supabase pode ter active ou is_active
        services = Servico.objects.all()
        
        # Filtrar apenas ativos
        active_services = []
        for s in services:
            # Verificar se está ativo (pode ter active=True ou is_active=True)
            is_active = getattr(s, 'active', None) or getattr(s, 'is_active', None)
            if is_active is not False:  # Se não for explicitamente False, considerar ativo
                active_services.append(s)
        
        data = [{
            'id': str(s.id),  # UUID precisa ser string
            'name': s.name or 'Serviço',
            'description': s.description or '',
            'duration': s.duration or 30,
            'price': str(float(s.price)) if s.price else '0.00'
        } for s in active_services]
        
        return Response(data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def barbers_list(request):
    """Lista todos os barbeiros ativos"""
    try:
        # Usar values() para evitar problemas com campos JSON
        barbers = Barbeiro.objects.filter(active=True).order_by('name').values('id', 'name', 'specialty', 'photo_url')
        
        data = [{
            'id': str(b['id']),  # UUID precisa ser string
            'name': b['name'],
            'specialty': b['specialty'] or 'Barbeiro profissional',
            'photo': b.get('photo_url') or None  # URL da foto do barbeiro
        } for b in barbers]
        
        return Response(data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def available_slots(request):
    """Retorna horários disponíveis para uma data"""
    date = request.GET.get('date')
    service_id = request.GET.get('service_id')
    barber_id = request.GET.get('barber_id')
    
    if not date or not service_id:
        return Response(
            {'error': 'Missing parameters: date and service_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        service = Servico.objects.get(id=service_id, active=True)
    except Servico.DoesNotExist:
        return Response(
            {'error': 'Service not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Horários de funcionamento (9h às 19h)
    all_slots = []
    start_hour = 9
    end_hour = 19
    
    for hour in range(start_hour, end_hour + 1):
        all_slots.append(f"{hour:02d}:00")
        if hour < end_hour:
            all_slots.append(f"{hour:02d}:30")
    
    # Buscar agendamentos existentes
    query = Q(
        appointment_date=date,
        status__in=['pending', 'confirmed']
    )
    
    if barber_id:
        # Se especificou barbeiro, buscar apenas agendamentos dele
        query &= Q(barber_id=barber_id)
        occupied_bookings = Agendamento.objects.filter(query).values_list('appointment_time', flat=True)
        occupied_times = {t.strftime('%H:%M') for t in occupied_bookings}
        
        # Filtrar horários disponíveis e marcar os ocupados
        available = []
        for slot in all_slots:
            is_available = slot not in occupied_times
            available.append({
                'time': slot,
                'available': is_available
            })
    else:
        # Se não especificou barbeiro, verificar disponibilidade geral
        # Contar quantos barbeiros ativos existem
        total_barbers = Barbeiro.objects.filter(active=True).count()
        
        # Buscar todos os agendamentos para esta data
        all_bookings = Agendamento.objects.filter(
            appointment_date=date,
            status__in=['pending', 'confirmed']
        ).values_list('appointment_time', flat=True)
        
        # Contar quantos agendamentos existem por horário
        from collections import Counter
        time_counts = Counter(t.strftime('%H:%M') for t in all_bookings)
        
        # Filtrar horários disponíveis
        available = []
        for slot in all_slots:
            # Um horário está disponível se há menos agendamentos que barbeiros
            bookings_count = time_counts.get(slot, 0)
            is_available = bookings_count < total_barbers
            available.append({
                'time': slot,
                'available': is_available
            })
    
    return Response(available)


@api_view(['POST'])
@permission_classes([AllowAny])
def validate_coupon(request):
    """Valida um cupom de desconto"""
    code = request.data.get('code', '').strip().upper()
    
    if not code:
        return Response({
            'valid': False,
            'message': 'Código de cupom é obrigatório'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        coupon = Cupom.objects.get(code=code, active=True)
        
        # Verificar expiração
        if coupon.expiry_date and coupon.expiry_date < timezone.now().date():
            return Response({
                'valid': False,
                'message': 'Cupom expirado'
            })
        
        # Verificar limite de usos
        if coupon.max_uses > 0 and coupon.current_uses >= coupon.max_uses:
            return Response({
                'valid': False,
                'message': 'Cupom esgotado'
            })
        
        return Response({
            'valid': True,
            'coupon': {
                'code': coupon.code,
                'discount': float(coupon.discount),
                'discount_type': coupon.discount_type
            }
        })
        
    except Cupom.DoesNotExist:
        return Response({
            'valid': False,
            'message': 'Cupom inválido'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Exigir autenticação obrigatória
def create_booking(request):
    """Cria um novo agendamento - REQUER AUTENTICAÇÃO"""
    try:
        # Validar dados obrigatórios
        service_id = request.data.get('service_id')
        date = request.data.get('date')
        time = request.data.get('time')
        customer_name = request.data.get('customer_name')
        customer_phone = request.data.get('customer_phone')
        
        if not all([service_id, date, time, customer_name, customer_phone]):
            return Response({
                'success': False,
                'message': 'Dados obrigatórios faltando'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar serviço
        try:
            service = Servico.objects.get(id=service_id, active=True)
        except Servico.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Serviço não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Buscar barbeiro (opcional)
        barber = None
        barber_id = request.data.get('barber_id')
        if barber_id:
            try:
                barber = Barbeiro.objects.get(id=barber_id, active=True)
            except Barbeiro.DoesNotExist:
                pass
        
        # Verificar disponibilidade
        # Se não especificou barbeiro, verificar se há algum barbeiro disponível
        if not barber:
            # Contar quantos barbeiros ativos existem
            total_barbers = Barbeiro.objects.filter(active=True).count()
            
            # Contar quantos agendamentos já existem neste horário
            existing_count = Agendamento.objects.filter(
                appointment_date=date,
                appointment_time=time,
                status__in=['pending', 'confirmed']
            ).count()
            
            # Se todos os barbeiros estão ocupados, não há disponibilidade
            if existing_count >= total_barbers:
                return Response({
                    'success': False,
                    'message': 'Horário não disponível. Todos os barbeiros estão ocupados.'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Se especificou barbeiro, verificar se ele está disponível
            existing = Agendamento.objects.filter(
                appointment_date=date,
                appointment_time=time,
                barber=barber,
                status__in=['pending', 'confirmed']
            )
            
            if existing.exists():
                return Response({
                    'success': False,
                    'message': 'Horário não disponível para este barbeiro'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calcular preço e desconto
        price = service.price
        coupon = None
        coupon_code = request.data.get('coupon_code')
        
        if coupon_code:
            try:
                coupon = Cupom.objects.get(code=coupon_code.upper(), active=True)
                
                # Verificar validade
                if coupon.expiry_date and coupon.expiry_date < timezone.now().date():
                    coupon = None
                elif coupon.max_uses > 0 and coupon.current_uses >= coupon.max_uses:
                    coupon = None
                else:
                    # Atualizar uso do cupom
                    coupon.current_uses += 1
                    coupon.save()
            except Cupom.DoesNotExist:
                pass
        
        # Criar agendamento
        # REQUER AUTENTICAÇÃO - usar sempre o usuário autenticado
        booking_data = {
            'service': service,
            'barber': barber,
            'appointment_date': date,
            'appointment_time': time,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': request.data.get('customer_email') or request.user.email or '',
            'notes': request.data.get('notes') or '',
            'price': price,
            'coupon_code': coupon_code or '',
            'status': 'pending',
            'user_id': request.user.id  # Sempre usar o usuário autenticado
        }
        
        booking = Agendamento.objects.create(**booking_data)
        
        return Response({
            'success': True,
            'booking_id': booking.id,
            'message': 'Agendamento confirmado com sucesso'
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

