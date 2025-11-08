from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

from core.views import custom_403, custom_404, custom_500, health_check

# Error handlers
handler404 = custom_404
handler500 = custom_500
handler403 = custom_403

urlpatterns = [
    # Health check
    path("health/", health_check, name="health_check"),
    # Admin Django padrão
    path("django-admin/", admin.site.urls),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # API REST
    path("api/users/", include("users.urls")),
    path("api/agendamentos/", include("agendamentos.urls")),
    path("api/servicos/", include("servicos.urls")),
    path("api/barbeiros/", include("barbeiros.urls")),
    path("api/admin/", include("admin_painel.urls")),
    # Views HTML
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "servicos/",
        TemplateView.as_view(template_name="servicos.html"),
        name="servicos",
    ),
    path(
        "contato/", TemplateView.as_view(template_name="contato.html"), name="contato"
    ),
    path(
        "galeria/", TemplateView.as_view(template_name="galeria.html"), name="galeria"
    ),
    path("auth/", TemplateView.as_view(template_name="auth/login.html"), name="auth"),
    path(
        "agendar/",
        TemplateView.as_view(template_name="agendamentos/criar.html"),
        name="agendar",
    ),
    path("perfil/", TemplateView.as_view(template_name="perfil.html"), name="perfil"),
    path(
        "historico/",
        TemplateView.as_view(template_name="historico.html"),
        name="historico",
    ),
    path(
        "admin-painel/",
        TemplateView.as_view(template_name="admin/dashboard.html"),
        name="admin_painel",
    ),
]

# Servir arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Debug toolbar
    try:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass
