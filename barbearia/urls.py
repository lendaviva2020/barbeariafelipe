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
    path("api/cupons/", include("cupons.urls")),
    path("api/", include("core.urls")),
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
        "goals/",
        TemplateView.as_view(template_name="goals.html"),
        name="goals",
    ),
    # Páginas de usuário
    path(
        "cupons/",
        TemplateView.as_view(template_name="cupons.html"),
        name="cupons",
    ),
    path(
        "reviews/",
        TemplateView.as_view(template_name="reviews.html"),
        name="reviews",
    ),
    path(
        "loyalty/",
        TemplateView.as_view(template_name="loyalty.html"),
        name="loyalty",
    ),
    path(
        "recurring/",
        TemplateView.as_view(template_name="recurring.html"),
        name="recurring",
    ),
    path(
        "settings/",
        TemplateView.as_view(template_name="settings.html"),
        name="settings",
    ),
    # Páginas de barbeiro/admin
    path(
        "commissions/",
        TemplateView.as_view(template_name="commissions.html"),
        name="commissions",
    ),
    path(
        "inventory/",
        TemplateView.as_view(template_name="inventory.html"),
        name="inventory",
    ),
    path(
        "suppliers/",
        TemplateView.as_view(template_name="suppliers.html"),
        name="suppliers",
    ),
    # Admin Panel
    path(
        "admin-painel/",
        TemplateView.as_view(template_name="admin/dashboard.html"),
        name="admin_painel",
    ),
    path(
        "admin-painel/appointments/",
        TemplateView.as_view(template_name="admin/appointments.html"),
        name="admin_appointments",
    ),
    path(
        "admin-painel/barbers/",
        TemplateView.as_view(template_name="admin/barbers.html"),
        name="admin_barbers",
    ),
    path(
        "admin-painel/services/",
        TemplateView.as_view(template_name="admin/services.html"),
        name="admin_services",
    ),
    path(
        "admin-painel/coupons/",
        TemplateView.as_view(template_name="admin/coupons.html"),
        name="admin_coupons",
    ),
    path(
        "admin-painel/users/",
        TemplateView.as_view(template_name="admin/users.html"),
        name="admin_users",
    ),
    path(
        "admin-painel/reports/",
        TemplateView.as_view(template_name="admin/reports.html"),
        name="admin_reports",
    ),
    path(
        "admin-painel/waiting-list/",
        TemplateView.as_view(template_name="admin/waiting-list.html"),
        name="admin_waiting_list",
    ),
    path(
        "admin-painel/audit-logs/",
        TemplateView.as_view(template_name="admin/audit-logs.html"),
        name="admin_audit_logs",
    ),
    path(
        "admin-painel/performance/",
        TemplateView.as_view(template_name="admin/performance.html"),
        name="admin_performance",
    ),
    path(
        "admin-painel/promotions/",
        TemplateView.as_view(template_name="admin/promotions.html"),
        name="admin_promotions",
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
