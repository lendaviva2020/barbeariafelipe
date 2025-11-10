"""
Middleware personalizado para a aplicação
"""
import logging
import traceback
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    """
    Middleware para tratamento centralizado de erros
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Processa exceções não tratadas
        """
        # Log do erro
        logger.error(
            f"Erro não tratado: {str(exception)}",
            exc_info=True,
            extra={
                'request_path': request.path,
                'request_method': request.method,
                'user': request.user.id if request.user.is_authenticated else 'Anonymous'
            }
        )

        # Resposta para APIs REST
        if request.path.startswith('/api/'):
            if isinstance(exception, ValidationError):
                return JsonResponse({
                    'error': 'Erro de validação',
                    'details': exception.messages if hasattr(exception, 'messages') else str(exception)
                }, status=status.HTTP_400_BAD_REQUEST)
            
            elif isinstance(exception, PermissionDenied):
                return JsonResponse({
                    'error': 'Acesso negado',
                    'details': 'Você não tem permissão para acessar este recurso'
                }, status=status.HTTP_403_FORBIDDEN)
            
            elif isinstance(exception, APIException):
                return JsonResponse({
                    'error': str(exception.detail) if hasattr(exception, 'detail') else 'Erro na API',
                    'status_code': exception.status_code if hasattr(exception, 'status_code') else 500
                }, status=exception.status_code if hasattr(exception, 'status_code') else 500)
            
            else:
                # Erro genérico
                return JsonResponse({
                    'error': 'Erro interno do servidor',
                    'details': str(exception) if settings.DEBUG else 'Ocorreu um erro inesperado'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Deixa o Django lidar com erros não-API
        return None


class RequestLoggingMiddleware:
    """
    Middleware para logging de requisições
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log da requisição
        logger.info(
            f"{request.method} {request.path}",
            extra={
                'user': request.user.id if request.user.is_authenticated else 'Anonymous',
                'ip': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')
            }
        )

        response = self.get_response(request)

        # Log da resposta (apenas erros)
        if response.status_code >= 400:
            logger.warning(
                f"Response {response.status_code} for {request.method} {request.path}",
                extra={
                    'status_code': response.status_code,
                    'user': request.user.id if request.user.is_authenticated else 'Anonymous'
                }
            )

        return response

    def get_client_ip(self, request):
        """Obtém o IP real do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware:
    """
    Middleware para adicionar headers de segurança
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Adiciona headers de segurança
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy
        if not settings.DEBUG:
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://api.whatsapp.com;"
            )
        
        return response


# Importar settings para usar DEBUG
from django.conf import settings

