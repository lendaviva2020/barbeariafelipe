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
    Decorator que requer que o usuário seja admin
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Autenticação necessária'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.role != 'admin':
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
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Autenticação necessária'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.user.role not in ['barber', 'admin']:
            return JsonResponse({
                'error': 'Acesso negado',
                'details': 'Apenas barbeiros e administradores podem acessar este recurso'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view


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

