# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# Importar Celery apenas se estiver instalado
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except ImportError:
    # Celery não instalado - modo sem tarefas assíncronas
    pass

