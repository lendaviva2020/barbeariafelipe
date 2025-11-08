"""
Integração WhatsApp
"""

import requests
from django.conf import settings


def send_whatsapp_message(phone, message):
    """
    Envia mensagem via WhatsApp API
    """
    # Por enquanto, apenas redireciona para WhatsApp Web
    # Em produção, você pode integrar com WhatsApp Business API

    whatsapp_phone = settings.WHATSAPP_PHONE
    encoded_message = requests.utils.quote(message)
    whatsapp_url = f"https://wa.me/{whatsapp_phone}?text={encoded_message}"

    return whatsapp_url


def generate_appointment_confirmation(appointment):
    """
    Gera mensagem de confirmação de agendamento
    """
    message = f"""
🎉 *Agendamento Confirmado!*

✅ *Cliente:* {appointment.customer_name}
📅 *Data:* {appointment.appointment_date.strftime('%d/%m/%Y')}
🕐 *Horário:* {appointment.appointment_time.strftime('%H:%M')}
✂️ *Serviço:* {appointment.service.name}
👨‍💼 *Barbeiro:* {appointment.barber.name}
💰 *Valor:* R$ {appointment.final_price:.2f}

📱 *Telefone:* {appointment.customer_phone}

Agradecemos pela preferência!
Barbearia Francisco - Tradição desde 1947
""".strip()

    return message


def send_appointment_confirmation(appointment):
    """
    Envia confirmação de agendamento via WhatsApp
    """
    message = generate_appointment_confirmation(appointment)
    return send_whatsapp_message(appointment.customer_phone, message)
