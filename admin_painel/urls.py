from django.urls import path

from barbeiros.admin_views import (BarbeiroAdminDetailView,
                                   BarbeiroAdminListCreateView)
from cupons.admin_views import CupomAdminDetailView, CupomAdminListCreateView
from servicos.admin_views import (ServicoAdminDetailView,
                                  ServicoAdminListCreateView)

from . import views

app_name = "admin_painel"

urlpatterns = [
    # Dashboard
    path(
        "dashboard/stats/", views.DashboardStatsView.as_view(), name="dashboard_stats"
    ),
    # Agendamentos
    path("agendamentos/", views.AgendamentosAdminView.as_view(), name="agendamentos"),
    path(
        "agendamentos/<int:pk>/status/",
        views.UpdateAgendamentoStatusView.as_view(),
        name="update_status",
    ),
    # Serviços CRUD
    path(
        "servicos/", ServicoAdminListCreateView.as_view(), name="servicos_list_create"
    ),
    path(
        "servicos/<int:pk>/", ServicoAdminDetailView.as_view(), name="servicos_detail"
    ),
    # Barbeiros CRUD
    path(
        "barbeiros/",
        BarbeiroAdminListCreateView.as_view(),
        name="barbeiros_list_create",
    ),
    path(
        "barbeiros/<int:pk>/",
        BarbeiroAdminDetailView.as_view(),
        name="barbeiros_detail",
    ),
    # Cupons CRUD
    path("cupons/", CupomAdminListCreateView.as_view(), name="cupons_list_create"),
    path("cupons/<int:pk>/", CupomAdminDetailView.as_view(), name="cupons_detail"),
]
