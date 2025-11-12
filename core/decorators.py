"""
Decorators personalizados para a aplicação
"""
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
import hashlib


def rate_limit(key_prefix='', limit=10, period=60):
    """
    Decorator para rate limiting simples baseado em cache
    
    Args:
        key_prefix: Prefixo da chave de cache
        limit: Número máximo de requisições
        period: Período em segundos
    
    Usage:
        @rate_limit(key_prefix='login', limit=5, period=300)
        def login_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Identifica o cliente (IP ou usuário)
            if request.user.is_authenticated:
                identifier = f"user_{request.user.id}"
            else:
                identifier = get_client_ip(request)
            
            # Cria a chave de cache
            cache_key = f"rate_limit_{key_prefix}_{identifier}"
            
            # Verifica o número de requisições
            attempts = cache.get(cache_key, 0)
            
            if attempts >= limit:
                return JsonResponse({
                    'error': 'Limite de requisições excedido',
                    'details': f'Você atingiu o limite de {limit} requisições. Tente novamente em {period} segundos.'
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # Incrementa o contador
            cache.set(cache_key, attempts + 1, period)
            
            # Executa a view
            response = view_func(request, *args, **kwargs)
            
            # Adiciona headers de rate limit
            response['X-RateLimit-Limit'] = str(limit)
            response['X-RateLimit-Remaining'] = str(max(0, limit - attempts - 1))
            response['X-RateLimit-Reset'] = str(period)
            
            return response
        
        return wrapped_view
    return decorator


def admin_required(view_func):
    """
    Decorator que requer que o usuário seja admin (staff)
    Redireciona para login se não autenticado, ou para home se não for staff
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar autenticado para acessar esta área.')
            return redirect('users:login')
        
        if not request.user.is_staff:
            messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta área.')
            return redirect('core:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view


def admin_required_api(view_func):
    """
    Decorator que requer admin para APIs (retorna JSON)
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Autenticação necessária'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not request.user.is_staff:
            return JsonResponse({
                'error': 'Acesso negado',
                'details': 'Apenas administradores podem acessar este recurso'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view


def barber_or_admin_required(view_func):
    """
    Decorator que requer que o usuário seja barbeiro ou admin
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.contrib import messages
        from barbeiros.models import Barbeiro
        
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar autenticado.')
            return redirect('users:login')
        
        # Verifica se é staff ou se é um barbeiro
        is_barber = Barbeiro.objects.filter(user=request.user, active=True).exists()
        
        if not (request.user.is_staff or is_barber):
            messages.error(request, 'Acesso negado. Apenas barbeiros e administradores podem acessar.')
            return redirect('core:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view


def role_required(allowed_roles):
    """
    Decorator que requer roles específicas
    
    Usage:
        @role_required(['admin', 'barber'])
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            from django.shortcuts import redirect
            from django.contrib import messages
            from barbeiros.models import Barbeiro
            
            if not request.user.is_authenticated:
                messages.error(request, 'Autenticação necessária.')
                return redirect('users:login')
            
            user_roles = []
            if request.user.is_staff or request.user.is_superuser:
                user_roles.append('admin')
            if Barbeiro.objects.filter(user=request.user, active=True).exists():
                user_roles.append('barber')
            if not user_roles:
                user_roles.append('user')
            
            if not any(role in allowed_roles for role in user_roles):
                messages.error(request, 'Você não tem permissão para acessar este recurso.')
                return redirect('core:home')
            
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    return decorator


def log_action(action_type):
    """
    Decorator para registrar ações em audit log
    
    Usage:
        @log_action('appointment_created')
        def create_appointment(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            import logging
            logger = logging.getLogger('barbearia')
            
            # Executa a view
            response = view_func(request, *args, **kwargs)
            
            # Log apenas se for sucesso (2xx)
            if 200 <= response.status_code < 300:
                logger.info(
                    f"Action: {action_type}",
                    extra={
                        'action': action_type,
                        'user': request.user.id if request.user.is_authenticated else None,
                        'ip': get_client_ip(request),
                        'path': request.path,
                        'method': request.method
                    }
                )
            
            return response
        
        return wrapped_view
    return decorator


def get_client_ip(request):
    """
    Obtém o IP real do cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def cache_response(timeout=300, key_prefix=''):
    """
    Decorator para cachear respostas de views
    
    Args:
        timeout: Tempo de cache em segundos (padrão: 5 minutos)
        key_prefix: Prefixo da chave de cache
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Gera chave de cache baseada na URL e parâmetros
            cache_key = f"{key_prefix}_{request.path}_{hash(str(request.GET))}"
            
            # Tenta obter do cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # Executa a view
            response = view_func(request, *args, **kwargs)
            
            # Cacheia apenas respostas de sucesso
            if 200 <= response.status_code < 300:
                cache.set(cache_key, response, timeout)
            
            return response
        
        return wrapped_view
    return decorator


def require_admin(view_func):
    """
    Decorator que verifica se usuário tem role 'admin'
    Para uso em views baseadas em função
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Autenticação necessária'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not (request.user.role == 'admin' or request.user.is_staff):
            return JsonResponse({
                'error': 'Acesso negado',
                'details': 'Apenas administradores podem acessar este recurso'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view


def require_barber_or_admin(view_func):
    """
    Decorator que verifica se usuário é barbeiro ou admin
    Para uso em views baseadas em função
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Autenticação necessária'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        is_admin = request.user.role == 'admin' or request.user.is_staff
        is_barber = request.user.role == 'barber'
        
        if not (is_admin or is_barber):
            return JsonResponse({
                'error': 'Acesso negado',
                'details': 'Apenas barbeiros e administradores podem acessar este recurso'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view


def require_appointment_owner(view_func):
    """
    Decorator que verifica se o usuário é dono do agendamento
    Espera que view_func receba appointment_id como parâmetro
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        from agendamentos.models import Agendamento
        
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Autenticação necessária'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Tentar obter appointment_id dos kwargs ou do request
        appointment_id = kwargs.get('appointment_id') or kwargs.get('pk')
        if not appointment_id and request.method == 'POST':
            import json
            try:
                data = json.loads(request.body)
                appointment_id = data.get('appointment_id')
            except:
                pass
        
        if not appointment_id:
            return JsonResponse({
                'error': 'ID do agendamento não fornecido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            appointment = Agendamento.objects.get(id=appointment_id)
        except Agendamento.DoesNotExist:
            return JsonResponse({
                'error': 'Agendamento não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar se é o dono, barbeiro ou admin
        is_owner = appointment.user == request.user
        is_barber = hasattr(request.user, 'barbeiro') and appointment.barber == request.user.barbeiro
        is_admin = request.user.role == 'admin' or request.user.is_staff
        
        if not (is_owner or is_barber or is_admin):
            return JsonResponse({
                'error': 'Acesso negado',
                'details': 'Você não tem permissão para acessar este agendamento'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Adicionar appointment ao request para uso na view
        request.appointment = appointment
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view


def check_rate_limit(key_prefix='api', limit=60, period=60):
    """
    Decorator para rate limiting em APIs sensíveis
    Similar ao rate_limit mas com configurações específicas para APIs
    
    Args:
        key_prefix: Prefixo da chave
        limit: Número de requisições (padrão: 60)
        period: Período em segundos (padrão: 60 = 1 req/segundo)
    """
    return rate_limit(key_prefix=key_prefix, limit=limit, period=period)
