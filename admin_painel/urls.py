from django.urls import path

from barbeiros.admin_views import (BarbeiroAdminDetailView,
                                   BarbeiroAdminListCreateView)
from cupons.admin_views import CupomAdminDetailView, CupomAdminListCreateView
from servicos.admin_views import (ServicoAdminDetailView,
                                  ServicoAdminListCreateView)

from . import views
from .users_views import UsersListView
from .report_views import (
    ReportsRevenueView,
    ReportsServicesView,
    ReportsBarbersPerformanceView,
    ExportPDFView,
    ExportExcelView
)
from .promotions_views import (
    PromotionListView,
    PromotionCreateView,
    PromotionUpdateView,
    PromotionDeleteView,
    PromotionToggleView
)

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
    
    # Users
    path("users/", views.UsersListView.as_view(), name="users"),
    
    # Reports
    path("reports/revenue/", ReportsRevenueView.as_view(), name="reports_revenue"),
    path("reports/services/", ReportsServicesView.as_view(), name="reports_services"),
    path("reports/barbers/", ReportsBarbersPerformanceView.as_view(), name="reports_barbers"),
    path("export-pdf/", ExportPDFView.as_view(), name="export_pdf"),
    path("export-excel/", ExportExcelView.as_view(), name="export_excel"),
    
    # Promotions
    path("promotions/", PromotionListView.as_view(), name="promotions_list"),
    path("promotions/create/", PromotionCreateView.as_view(), name="promotions_create"),
    path("promotions/<int:pk>/", PromotionUpdateView.as_view(), name="promotions_update"),
    path("promotions/<int:pk>/delete/", PromotionDeleteView.as_view(), name="promotions_delete"),
    path("promotions/<int:pk>/toggle/", PromotionToggleView.as_view(), name="promotions_toggle"),
]
