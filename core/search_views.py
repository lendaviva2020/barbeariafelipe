"""
Views de busca global
Busca em tempo real em agendamentos, clientes, serviços e produtos
"""
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from agendamentos.models import Agendamento
from users.models import User
from servicos.models import Servico
from core.models import Product
from django.urls import reverse


class GlobalSearchView(APIView):
    """
    Busca global no sistema
    GET /api/search/?q=<query>
    
    Retorna resultados categorizados por tipo:
    - agendamentos
    - clientes
    - serviços
    - produtos
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return Response({
                'results': [],
                'message': 'Digite pelo menos 2 caracteres para buscar'
            })
        
        # Limitar tamanho da query para segurança
        query = query[:100]
        
        results = []
        
        # Buscar agendamentos
        appointments = Agendamento.objects.filter(
            Q(customer_name__icontains=query) |
            Q(customer_phone__icontains=query) |
            Q(customer_email__icontains=query)
        ).select_related('servico', 'barbeiro').order_by('-appointment_date')[:5]
        
        for apt in appointments:
            results.append({
                'type': 'appointment',
                'id': str(apt.id),
                'title': apt.customer_name,
                'subtitle': f"{apt.servico.name if apt.servico else 'Serviço'} - {apt.appointment_date.strftime('%d/%m/%Y')} {apt.appointment_time}",
                'icon': 'calendar',
                'url': reverse('admin_painel:appointments')
            })
        
        # Buscar clientes (usuários)
        if request.user.is_staff or request.user.role in ['admin', 'owner']:
            clients = User.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            ).order_by('-created_at')[:5]
            
            for client in clients:
                results.append({
                    'type': 'client',
                    'id': str(client.id),
                    'title': client.name,
                    'subtitle': client.email or client.phone or '',
                    'icon': 'user',
                    'url': reverse('admin_painel:users')
                })
        
        # Buscar serviços
        services = Servico.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).order_by('name')[:5]
        
        for service in services:
            results.append({
                'type': 'service',
                'id': str(service.id),
                'title': service.name,
                'subtitle': f"R$ {service.price} - {service.duration} min",
                'icon': 'scissors',
                'url': reverse('servicos:list')
            })
        
        # Buscar produtos (se admin)
        if request.user.is_staff or request.user.role in ['admin', 'owner']:
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).order_by('name')[:5]
            
            for product in products:
                results.append({
                    'type': 'product',
                    'id': str(product.id),
                    'title': product.name,
                    'subtitle': f"R$ {product.price} - Estoque: {product.quantity}",
                    'icon': 'package',
                    'url': reverse('core:inventory')
                })
        
        return Response({
            'results': results,
            'total': len(results),
            'query': query
        })

