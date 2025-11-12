"""
Sistema de Chat com IA usando Google Gemini
"""
import re
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from django.utils import timezone
from core.models import AISettings, ChatMessage, AIConversationContext, BarbershopSettings
import logging

logger = logging.getLogger(__name__)

# Lazy import para evitar erro se biblioteca não estiver instalada
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai não instalado. Sistema de IA desabilitado.")


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitiza input do usuário para prevenir injeção e ataques
    
    Args:
        text: Texto a ser sanitizado
        max_length: Tamanho máximo permitido
    
    Returns:
        Texto sanitizado
    """
    if not text:
        return ""
    
    # Remove caracteres perigosos
    sanitized = text.replace('<', '').replace('>', '').replace('"', '').replace("'", '').replace('`', '')
    
    # Remove carriage returns mas mantém newlines
    sanitized = sanitized.replace('\r', '')
    
    # Remove múltiplos espaços
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Limita tamanho
    sanitized = sanitized.strip()[:max_length]
    
    return sanitized


def detect_requires_human_attention(message: str) -> bool:
    """
    Detecta se a mensagem requer atenção humana
    
    Args:
        message: Mensagem do usuário
    
    Returns:
        True se requer atenção humana
    """
    keywords = [
        'cancelar', 'cancela', 'cancelamento',
        'reagendar', 'remarcar', 'mudar data', 'mudar horário',
        'reclamação', 'reclamar', 'problema', 'insatisfeito',
        'reembolso', 'devolução', 'dinheiro de volta',
        'gerente', 'falar com responsável', 'supervisor'
    ]
    
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in keywords)


def build_system_prompt(appointment, ai_settings: Optional[AISettings], barbershop_settings: Optional[BarbershopSettings]) -> str:
    """
    Constrói o prompt do sistema personalizado
    
    Args:
        appointment: Agendamento relacionado
        ai_settings: Configurações de IA do barbeiro
        barbershop_settings: Configurações da barbearia
    
    Returns:
        Prompt do sistema
    """
    barbershop_name = barbershop_settings.name if barbershop_settings else "Barbearia Francisco"
    barbershop_address = barbershop_settings.address if barbershop_settings else "Rua José R Filho, N° 150, Bairro Guilhermina Tenffen, Cafelândia, Paraná"
    barbershop_phone = barbershop_settings.phone if barbershop_settings else "(45) 99941-7111"
    
    personality = "Seja amigável e descontraído" if not ai_settings or ai_settings.personality == 'friendly' else "Seja profissional e formal"
    
    custom_instructions = ""
    if ai_settings and ai_settings.custom_instructions:
        custom_instructions = f"\n\nINSTRUÇÕES PERSONALIZADAS: {ai_settings.custom_instructions}"
    
    prompt = f"""Você é o assistente virtual da {barbershop_name}.

INFORMAÇÕES DA BARBEARIA:
- Nome: {barbershop_name}
- Endereço: {barbershop_address}
- Telefone: {barbershop_phone}

AGENDAMENTO ATUAL:
- Cliente: {appointment.customer_name}
- Barbeiro: {appointment.barber.name}
- Serviço: {appointment.service.name} (R$ {appointment.service.price})
- Data: {appointment.appointment_date.strftime('%d/%m/%Y')}
- Horário: {appointment.appointment_time.strftime('%H:%M')}
- Status: {appointment.get_status_display()}

PERSONALIDADE: {personality}
{custom_instructions}

DIRETRIZES:
- Responda em português brasileiro
- Seja breve e objetivo (máximo 3 frases)
- Se não souber algo, seja honesto
- Para alterações de agendamento, peça para falar com o barbeiro
- Sempre mantenha tom cordial e profissional
- Use emojis ocasionalmente para deixar mais amigável
- NUNCA invente informações que você não sabe
- NUNCA confirme alterações sem aprovação humana
"""
    
    return prompt


def get_conversation_history(appointment, limit: int = 10) -> List[Dict[str, str]]:
    """
    Busca histórico de conversas do agendamento
    
    Args:
        appointment: Agendamento
        limit: Limite de mensagens
    
    Returns:
        Lista de mensagens formatadas para a IA
    """
    messages = ChatMessage.objects.filter(
        appointment=appointment
    ).order_by('-created_at')[:limit]
    
    # Reverter ordem para cronológica
    messages = reversed(messages)
    
    history = []
    for msg in messages:
        role = 'assistant' if msg.is_ai_response else 'user'
        history.append({
            'role': role,
            'content': msg.message
        })
    
    return history


def generate_ai_response(appointment, user_message: str) -> Tuple[str, bool]:
    """
    Gera resposta da IA para uma mensagem do usuário
    
    Args:
        appointment: Agendamento relacionado
        user_message: Mensagem do usuário
    
    Returns:
        Tupla (resposta_ia, requer_atencao_humana)
    
    Raises:
        Exception: Se houver erro na geração
    """
    if not GEMINI_AVAILABLE:
        raise Exception("Sistema de IA não disponível. Biblioteca não instalada.")
    
    # Verificar se IA está habilitada para o barbeiro
    try:
        ai_settings = AISettings.objects.get(barber=appointment.barber)
        if not ai_settings.is_enabled:
            raise Exception("IA desabilitada para este barbeiro")
    except AISettings.DoesNotExist:
        ai_settings = None
    
    # Sanitizar mensagem do usuário
    sanitized_message = sanitize_input(user_message)
    
    if not sanitized_message:
        raise Exception("Mensagem vazia ou inválida")
    
    # Detectar se requer atenção humana
    requires_attention = detect_requires_human_attention(sanitized_message)
    
    # Buscar configurações da barbearia
    try:
        barbershop_settings = BarbershopSettings.objects.first()
    except:
        barbershop_settings = None
    
    # Construir prompt do sistema
    system_prompt = build_system_prompt(appointment, ai_settings, barbershop_settings)
    
    # Buscar histórico de conversa
    history = get_conversation_history(appointment)
    
    # Configurar Gemini
    try:
        gemini_api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not gemini_api_key:
            raise Exception("GEMINI_API_KEY não configurada")
        
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Preparar mensagens para o modelo
        chat = model.start_chat(history=[])
        
        # Enviar prompt do sistema primeiro
        full_prompt = f"{system_prompt}\n\nHistórico de conversa:\n"
        for msg in history:
            role_label = "Cliente" if msg['role'] == 'user' else "Assistente"
            full_prompt += f"{role_label}: {msg['content']}\n"
        
        full_prompt += f"\nCliente: {sanitized_message}\n\nResponda como o assistente:"
        
        # Gerar resposta
        response = chat.send_message(full_prompt)
        ai_message = response.text.strip()
        
        # Limitar tamanho da resposta
        if len(ai_message) > 500:
            ai_message = ai_message[:497] + "..."
        
        logger.info(f"IA respondeu para agendamento {appointment.id}: {ai_message[:50]}...")
        
        return ai_message, requires_attention
        
    except Exception as e:
        logger.error(f"Erro ao gerar resposta da IA: {str(e)}")
        raise Exception(f"Erro ao processar solicitação: {str(e)}")


def process_chat_message(appointment, user, message: str) -> Dict:
    """
    Processa uma mensagem de chat e gera resposta da IA
    
    Args:
        appointment: Agendamento
        user: Usuário que enviou
        message: Mensagem
    
    Returns:
        Dict com user_message, ai_message e requires_human_attention
    """
    # Salvar mensagem do usuário
    user_msg = ChatMessage.objects.create(
        appointment=appointment,
        sender=user,
        message=sanitize_input(message),
        is_ai_response=False
    )
    
    try:
        # Gerar resposta da IA
        ai_response, requires_attention = generate_ai_response(appointment, message)
        
        # Salvar resposta da IA
        ai_msg = ChatMessage.objects.create(
            appointment=appointment,
            sender=None,  # IA não tem sender
            message=ai_response,
            is_ai_response=True,
            requires_human_attention=requires_attention
        )
        
        # Atualizar ou criar contexto
        context, created = AIConversationContext.objects.get_or_create(
            appointment=appointment,
            defaults={
                'context_data': {},
                'message_count': 0
            }
        )
        
        context.last_user_message = user_msg.message
        context.last_ai_response = ai_msg.message
        context.last_summary = ai_response
        context.message_count += 2  # Usuário + IA
        context.save()
        
        return {
            'success': True,
            'user_message': user_msg,
            'ai_message': ai_msg,
            'requires_human_attention': requires_attention
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem de chat: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'user_message': user_msg
        }


def get_ai_statistics(barber=None) -> Dict:
    """
    Retorna estatísticas do sistema de IA
    
    Args:
        barber: Filtrar por barbeiro (opcional)
    
    Returns:
        Dict com estatísticas
    """
    from agendamentos.models import Agendamento
    
    filters = {}
    if barber:
        filters['appointment__barber'] = barber
    
    total_messages = ChatMessage.objects.filter(**filters).count()
    ai_messages = ChatMessage.objects.filter(is_ai_response=True, **filters).count()
    human_attention = ChatMessage.objects.filter(requires_human_attention=True, **filters).count()
    
    stats = {
        'total_messages': total_messages,
        'ai_messages': ai_messages,
        'user_messages': total_messages - ai_messages,
        'requires_attention': human_attention,
        'ai_response_rate': (ai_messages / total_messages * 100) if total_messages > 0 else 0,
        'attention_rate': (human_attention / total_messages * 100) if total_messages > 0 else 0
    }
    
    return stats

