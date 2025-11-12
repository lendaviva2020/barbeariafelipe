from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from core.decorators import admin_required, admin_required_api
from agendamentos.models import Agendamento
from barbeiros.models import Barbeiro
from servicos.models import Servico
from cupons.models import Cupom
from users.models import User
from core.models import AuditLog


@admin_required
def dashboard_view(request):
    """Página principal do dashboard"""
    return render(request, 'admin/dashboard.html')


@admin_required_api
def dashboard_stats_api(request):
    """API: Estatísticas gerais do dashboard"""
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    # Parse dates
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = (timezone.now() - timedelta(days=30)).date()
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
    
    # Query appointments
    appointments = Agendamento.objects.filter(
        appointment_date__range=[start_date, end_date]
    )
    
    completed = appointments.filter(status='completed')
    
    # Calculate stats
    total_revenue = completed.aggregate(Sum('price'))['price__sum'] or 0
    completed_count = completed.count()
    
    stats = {
        'total_appointments': appointments.count(),
        'completed_appointments': completed_count,
        'pending_appointments': appointments.filter(status='pending').count(),
        'confirmed_appointments': appointments.filter(status='confirmed').count(),
        'cancelled_appointments': appointments.filter(status='cancelled').count(),
        'total_revenue': float(total_revenue),
        'average_ticket': float(completed.aggregate(Avg('price'))['price__avg'] or 0),
        'active_barbers': Barbeiro.objects.filter(active=True).count(),
        'active_services': Servico.objects.filter(active=True).count(),
        'total_users': User.objects.filter(is_active=True).count(),
    }
    
    # Today's appointments
    today = timezone.now().date()
    today_appointments = Agendamento.objects.filter(appointment_date=today)
    
    stats['today'] = {
        'total': today_appointments.count(),
        'completed': today_appointments.filter(status='completed').count(),
        'pending': today_appointments.filter(status='pending').count(),
        'cancelled': today_appointments.filter(status='cancelled').count(),
    }
    
    return JsonResponse(stats)


@admin_required_api
def dashboard_revenue_chart_api(request):
    """API: Dados para gráfico de faturamento"""
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = (timezone.now() - timedelta(days=30)).date()
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
    
    # Get daily revenue
    revenue_data = []
    current_date = start_date
    
    while current_date <= end_date:
        day_appointments = Agendamento.objects.filter(
            appointment_date=current_date,
            status='completed'
        )
        
        revenue = day_appointments.aggregate(Sum('price'))['price__sum'] or 0
        appointments_count = day_appointments.count()
        
        revenue_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'revenue': float(revenue),
            'appointments': appointments_count,
            'average': float(revenue / appointments_count) if appointments_count > 0 else 0,
        })
        
        current_date += timedelta(days=1)
    
    return JsonResponse({'data': revenue_data})


@admin_required_api
def dashboard_services_chart_api(request):
    """API: Dados dos serviços mais populares"""
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = (timezone.now() - timedelta(days=30)).date()
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
    
    # Get service statistics
    services_data = []
    services = Servico.objects.filter(active=True)
    
    for service in services:
        service_appointments = Agendamento.objects.filter(
            service=service,
            appointment_date__range=[start_date, end_date]
        )
        
        completed = service_appointments.filter(status='completed')
        revenue = completed.aggregate(Sum('price'))['price__sum'] or 0
        
        services_data.append({
            'id': service.id,
            'name': service.name,
            'count': service_appointments.count(),
            'completed': completed.count(),
            'revenue': float(revenue),
            'price': float(service.price),
        })
    
    # Sort by revenue
    services_data.sort(key=lambda x: x['revenue'], reverse=True)
    
    return JsonResponse({'data': services_data[:10]})  # Top 10


@admin_required_api
def dashboard_barber_performance_api(request):
    """API: Performance dos barbeiros"""
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = (timezone.now() - timedelta(days=30)).date()
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
    
    # Get barber performance
    barbers_data = []
    barbers = Barbeiro.objects.filter(active=True)
    
    for barber in barbers:
        barber_appointments = Agendamento.objects.filter(
            barber=barber,
            appointment_date__range=[start_date, end_date]
        )
        
        completed = barber_appointments.filter(status='completed')
        revenue = completed.aggregate(Sum('price'))['price__sum'] or 0
        total_count = barber_appointments.count()
        completed_count = completed.count()
        
        efficiency = (completed_count / total_count * 100) if total_count > 0 else 0
        
        barbers_data.append({
            'id': barber.id,
            'name': barber.name,
            'appointments': total_count,
            'completed': completed_count,
            'revenue': float(revenue),
            'efficiency': round(efficiency, 1),
        })
    
    # Sort by revenue
    barbers_data.sort(key=lambda x: x['revenue'], reverse=True)
    
    return JsonResponse({'data': barbers_data})


@admin_required_api
def dashboard_status_distribution_api(request):
    """API: Distribuição de status dos agendamentos"""
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = (timezone.now() - timedelta(days=30)).date()
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
    
    appointments = Agendamento.objects.filter(
        appointment_date__range=[start_date, end_date]
    )
    
    status_data = [
        {
            'name': 'Completados',
            'value': appointments.filter(status='completed').count(),
            'color': '#10b981'
        },
        {
            'name': 'Confirmados',
            'value': appointments.filter(status='confirmed').count(),
            'color': '#3b82f6'
        },
        {
            'name': 'Pendentes',
            'value': appointments.filter(status='pending').count(),
            'color': '#f59e0b'
        },
        {
            'name': 'Cancelados',
            'value': appointments.filter(status='cancelled').count(),
            'color': '#ef4444'
        },
    ]
    
    # Filter out zero values
    status_data = [item for item in status_data if item['value'] > 0]
    
    return JsonResponse({'data': status_data})

