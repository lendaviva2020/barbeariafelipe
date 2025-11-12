"""
Configuração do Celery
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbearia.settings')

app = Celery('barbearia')

# Load config from Django settings (CELERY_ prefix)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all apps
app.autodiscover_tasks()

# Configurar tarefas periódicas
app.conf.beat_schedule = {
    # Enviar lembretes diários às 18:00
    'send-daily-reminders': {
        'task': 'core.tasks.send_reminder_notifications',
        'schedule': crontab(hour=18, minute=0),
    },
    # Gerar agendamentos recorrentes diariamente às 6:00
    'generate-recurring-daily': {
        'task': 'core.tasks.generate_recurring_appointments_task',
        'schedule': crontab(hour=6, minute=0),
    },
    # Limpar notificações antigas semanalmente (domingos às 3:00)
    'cleanup-old-notifications': {
        'task': 'core.tasks.cleanup_old_notifications',
        'schedule': crontab(hour=3, minute=0, day_of_week=0),
    },
    # Limpar mensagens de chat antigas mensalmente (dia 1 às 4:00)
    'cleanup-old-chat-messages': {
        'task': 'core.tasks.cleanup_old_chat_messages',
        'schedule': crontab(hour=4, minute=0, day_of_month=1),
    },
    # Retentar notificações falhadas a cada 6 horas
    'retry-failed-notifications': {
        'task': 'core.tasks.retry_failed_notifications',
        'schedule': crontab(hour='*/6', minute=0),
    },
    # Verificar no-shows a cada hora
    'check-appointment-no-shows': {
        'task': 'core.tasks.check_appointment_no_shows',
        'schedule': crontab(hour='*', minute=0),
    },
    # Atualizar contextos de IA diariamente às 2:00
    'update-ai-contexts': {
        'task': 'core.tasks.update_ai_conversation_contexts',
        'schedule': crontab(hour=2, minute=0),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

