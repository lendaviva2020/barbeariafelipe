from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from core.decorators import admin_required, admin_required_api
from core.models import WaitingList, AuditLog
from core.whatsapp import send_whatsapp_message
from datetime import date


@admin_required
def waiting_list_view(request):
    """Página de lista de espera"""
    return render(request, 'admin/waiting_list.html')


@admin_required_api
def waiting_list_api(request):
    """API: Lista de espera com filtros"""
    # Filtros
    status_filter = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    barber_filter = request.GET.get('barber')
    service_filter = request.GET.get('service')
    
    # Query base
    entries = WaitingList.objects.all().select_related('service', 'barber')
    
    # Filtros
    if status_filter != 'all':
        entries = entries.filter(status=status_filter)
    
    if barber_filter:
        entries = entries.filter(barber_id=barber_filter)
    
    if service_filter:
        entries = entries.filter(service_id=service_filter)
    
    if search:
        entries = entries.filter(
            Q(customer_name__icontains=search) |
            Q(customer_phone__icontains=search) |
            Q(service__name__icontains=search)
        )
    
    # Ordenar
    entries = entries.order_by('-created_at')
    
    # Limitar
    entries = entries[:100]
    
    # Serializar
    data = []
    for entry in entries:
        data.append({
            'id': entry.id,
            'customer_name': entry.customer_name,
            'customer_phone': entry.customer_phone,
            'customer_email': entry.customer_email or '',
            'service_name': entry.service.name,
            'service_price': float(entry.service.price),
            'service_duration': entry.service.duration,
            'barber_name': entry.barber.name if entry.barber else 'Qualquer barbeiro',
            'preferred_date': entry.preferred_date.strftime('%Y-%m-%d'),
            'preferred_time_start': entry.preferred_time_start.strftime('%H:%M') if entry.preferred_time_start else None,
            'preferred_time_end': entry.preferred_time_end.strftime('%H:%M') if entry.preferred_time_end else None,
            'notes': entry.notes,
            'status': entry.status,
            'created_at': entry.created_at.isoformat(),
            'notified_at': entry.notified_at.isoformat() if entry.notified_at else None,
        })
    
    return JsonResponse({'entries': data})


@admin_required_api
@require_http_methods(["POST"])
def notify_customer_api(request, pk):
    """API: Notificar cliente via WhatsApp"""
    try:
        entry = WaitingList.objects.select_related('service', 'barber').get(pk=pk)
        
        # Montar mensagem
        message = f"""Olá {entry.customer_name}! 👋

Temos uma boa notícia! 😊

Estamos com disponibilidade para o serviço de *{entry.service.name}* no dia *{entry.preferred_date.strftime('%d/%m/%Y')}*.

💰 Valor: R$ {entry.service.price:.2f}
⏱️ Duração: {entry.service.duration} minutos

Por favor, entre em contato conosco para confirmar seu agendamento!

Atenciosamente,
Barbearia Francisco"""
        
        # Enviar WhatsApp
        send_whatsapp_message(entry.customer_phone, message)
        
        # Atualizar status
        entry.status = 'notified'
        entry.notified_at = timezone.now()
        entry.save()
        
        # Log
        AuditLog.log(
            user=request.user,
            action='UPDATE',
            table_name='waiting_list',
            record_id=pk,
            old_data={'status': 'waiting'},
            new_data={'status': 'notified', 'notified_at': entry.notified_at.isoformat()},
            request=request
        )
        
        return JsonResponse({'success': True, 'message': 'Cliente notificado via WhatsApp'})
    except WaitingList.DoesNotExist:
        return JsonResponse({'error': 'Entrada não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@admin_required_api
@require_http_methods(["POST"])
def update_status_api(request, pk):
    """API: Atualizar status da entrada"""
    import json
    try:
        entry = WaitingList.objects.get(pk=pk)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status not in dict(WaitingList.STATUS_CHOICES):
            return JsonResponse({'error': 'Status inválido'}, status=400)
        
        old_status = entry.status
        entry.status = new_status
        entry.save()
        
        # Log
        AuditLog.log(
            user=request.user,
            action='UPDATE',
            table_name='waiting_list',
            record_id=pk,
            old_data={'status': old_status},
            new_data={'status': new_status},
            request=request
        )
        
        return JsonResponse({'success': True})
    except WaitingList.DoesNotExist:
        return JsonResponse({'error': 'Entrada não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@admin_required_api
@require_http_methods(["DELETE"])
def remove_entry_api(request, pk):
    """API: Remover entrada da lista"""
    try:
        entry = WaitingList.objects.get(pk=pk)
        
        # Log antes de deletar
        AuditLog.log(
            user=request.user,
            action='DELETE',
            table_name='waiting_list',
            record_id=pk,
            old_data={
                'customer_name': entry.customer_name,
                'customer_phone': entry.customer_phone,
                'service': entry.service.name,
                'preferred_date': entry.preferred_date.strftime('%Y-%m-%d')
            },
            request=request
        )
        
        entry.delete()
        
        return JsonResponse({'success': True, 'message': 'Entrada removida'})
    except WaitingList.DoesNotExist:
        return JsonResponse({'error': 'Entrada não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

