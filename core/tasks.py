"""
Tarefas Celery para notificações automáticas e processamento assíncrono
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_reminder_notifications(self):
    """
    Envia notificações de lembrete para agendamentos no dia seguinte
    Executar diariamente às 18:00
    """
    from agendamentos.models import Agendamento
    from .whatsapp import send_notification
    
    tomorrow = timezone.now().date() + timedelta(days=1)
    
    # Buscar agendamentos para amanhã que estão confirmados
    appointments = Agendamento.objects.filter(
        appointment_date=tomorrow,
        status='confirmed'
    ).select_related('user', 'barber', 'service')
    
    sent_count = 0
    error_count = 0
    
    logger.info(f"Iniciando envio de lembretes: {appointments.count()} agendamentos")
    
    for appointment in appointments:
        try:
            # Enviar notificação de lembrete
            result = send_notification(appointment, 'reminder', appointment.user)
            
            if result.get('success'):
                sent_count += 1
                logger.info(f"Lembrete enviado para agendamento {appointment.id}")
            else:
                error_count += 1
                logger.error(f"Erro ao enviar lembrete para agendamento {appointment.id}: {result.get('error')}")
        
        except Exception as e:
            error_count += 1
            logger.error(f"Exceção ao enviar lembrete para agendamento {appointment.id}: {str(e)}")
            # Retry task se houver erro
            if self.request.retries < self.max_retries:
                raise self.retry(exc=e, countdown=300)  # Retry após 5 minutos
    
    logger.info(f"Envio de lembretes concluído: {sent_count} enviados, {error_count} erros")
    
    return {
        'sent': sent_count,
        'errors': error_count,
        'total': appointments.count()
    }


@shared_task
def send_confirmation_notification_async(appointment_id):
    """
    Envia notificação de confirmação de forma assíncrona
    
    Args:
        appointment_id: ID do agendamento
    """
    from agendamentos.models import Agendamento
    from .whatsapp import send_notification
    
    try:
        appointment = Agendamento.objects.get(id=appointment_id)
        result = send_notification(appointment, 'confirmation', appointment.user)
        
        if result.get('success'):
            logger.info(f"Confirmação enviada para agendamento {appointment_id}")
            return {'success': True, 'appointment_id': appointment_id}
        else:
            logger.error(f"Erro ao enviar confirmação: {result.get('error')}")
            return {'success': False, 'error': result.get('error')}
    
    except Agendamento.DoesNotExist:
        logger.error(f"Agendamento {appointment_id} não encontrado")
        return {'success': False, 'error': 'Agendamento não encontrado'}
    except Exception as e:
        logger.error(f"Erro ao enviar confirmação: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task
def generate_recurring_appointments_task():
    """
    Gera agendamentos recorrentes
    Executar diariamente
    """
    from .recurring_scheduler import generate_recurring_appointments
    
    logger.info("Iniciando geração de agendamentos recorrentes")
    
    try:
        result = generate_recurring_appointments(days_ahead=7)
        logger.info(f"Geração de recorrentes concluída: {result}")
        return result
    except Exception as e:
        logger.error(f"Erro ao gerar recorrentes: {str(e)}")
        raise


@shared_task
def cleanup_old_notifications():
    """
    Remove notificações antigas (>90 dias)
    Executar semanalmente
    """
    from .models import Notification
    
    cutoff_date = timezone.now() - timedelta(days=90)
    
    old_notifications = Notification.objects.filter(created_at__lt=cutoff_date)
    count = old_notifications.count()
    old_notifications.delete()
    
    logger.info(f"Removidas {count} notificações antigas")
    return {'deleted': count}


@shared_task
def cleanup_old_chat_messages():
    """
    Remove mensagens de chat antigas de agendamentos concluídos (>180 dias)
    Executar mensalmente
    """
    from .models import ChatMessage
    from agendamentos.models import Agendamento
    
    cutoff_date = timezone.now() - timedelta(days=180)
    
    # Buscar agendamentos antigos concluídos ou cancelados
    old_appointments = Agendamento.objects.filter(
        appointment_date__lt=cutoff_date.date(),
        status__in=['completed', 'cancelled']
    )
    
    # Remover mensagens desses agendamentos
    count = ChatMessage.objects.filter(appointment__in=old_appointments).delete()[0]
    
    logger.info(f"Removidas {count} mensagens de chat antigas")
    return {'deleted': count}


@shared_task(bind=True, max_retries=3)
def retry_failed_notifications(self):
    """
    Retenta enviar notificações que falharam
    Executar a cada 6 horas
    """
    from .models import Notification
    from .whatsapp import send_whatsapp_via_twilio
    
    # Buscar notificações falhadas nas últimas 24 horas
    cutoff_time = timezone.now() - timedelta(hours=24)
    
    failed_notifications = Notification.objects.filter(
        status='failed',
        created_at__gte=cutoff_time
    ).select_related('appointment')
    
    retry_count = 0
    success_count = 0
    
    logger.info(f"Retrying {failed_notifications.count()} failed notifications")
    
    for notification in failed_notifications:
        try:
            result = send_whatsapp_via_twilio(notification.recipient, notification.message)
            
            if result.get('success'):
                notification.mark_as_sent(external_id=result.get('sid'))
                success_count += 1
            else:
                notification.error_message = result.get('error', 'Retry failed')
                notification.save()
            
            retry_count += 1
        
        except Exception as e:
            logger.error(f"Error retrying notification {notification.id}: {str(e)}")
    
    logger.info(f"Retry completed: {retry_count} retried, {success_count} successful")
    
    return {
        'retried': retry_count,
        'successful': success_count
    }


@shared_task
def update_ai_conversation_contexts():
    """
    Atualiza contextos de conversa antigos
    Executar diariamente
    """
    from .models import AIConversationContext
    
    # Buscar contextos sem atividade há mais de 7 dias
    cutoff_date = timezone.now() - timedelta(days=7)
    
    old_contexts = AIConversationContext.objects.filter(
        updated_at__lt=cutoff_date
    )
    
    # Pode adicionar lógica de limpeza ou resumo aqui
    count = old_contexts.count()
    
    logger.info(f"Encontrados {count} contextos de conversa inativos")
    return {'inactive_contexts': count}


@shared_task
def send_completion_notification_async(appointment_id):
    """
    Envia notificação de conclusão de forma assíncrona
    
    Args:
        appointment_id: ID do agendamento
    """
    from agendamentos.models import Agendamento
    from .whatsapp import send_notification
    
    try:
        appointment = Agendamento.objects.get(id=appointment_id)
        
        # Aguardar 5 minutos antes de enviar (dar tempo do cliente sair)
        from time import sleep
        sleep(300)
        
        result = send_notification(appointment, 'completed', appointment.user)
        
        if result.get('success'):
            logger.info(f"Notificação de conclusão enviada para agendamento {appointment_id}")
            return {'success': True, 'appointment_id': appointment_id}
        else:
            logger.error(f"Erro ao enviar notificação de conclusão: {result.get('error')}")
            return {'success': False, 'error': result.get('error')}
    
    except Agendamento.DoesNotExist:
        logger.error(f"Agendamento {appointment_id} não encontrado")
        return {'success': False, 'error': 'Agendamento não encontrado'}
    except Exception as e:
        logger.error(f"Erro ao enviar notificação de conclusão: {str(e)}")
        return {'success': False, 'error': str(e)}


@shared_task
def check_appointment_no_shows():
    """
    Verifica agendamentos que não foram comparecidos (no-show)
    Executar a cada hora
    """
    from agendamentos.models import Agendamento
    
    # Buscar agendamentos confirmados que já passaram há mais de 2 horas
    cutoff_time = timezone.now() - timedelta(hours=2)
    
    no_show_appointments = Agendamento.objects.filter(
        status='confirmed',
        appointment_date__lt=timezone.now().date()
    )
    
    # Para agendamentos de hoje, verificar horário
    today_no_shows = no_show_appointments.filter(
        appointment_date=timezone.now().date()
    )
    
    # Atualizar status para cancelled ou adicionar nota
    count = 0
    for appointment in today_no_shows:
        # Verificar se já passou da hora
        from datetime import datetime, time
        appointment_datetime = datetime.combine(appointment.appointment_date, appointment.appointment_time)
        
        if timezone.make_aware(appointment_datetime) < cutoff_time:
            appointment.notes += "\n[Sistema] Possível no-show detectado."
            appointment.save()
            count += 1
    
    logger.info(f"Verificados {count} possíveis no-shows")
    return {'checked': count}

