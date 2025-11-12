from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from core.decorators import admin_required, admin_required_api
from agendamentos.models import Agendamento
from core.models import AuditLog
from datetime import datetime, date


@admin_required
def appointments_view(request):
    """Página de gerenciamento de agendamentos"""
    return render(request, 'admin/appointments.html')


@admin_required_api
def appointments_api(request):
    """API: Lista de agendamentos com filtros"""
    # Filtros
    status_filter = request.GET.get('status', 'all')
    tab = request.GET.get('tab', 'all')
    search = request.GET.get('search', '')
    
    # Query base
    appointments = Agendamento.objects.all().select_related('service', 'barber')
    
    # Filtro por tab
    today = date.today()
    if tab == 'today':
        appointments = appointments.filter(appointment_date=today)
    elif tab == 'upcoming':
        appointments = appointments.filter(appointment_date__gt=today)
    elif tab == 'past':
        appointments = appointments.filter(appointment_date__lt=today)
    
    # Filtro por status
    if status_filter != 'all':
        appointments = appointments.filter(status=status_filter)
    
    # Busca
    if search:
        appointments = appointments.filter(
            Q(customer_name__icontains=search) |
            Q(customer_phone__icontains=search) |
            Q(customer_email__icontains=search)
        )
    
    # Ordenar
    appointments = appointments.order_by('-appointment_date', '-appointment_time')
    
    # Limitar resultados
    appointments = appointments[:100]
    
    # Serializar
    data = []
    for apt in appointments:
        data.append({
            'id': apt.id,
            'customer_name': apt.customer_name,
            'customer_phone': apt.customer_phone or '',
            'customer_email': apt.customer_email or '',
            'appointment_date': apt.appointment_date.strftime('%Y-%m-%d'),
            'appointment_time': apt.appointment_time.strftime('%H:%M'),
            'status': apt.status,
            'service': apt.service.name,
            'barber': apt.barber.name,
            'price': float(apt.price) if apt.price else 0,
        })
    
    return JsonResponse({'appointments': data})


@admin_required_api
@require_http_methods(["POST"])
def confirm_appointment_api(request, pk):
    """API: Confirmar agendamento"""
    try:
        apt = Agendamento.objects.get(pk=pk)
        old_status = apt.status
        
        apt.status = 'confirmed'
        apt.save()
        
        # Log de auditoria
        AuditLog.log(
            user=request.user,
            action='UPDATE',
            table_name='agendamentos',
            record_id=pk,
            old_data={'status': old_status},
            new_data={'status': 'confirmed'},
            request=request
        )
        
        return JsonResponse({'success': True, 'message': 'Agendamento confirmado'})
    except Agendamento.DoesNotExist:
        return JsonResponse({'error': 'Agendamento não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@admin_required_api
@require_http_methods(["POST"])
def complete_appointment_api(request, pk):
    """API: Completar agendamento"""
    try:
        apt = Agendamento.objects.get(pk=pk)
        old_status = apt.status
        
        apt.status = 'completed'
        apt.completed_at = datetime.now()
        apt.save()
        
        # Log de auditoria
        AuditLog.log(
            user=request.user,
            action='UPDATE',
            table_name='agendamentos',
            record_id=pk,
            old_data={'status': old_status},
            new_data={'status': 'completed', 'completed_at': apt.completed_at.isoformat()},
            request=request
        )
        
        return JsonResponse({'success': True, 'message': 'Agendamento concluído'})
    except Agendamento.DoesNotExist:
        return JsonResponse({'error': 'Agendamento não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@admin_required_api
@require_http_methods(["POST"])
def cancel_appointment_api(request, pk):
    """API: Cancelar agendamento"""
    try:
        apt = Agendamento.objects.get(pk=pk)
        old_status = apt.status
        
        apt.status = 'cancelled'
        apt.save()
        
        # Log de auditoria
        AuditLog.log(
            user=request.user,
            action='UPDATE',
            table_name='agendamentos',
            record_id=pk,
            old_data={'status': old_status},
            new_data={'status': 'cancelled'},
            request=request
        )
        
        return JsonResponse({'success': True, 'message': 'Agendamento cancelado'})
    except Agendamento.DoesNotExist:
        return JsonResponse({'error': 'Agendamento não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

