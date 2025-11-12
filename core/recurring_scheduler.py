"""
Sistema de Agendamentos Recorrentes
"""
from datetime import datetime, timedelta, date
from typing import List, Dict
import logging
from django.utils import timezone
from django.db import transaction
from core.models import RecurringAppointment
from agendamentos.models import Agendamento

logger = logging.getLogger(__name__)


def get_next_occurrence(day_of_week: int, start_from: date = None) -> date:
    """
    Calcula a próxima ocorrência do dia da semana
    
    Args:
        day_of_week: Dia da semana (0=Segunda, 6=Domingo)
        start_from: Data inicial (default: hoje)
    
    Returns:
        Data da próxima ocorrência
    """
    if start_from is None:
        start_from = timezone.now().date()
    
    days_ahead = day_of_week - start_from.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    
    return start_from + timedelta(days=days_ahead)


def check_appointment_exists(recurring: RecurringAppointment, appointment_date: date) -> bool:
    """
    Verifica se já existe agendamento para esta recorrência na data especificada
    
    Args:
        recurring: Agendamento recorrente
        appointment_date: Data do agendamento
    
    Returns:
        True se já existe
    """
    return Agendamento.objects.filter(
        user=recurring.user,
        barber=recurring.barber,
        service=recurring.service,
        appointment_date=appointment_date,
        appointment_time=recurring.time
    ).exists()


def create_appointment_from_recurring(recurring: RecurringAppointment, appointment_date: date) -> Agendamento:
    """
    Cria um agendamento a partir de uma recorrência
    
    Args:
        recurring: Agendamento recorrente
        appointment_date: Data do agendamento
    
    Returns:
        Agendamento criado
    """
    appointment = Agendamento.objects.create(
        user=recurring.user,
        service=recurring.service,
        barber=recurring.barber,
        appointment_date=appointment_date,
        appointment_time=recurring.time,
        customer_name=recurring.customer_name,
        customer_phone=recurring.customer_phone,
        customer_email=recurring.customer_email,
        notes=recurring.notes,
        payment_method='cash',  # Default
        price=recurring.service.price,
        status='pending'
    )
    
    logger.info(f"Agendamento criado a partir de recorrência {recurring.id}: {appointment.id}")
    return appointment


def deactivate_expired_recurrences() -> int:
    """
    Desativa recorrências expiradas
    
    Returns:
        Número de recorrências desativadas
    """
    today = timezone.now().date()
    
    expired = RecurringAppointment.objects.filter(
        is_active=True,
        end_date__lt=today
    )
    
    count = expired.count()
    expired.update(is_active=False)
    
    logger.info(f"Desativadas {count} recorrências expiradas")
    return count


def generate_recurring_appointments(days_ahead: int = 7) -> Dict:
    """
    Gera agendamentos recorrentes para os próximos N dias
    
    Args:
        days_ahead: Número de dias para gerar à frente
    
    Returns:
        Dict com estatísticas de geração
    """
    today = timezone.now().date()
    end_date = today + timedelta(days=days_ahead)
    
    stats = {
        'processed': 0,
        'created': 0,
        'skipped': 0,
        'errors': 0,
        'deactivated': 0
    }
    
    # Primeiro, desativar recorrências expiradas
    stats['deactivated'] = deactivate_expired_recurrences()
    
    # Buscar todas as recorrências ativas
    active_recurrences = RecurringAppointment.objects.filter(is_active=True).select_related(
        'user', 'service', 'barber'
    )
    
    logger.info(f"Processando {active_recurrences.count()} recorrências ativas")
    
    for recurring in active_recurrences:
        stats['processed'] += 1
        
        try:
            # Verificar se a recorrência já expirou
            if recurring.end_date and recurring.end_date < today:
                recurring.is_active = False
                recurring.save()
                stats['deactivated'] += 1
                continue
            
            # Calcular próximas ocorrências dentro do período
            current_date = today
            while current_date <= end_date:
                next_occurrence = get_next_occurrence(recurring.day_of_week, current_date)
                
                if next_occurrence > end_date:
                    break
                
                # Verificar se está dentro do período de validade
                if recurring.end_date and next_occurrence > recurring.end_date:
                    break
                
                # Verificar se não está no passado
                if next_occurrence < today:
                    current_date = next_occurrence + timedelta(days=1)
                    continue
                
                # Verificar se agendamento já existe
                if check_appointment_exists(recurring, next_occurrence):
                    stats['skipped'] += 1
                    logger.debug(f"Agendamento já existe para {next_occurrence}")
                else:
                    # Criar agendamento
                    with transaction.atomic():
                        create_appointment_from_recurring(recurring, next_occurrence)
                        stats['created'] += 1
                
                # Avançar para próxima semana
                current_date = next_occurrence + timedelta(days=7)
        
        except Exception as e:
            logger.error(f"Erro ao processar recorrência {recurring.id}: {str(e)}")
            stats['errors'] += 1
    
    logger.info(f"Geração concluída: {stats}")
    return stats


def get_recurring_stats() -> Dict:
    """
    Retorna estatísticas sobre agendamentos recorrentes
    
    Returns:
        Dict com estatísticas
    """
    total_recurring = RecurringAppointment.objects.count()
    active_recurring = RecurringAppointment.objects.filter(is_active=True).count()
    
    # Contar agendamentos futuros gerados de recorrências
    today = timezone.now().date()
    future_appointments = Agendamento.objects.filter(
        appointment_date__gte=today,
        status='pending'
    ).count()
    
    return {
        'total_recurring': total_recurring,
        'active_recurring': active_recurring,
        'inactive_recurring': total_recurring - active_recurring,
        'future_appointments': future_appointments
    }


def cleanup_old_recurrences(days_old: int = 90) -> int:
    """
    Remove recorrências inativas antigas
    
    Args:
        days_old: Remover recorrências inativas há mais de N dias
    
    Returns:
        Número de recorrências removidas
    """
    cutoff_date = timezone.now().date() - timedelta(days=days_old)
    
    old_recurrences = RecurringAppointment.objects.filter(
        is_active=False,
        end_date__lt=cutoff_date
    )
    
    count = old_recurrences.count()
    old_recurrences.delete()
    
    logger.info(f"Removidas {count} recorrências antigas")
    return count

