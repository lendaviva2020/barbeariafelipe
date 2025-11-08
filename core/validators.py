"""
Validadores customizados para o projeto
"""

import re
from datetime import date
from datetime import time as datetime_time

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_brazilian_phone(value):
    """
    Valida formato de telefone brasileiro
    Aceita: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX ou XXXXXXXXXXX
    """
    if not value:  # Permitir vazio
        return value

    # Remover caracteres não numéricos
    phone = re.sub(r"\D", "", str(value))

    # Validar comprimento (10 ou 11 dígitos)
    if len(phone) not in [10, 11]:
        raise ValidationError(
            _("Telefone deve ter 10 ou 11 dígitos (com DDD)"), code="invalid_phone"
        )

    # Validar DDD (código de área deve ser válido) - 11 a 99
    ddd = int(phone[:2])
    if ddd < 11 or ddd > 99:
        raise ValidationError(_("DDD inválido"), code="invalid_ddd")

    return value


def validate_cpf(value):
    """
    Valida CPF brasileiro com dígito verificador
    """
    # Remover caracteres não numéricos
    cpf = re.sub(r"\D", "", str(value))

    # Validar comprimento
    if len(cpf) != 11:
        raise ValidationError(_("CPF deve ter 11 dígitos"), code="invalid_cpf_length")

    # Validar CPFs conhecidos como inválidos
    if cpf in [
        "00000000000",
        "11111111111",
        "22222222222",
        "33333333333",
        "44444444444",
        "55555555555",
        "66666666666",
        "77777777777",
        "88888888888",
        "99999999999",
    ]:
        raise ValidationError(_("CPF inválido"), code="invalid_cpf")

    # Validar dígitos verificadores
    def calculate_digit(cpf_partial):
        total = sum(
            int(digit) * weight
            for digit, weight in zip(cpf_partial, range(len(cpf_partial) + 1, 1, -1))
        )
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    # Verificar primeiro dígito
    first_digit = calculate_digit(cpf[:9])
    if int(cpf[9]) != first_digit:
        raise ValidationError(_("CPF inválido"), code="invalid_cpf_digit")

    # Verificar segundo dígito
    second_digit = calculate_digit(cpf[:10])
    if int(cpf[10]) != second_digit:
        raise ValidationError(_("CPF inválido"), code="invalid_cpf_digit")

    return value


def validate_future_date(value):
    """
    Valida que a data não está no passado
    """
    if isinstance(value, str):
        from datetime import datetime

        value = datetime.strptime(value, "%Y-%m-%d").date()

    today = date.today()
    if value < today:
        raise ValidationError(
            _("A data não pode estar no passado"), code="date_in_past"
        )

    return value


def validate_appointment_date(value):
    """
    Valida data de agendamento (não pode ser passado e máximo 90 dias no futuro)
    """
    if isinstance(value, str):
        from datetime import datetime

        value = datetime.strptime(value, "%Y-%m-%d").date()

    today = date.today()

    if value < today:
        raise ValidationError(
            _("Não é possível agendar em datas passadas"), code="date_in_past"
        )

    # Máximo 90 dias no futuro
    from datetime import timedelta

    max_date = today + timedelta(days=90)
    if value > max_date:
        raise ValidationError(
            _("Não é possível agendar com mais de 90 dias de antecedência"),
            code="date_too_far",
        )

    return value


def validate_business_hours(value):
    """
    Valida que o horário está dentro do expediente comercial (08:00 - 20:00)
    """
    if isinstance(value, str):
        from datetime import datetime

        value = datetime.strptime(value, "%H:%M").time()

    opening_time = datetime_time(8, 0)  # 08:00
    closing_time = datetime_time(20, 0)  # 20:00

    if value < opening_time or value >= closing_time:
        raise ValidationError(
            _("Horário deve estar entre 08:00 e 20:00"), code="outside_business_hours"
        )

    return value


def validate_cep(value):
    """
    Valida formato de CEP brasileiro (XXXXX-XXX ou XXXXXXXX)
    """
    cep = re.sub(r"\D", "", str(value))

    if len(cep) != 8:
        raise ValidationError(_("CEP deve ter 8 dígitos"), code="invalid_cep")

    return value


def validate_price_positive(value):
    """
    Valida que o preço é positivo
    """
    if value <= 0:
        raise ValidationError(
            _("O preço deve ser maior que zero"), code="price_not_positive"
        )

    return value


def validate_duration_positive(value):
    """
    Valida que a duração é positiva (em minutos)
    """
    if value <= 0:
        raise ValidationError(
            _("A duração deve ser maior que zero"), code="duration_not_positive"
        )

    if value > 480:  # Máximo 8 horas
        raise ValidationError(
            _("A duração não pode ser maior que 8 horas"), code="duration_too_long"
        )

    return value


def validate_discount_percentage(value):
    """
    Valida que o desconto percentual está entre 0 e 100
    """
    if value < 0 or value > 100:
        raise ValidationError(
            _("O desconto deve estar entre 0% e 100%"),
            code="invalid_discount_percentage",
        )

    return value


def validate_appointment_interval(value):
    """
    Valida que os agendamentos são em intervalos de 30 minutos
    """
    if isinstance(value, str):
        from datetime import datetime

        value = datetime.strptime(value, "%H:%M").time()

    # Minutos devem ser 00 ou 30
    if value.minute not in [0, 30]:
        raise ValidationError(
            _("Agendamentos devem ser em intervalos de 30 minutos (00 ou 30)"),
            code="invalid_interval",
        )

    return value
