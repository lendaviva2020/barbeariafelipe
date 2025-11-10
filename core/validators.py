"""
Validadores brasileiros: CPF, CNPJ, Telefone
"""

from django.core.exceptions import ValidationError


def validate_cpf(cpf):
    """Valida CPF brasileiro"""
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos')
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        raise ValidationError('CPF inválido')
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[10]) != digito2:
        raise ValidationError('CPF inválido')
    
    return cpf


def validate_cnpj(cnpj):
    """Valida CNPJ brasileiro"""
    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        raise ValidationError('CNPJ deve ter 14 dígitos')
    
    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        raise ValidationError('CNPJ inválido')
    
    # Calcula primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj[12]) != digito1:
        raise ValidationError('CNPJ inválido')
    
    # Calcula segundo dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cnpj[13]) != digito2:
        raise ValidationError('CNPJ inválido')
    
    return cnpj


def validate_phone(phone):
    """Valida telefone brasileiro (com DDD)"""
    # Remove caracteres não numéricos
    phone = ''.join(filter(str.isdigit, phone))
    
    # Verifica tamanho (10 ou 11 dígitos)
    if len(phone) not in [10, 11]:
        raise ValidationError('Telefone deve ter 10 ou 11 dígitos (com DDD)')
    
    # Verifica DDD válido (11 a 99)
    ddd = int(phone[:2])
    if ddd < 11 or ddd > 99:
        raise ValidationError('DDD inválido')
    
    return phone


def format_cpf(cpf):
    """Formata CPF: 123.456.789-00"""
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return cpf
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'


def format_cnpj(cnpj):
    """Formata CNPJ: 12.345.678/0001-00"""
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14:
        return cnpj
    return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'


def format_phone(phone):
    """Formata telefone: (11) 98765-4321"""
    phone = ''.join(filter(str.isdigit, phone))
    if len(phone) == 11:
        return f'({phone[:2]}) {phone[2:7]}-{phone[7:]}'
    elif len(phone) == 10:
        return f'({phone[:2]}) {phone[2:6]}-{phone[6:]}'
    return phone


def validate_price_positive(value):
    """Valida se o preço é positivo"""
    if value <= 0:
        raise ValidationError('O preço deve ser maior que zero')
    return value


def validate_duration_positive(value):
    """Valida se a duração é positiva"""
    if value <= 0:
        raise ValidationError('A duração deve ser maior que zero')
    return value


def validate_future_date(value):
    """Valida se a data é futura"""
    from datetime import date
    if value < date.today():
        raise ValidationError('A data deve ser no futuro')
    return value


def validate_business_hours(value):
    """Valida se o horário está dentro do horário comercial (8h-20h)"""
    from datetime import time
    if value < time(8, 0) or value > time(20, 0):
        raise ValidationError('Horário deve ser entre 08:00 e 20:00')
    return value


def validate_appointment_interval(value):
    """Valida se o horário está em intervalos de 30 minutos"""
    if value.minute not in [0, 30]:
        raise ValidationError('Agendamentos devem ser em intervalos de 30 minutos')
    return value