"""
Integração WhatsApp com Twilio
"""

import re
import logging
from typing import Optional, Dict
from django.conf import settings
from django.utils import timezone
from core.models import Notification

logger = logging.getLogger(__name__)

# Lazy import para evitar erro se Twilio não estiver instalado
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    logger.warning("Twilio não instalado. Notificações WhatsApp via API desabilitadas.")


def sanitize_phone(phone: str) -> str:
    """
    Sanitiza e formata número de telefone
    
    Args:
        phone: Número de telefone
    
    Returns:
        Número formatado (apenas dígitos)
    """
    # Remove todos os caracteres não numéricos
    digits_only = re.sub(r'\D', '', phone)
    
    # Adiciona código do país se não tiver (Brasil = 55)
    if len(digits_only) == 11:  # DDD + número
        digits_only = '55' + digits_only
    elif len(digits_only) == 10:  # DDD + número sem 9
        digits_only = '55' + digits_only
    
    return digits_only


def sanitize_message_content(text: str, max_length: int = 1000) -> str:
    """
    Sanitiza conteúdo da mensagem
    
    Args:
        text: Texto da mensagem
        max_length: Tamanho máximo
    
    Returns:
        Texto sanitizado
    """
    if not text:
        return ""
    
    # Remove caracteres perigosos mas mantém formatação básica
    sanitized = text.replace('<', '').replace('>', '').replace('"', '').replace('`', '')
    
    # Limita tamanho
    sanitized = sanitized.strip()[:max_length]
    
    return sanitized


def generate_confirmation_message(appointment) -> str:
    """
    Gera mensagem de confirmação de agendamento
    """
    message = f"""🔥 *AGENDAMENTO CONFIRMADO* 🔥

👤 *Cliente:* {appointment.customer_name}
📞 *Telefone:* {appointment.customer_phone}
✂️ *Serviço:* {appointment.service.name}
💰 *Valor:* R$ {appointment.final_price:.2f}
📅 *Data:* {appointment.appointment_date.strftime('%d/%m/%Y')}
⏰ *Horário:* {appointment.appointment_time.strftime('%H:%M')}
💈 *Barbeiro:* {appointment.barber.name}

📍 *Local:* Rua José R Filho, N° 150, Bairro Guilhermina Tenffen, Cafelândia, Paraná

⚠️ *IMPORTANTE:*
- Chegue 10 minutos antes
- Cancelamentos até 2h antes
- WhatsApp: (45) 99941-7111

Obrigado por escolher a Barbearia Francisco! 💈✨"""
    
    return sanitize_message_content(message)


def generate_reminder_message(appointment) -> str:
    """
    Gera mensagem de lembrete (1 dia antes)
    """
    message = f"""⏰ *Lembrete de Agendamento*

Olá {appointment.customer_name}!

Lembrete: seu agendamento é amanhã!
📅 Data: {appointment.appointment_date.strftime('%d/%m/%Y')}
🕐 Horário: {appointment.appointment_time.strftime('%H:%M')}
✂️ Serviço: {appointment.service.name}
💈 Barbeiro: {appointment.barber.name}

📍 Rua José R Filho, N° 150, Bairro Guilhermina Tenffen, Cafelândia, PR

Nos vemos em breve! 🎩
Barbearia Francisco"""
    
    return sanitize_message_content(message)


def generate_completion_message(appointment) -> str:
    """
    Gera mensagem de conclusão do serviço
    """
    message = f"""✨ *Obrigado pela Preferência!*

Olá {appointment.customer_name}!

Esperamos que tenha gostado do resultado! 😊

📸 Adoraríamos ver o resultado final!
Tire uma foto e envie para nós.

⭐ Não esqueça de deixar sua avaliação!

Até a próxima! 🎩
Barbearia Francisco
(45) 99941-7111"""
    
    return sanitize_message_content(message)


def generate_cancellation_message(appointment) -> str:
    """
    Gera mensagem de cancelamento
    """
    message = f"""❌ *Agendamento Cancelado*

Olá {appointment.customer_name},

Seu agendamento foi cancelado.
📅 Data: {appointment.appointment_date.strftime('%d/%m/%Y')}
🕐 Horário: {appointment.appointment_time.strftime('%H:%M')}

Esperamos vê-lo em breve!
Barbearia Francisco - (45) 99941-7111"""
    
    return sanitize_message_content(message)


def generate_rescheduled_message(appointment) -> str:
    """
    Gera mensagem de reagendamento
    """
    message = f"""🔄 *Agendamento Reagendado*

Olá {appointment.customer_name}!

Seu agendamento foi reagendado:
📅 Nova data: {appointment.appointment_date.strftime('%d/%m/%Y')}
🕐 Novo horário: {appointment.appointment_time.strftime('%H:%M')}
✂️ Serviço: {appointment.service.name}
💈 Barbeiro: {appointment.barber.name}

📍 Rua José R Filho, N° 150, Bairro Guilhermina Tenffen, Cafelândia, PR

Até breve! 🎩
Barbearia Francisco"""
    
    return sanitize_message_content(message)


def send_whatsapp_via_twilio(phone: str, message: str) -> Dict:
    """
    Envia mensagem via Twilio WhatsApp API
    
    Args:
        phone: Número do telefone
        message: Mensagem a enviar
    
    Returns:
        Dict com status e informações do envio
    """
    if not TWILIO_AVAILABLE:
        return {
            'success': False,
            'error': 'Twilio não disponível',
            'fallback_url': generate_whatsapp_web_url(phone, message)
        }
    
    try:
        # Obter credenciais do Twilio
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        whatsapp_number = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        if not account_sid or not auth_token:
            return {
                'success': False,
                'error': 'Credenciais Twilio não configuradas',
                'fallback_url': generate_whatsapp_web_url(phone, message)
            }
        
        # Sanitizar telefone
        clean_phone = sanitize_phone(phone)
        
        # Criar cliente Twilio
        client = Client(account_sid, auth_token)
        
        # Enviar mensagem
        twilio_message = client.messages.create(
            from_=whatsapp_number,
            body=message,
            to=f'whatsapp:+{clean_phone}'
        )
        
        logger.info(f"WhatsApp enviado via Twilio: {twilio_message.sid}")
        
        return {
            'success': True,
            'status': twilio_message.status,
            'sid': twilio_message.sid,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Erro ao enviar WhatsApp via Twilio: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'fallback_url': generate_whatsapp_web_url(phone, message)
        }


def generate_whatsapp_web_url(phone: str, message: str) -> str:
    """
    Gera URL do WhatsApp Web (fallback)
    
    Args:
        phone: Número do telefone
        message: Mensagem
    
    Returns:
        URL do WhatsApp Web
    """
    import urllib.parse
    clean_phone = sanitize_phone(phone)
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{clean_phone}?text={encoded_message}"


def send_notification(appointment, notification_type: str, user) -> Dict:
    """
    Envia notificação WhatsApp e registra no banco
    
    Args:
        appointment: Agendamento
        notification_type: Tipo da notificação (confirmation, reminder, etc)
        user: Usuário responsável pelo envio
    
    Returns:
        Dict com resultado do envio
    """
    # Gerar mensagem baseada no tipo
    message_generators = {
        'confirmation': generate_confirmation_message,
        'reminder': generate_reminder_message,
        'completed': generate_completion_message,
        'cancellation': generate_cancellation_message,
        'rescheduled': generate_rescheduled_message,
    }
    
    generator = message_generators.get(notification_type)
    if not generator:
        return {
            'success': False,
            'error': f'Tipo de notificação inválido: {notification_type}'
        }
    
    message = generator(appointment)
    phone = appointment.customer_phone
    
    # Criar registro de notificação
    notification = Notification.objects.create(
        user=user,
        appointment=appointment,
        type=notification_type,
        channel='whatsapp',
        recipient=phone,
        message=message,
        status='pending'
    )
    
    # Tentar enviar via Twilio
    result = send_whatsapp_via_twilio(phone, message)
    
    # Atualizar notificação
    if result['success']:
        notification.mark_as_sent(external_id=result.get('sid'))
    else:
        notification.mark_as_failed(result.get('error', 'Erro desconhecido'))
    
    # Adicionar URL de fallback
    result['whatsapp_url'] = generate_whatsapp_web_url(phone, message)
    result['notification_id'] = notification.id
    
    return result


# Manter compatibilidade com código antigo
def send_whatsapp_message(phone, message):
    """
    DEPRECATED: Use send_notification() ao invés
    Mantido para compatibilidade
    """
    return generate_whatsapp_web_url(phone, message)


def generate_appointment_confirmation(appointment):
    """
    DEPRECATED: Use generate_confirmation_message() ao invés
    Mantido para compatibilidade
    """
    return generate_confirmation_message(appointment)


def send_appointment_confirmation(appointment):
    """
    DEPRECATED: Use send_notification() ao invés
    Mantido para compatibilidade
    """
    return generate_whatsapp_web_url(appointment.customer_phone, generate_confirmation_message(appointment))
