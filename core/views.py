import logging

from django.http import JsonResponse
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
