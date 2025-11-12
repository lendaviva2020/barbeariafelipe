from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from core.decorators import admin_required, admin_required_api
from django.db import connection
from django.conf import settings
import time


@admin_required
def performance_view(request):
    """Página de monitoramento de performance"""
    return render(request, 'admin/performance.html')


@admin_required_api
def performance_metrics_api(request):
    """API: Métricas de performance do sistema"""
    metrics = {
        'database': get_database_metrics(),
        'cache': get_cache_metrics(),
        'queries': get_query_metrics(),
        'system': get_system_metrics(),
    }
    
    return JsonResponse(metrics)


@admin_required_api
def clear_metrics_api(request):
    """API: Limpar métricas armazenadas"""
    # Limpar cache de métricas
    cache.delete_many([
        'perf_db_query_count',
        'perf_db_query_time',
        'perf_cache_hits',
        'perf_cache_misses',
    ])
    
    return JsonResponse({'success': True, 'message': 'Métricas limpas'})


def get_database_metrics():
    """Obter métricas do banco de dados"""
    # Queries executadas
    query_count = len(connection.queries) if settings.DEBUG else 0
    query_time = sum(float(q['time']) for q in connection.queries) if settings.DEBUG else 0
    
    return {
        'query_count': query_count,
        'query_time': round(query_time, 2),
        'avg_query_time': round(query_time / query_count, 3) if query_count > 0 else 0,
    }


def get_cache_metrics():
    """Obter métricas de cache"""
    try:
        # Testar cache
        test_key = 'cache_test_key'
        cache.set(test_key, 'test', 10)
        cache_working = cache.get(test_key) == 'test'
        cache.delete(test_key)
        
        # Métricas armazenadas
        hits = cache.get('perf_cache_hits', 0)
        misses = cache.get('perf_cache_misses', 0)
        total = hits + misses
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        return {
            'working': cache_working,
            'hits': hits,
            'misses': misses,
            'hit_rate': round(hit_rate, 1),
        }
    except Exception:
        return {
            'working': False,
            'hits': 0,
            'misses': 0,
            'hit_rate': 0,
        }


def get_query_metrics():
    """Obter métricas de queries lentas"""
    if not settings.DEBUG:
        return {'slow_queries': [], 'total_slow': 0}
    
    # Queries > 100ms
    slow_queries = [
        {
            'sql': q['sql'][:100] + '...' if len(q['sql']) > 100 else q['sql'],
            'time': float(q['time'])
        }
        for q in connection.queries
        if float(q['time']) > 0.1
    ]
    
    return {
        'slow_queries': slow_queries[:10],  # Top 10
        'total_slow': len(slow_queries),
    }


def get_system_metrics():
    """Obter métricas do sistema"""
    import sys
    import os
    
    metrics = {
        'python_version': sys.version.split()[0],
        'django_debug': settings.DEBUG,
        'database_engine': settings.DATABASES['default']['ENGINE'].split('.')[-1],
    }
    
    # Informações de memória (se disponível)
    try:
        import psutil
        process = psutil.Process(os.getpid())
        metrics['memory_mb'] = round(process.memory_info().rss / 1024 / 1024, 2)
        metrics['cpu_percent'] = round(process.cpu_percent(interval=0.1), 1)
    except ImportError:
        metrics['memory_mb'] = None
        metrics['cpu_percent'] = None
    
    return metrics

