import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint para monitoramento e deploy
    """
    try:
        # Verificar conexão com o banco de dados
        from django.db import connection

        connection.ensure_connection()

        return JsonResponse({"status": "healthy", "database": "connected"})
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JsonResponse({"status": "unhealthy", "error": str(e)}, status=503)


def custom_404(request, exception=None):
    """Handler customizado para erro 404"""
    from django.http import HttpResponse

    try:
        return render(request, "errors/404.html", status=404)
    except Exception:
        return HttpResponse("<h1>404 - Página não encontrada</h1>", status=404)


def custom_500(request):
    """Handler customizado para erro 500"""
    from django.http import HttpResponse

    try:
        return render(request, "errors/500.html", status=500)
    except Exception:
        return HttpResponse("<h1>500 - Erro interno do servidor</h1>", status=500)


def custom_403(request, exception=None):
    """Handler customizado para erro 403"""
    from django.http import HttpResponse

    try:
        return render(request, "errors/403.html", status=403)
    except Exception:
        return HttpResponse("<h1>403 - Acesso negado</h1>", status=403)
