from django.urls import path

from barbeiros.admin_views import (BarbeiroAdminDetailView,
                                   BarbeiroAdminListCreateView)
from cupons.admin_views import (
    CupomAdminListView, 
    CupomAdminCreateView,
    CupomAdminUpdateView,
    CupomAdminDeleteView
)
from servicos.admin_views import (
    ServicoAdminCreateView,
    ServicoAdminUpdateView,
    ServicoAdminDeleteView
)
from servicos.views import ServicoListView

from . import views
from .dashboard_views import (
    dashboard_view,
    dashboard_stats_api,
    dashboard_revenue_chart_api,
    dashboard_services_chart_api,
    dashboard_barber_performance_api,
    dashboard_status_distribution_api,
)
from .appointments_views import (
    appointments_view,
    appointments_api,
    confirm_appointment_api,
    complete_appointment_api,
    cancel_appointment_api,
)
from .users_admin_views import (
    users_view,
    users_list_api,
    toggle_admin_api,
    toggle_active_api,
)
from .audit_views import (
    audit_logs_view,
    audit_logs_api,
    audit_logs_tables_api,
    audit_logs_export_csv,
)
from .waiting_list_views import (
    waiting_list_view,
    waiting_list_api,
    notify_customer_api,
    update_status_api,
    remove_entry_api,
)
from .performance_views import (
    performance_view,
    performance_metrics_api,
    clear_metrics_api,
)
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
    path("dashboard/", dashboard_view, name="dashboard"),
    path("api/dashboard/stats/", dashboard_stats_api, name="dashboard_stats_api"),
    path("api/dashboard/revenue/", dashboard_revenue_chart_api, name="dashboard_revenue_api"),
    path("api/dashboard/services/", dashboard_services_chart_api, name="dashboard_services_api"),
    path("api/dashboard/barbers/", dashboard_barber_performance_api, name="dashboard_barbers_api"),
    path("api/dashboard/status/", dashboard_status_distribution_api, name="dashboard_status_api"),
    
    # Agendamentos
    path("appointments/", appointments_view, name="appointments"),
    path("api/appointments/", appointments_api, name="appointments_api"),
    path("api/appointments/<int:pk>/confirm/", confirm_appointment_api, name="appointment_confirm"),
    path("api/appointments/<int:pk>/complete/", complete_appointment_api, name="appointment_complete"),
    path("api/appointments/<int:pk>/cancel/", cancel_appointment_api, name="appointment_cancel"),
    
    # Serviços CRUD
    path("services/", ServicoListView.as_view(), name="services"),
    path("api/services/create/", ServicoAdminCreateView.as_view(), name="service_create"),
    path("api/services/<int:pk>/", ServicoAdminUpdateView.as_view(), name="service_update"),
    path("api/services/<int:pk>/delete/", ServicoAdminDeleteView.as_view(), name="service_delete"),
    
    # Barbeiros CRUD
    path("barbers/", BarbeiroAdminListCreateView.as_view(), name="barbers"),
    path("api/barbers/", BarbeiroAdminListCreateView.as_view(), name="barbers_list"),
    path("api/barbers/<int:pk>/", BarbeiroAdminDetailView.as_view(), name="barber_detail"),
    
    # Cupons CRUD
    path("coupons/", CupomAdminListView.as_view(), name="coupons"),
    path("api/coupons/", CupomAdminListView.as_view(), name="coupons_list"),
    path("api/coupons/create/", CupomAdminCreateView.as_view(), name="coupon_create"),
    path("api/coupons/<int:pk>/", CupomAdminUpdateView.as_view(), name="coupon_update"),
    path("api/coupons/<int:pk>/delete/", CupomAdminDeleteView.as_view(), name="coupon_delete"),
    
    # Users
    path("users/", users_view, name="users"),
    path("api/users/", users_list_api, name="users_api"),
    path("api/users/<int:pk>/toggle-admin/", toggle_admin_api, name="user_toggle_admin"),
    path("api/users/<int:pk>/toggle-active/", toggle_active_api, name="user_toggle_active"),
    
    # Reports
    path("reports/", ReportsRevenueView.as_view(), name="reports"),
    path("api/reports/revenue/", ReportsRevenueView.as_view(), name="reports_revenue"),
    path("api/reports/services/", ReportsServicesView.as_view(), name="reports_services"),
    path("api/reports/barbers/", ReportsBarbersPerformanceView.as_view(), name="reports_barbers"),
    path("api/export-pdf/", ExportPDFView.as_view(), name="export_pdf"),
    path("api/export-excel/", ExportExcelView.as_view(), name="export_excel"),
    
    # Promotions
    path("promotions/", PromotionListView.as_view(), name="promotions_list"),
    path("api/promotions/create/", PromotionCreateView.as_view(), name="promotions_create"),
    path("api/promotions/<int:pk>/", PromotionUpdateView.as_view(), name="promotions_update"),
    path("api/promotions/<int:pk>/delete/", PromotionDeleteView.as_view(), name="promotions_delete"),
    path("api/promotions/<int:pk>/toggle/", PromotionToggleView.as_view(), name="promotions_toggle"),
    
    # Waiting List
    path("waiting-list/", waiting_list_view, name="waiting_list"),
    path("api/waiting-list/", waiting_list_api, name="waiting_list_api"),
    path("api/waiting-list/<int:pk>/notify/", notify_customer_api, name="waiting_list_notify"),
    path("api/waiting-list/<int:pk>/status/", update_status_api, name="waiting_list_update_status"),
    path("api/waiting-list/<int:pk>/remove/", remove_entry_api, name="waiting_list_remove"),
    
    # Audit Logs
    path("audit-logs/", audit_logs_view, name="audit_logs"),
    path("api/audit-logs/", audit_logs_api, name="audit_logs_api"),
    path("api/audit-logs/tables/", audit_logs_tables_api, name="audit_logs_tables"),
    path("api/audit-logs/export/", audit_logs_export_csv, name="audit_logs_export"),
    
    # Performance
    path("performance/", performance_view, name="performance"),
    path("api/performance/metrics/", performance_metrics_api, name="performance_metrics"),
    path("api/performance/clear/", clear_metrics_api, name="performance_clear"),
]
