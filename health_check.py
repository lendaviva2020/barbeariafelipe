"""
Health Check Endpoint
Adicionar em core/views.py ou criar arquivo separado
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Endpoint de health check para monitoramento
    URL: /health/
    """
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status['checks']['database'] = 'ok'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = f'error: {str(e)}'
        logger.error(f"Health check - Database error: {e}")
    
    # Check Redis/Cache
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = 'ok'
        else:
            raise Exception("Cache set/get failed")
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['cache'] = f'error: {str(e)}'
        logger.error(f"Health check - Cache error: {e}")
    
    # Check Celery (opcional - pode ser lento)
    try:
        from celery import current_app
        inspect = current_app.control.inspect()
        stats = inspect.stats()
        
        if stats:
            health_status['checks']['celery'] = 'ok'
        else:
            health_status['checks']['celery'] = 'no workers'
    except Exception as e:
        health_status['checks']['celery'] = f'error: {str(e)}'
        logger.warning(f"Health check - Celery error: {e}")
    
    # Informações do sistema
    health_status['info'] = {
        'debug': settings.DEBUG,
        'version': '1.0.0',
        'python': '3.11'
    }
    
    # Status code baseado na saúde
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return JsonResponse(health_status, status=status_code)

