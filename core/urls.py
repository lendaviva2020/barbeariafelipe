from django.urls import path
from .auth_views import auth_page, login_view, register_view, logout_view
from .views import (
    GoalListView,
    GoalCreateView,
    GoalUpdateView,
    GoalDeleteView,
    ReviewListView,
    ReviewCreateView,
    ReviewApproveView,
    WaitingListCreateView,
    WaitingListNotifyView,
    ProductListView,
    ProductLowStockView,
    SettingsView,
    CommissionListView,
    CommissionCreateView,
    CommissionMarkPaidView,
    CommissionSummaryView,
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
    LoyaltyMeView,
    LoyaltyRedeemView,
    LoyaltyHistoryView,
    RecurringListView,
    RecurringCreateView,
    RecurringUpdateView,
    RecurringDeleteView,
)
from .chat_views import (
    ChatSendMessageView,
    ChatHistoryView,
    AISettingsListCreateView,
    AISettingsDetailView,
    AIStatsView,
    ChatRequiringAttentionView,
    ChatMarkReadView,
    SendNotificationView,
    NotificationListView,
    NotificationDetailView,
)

app_name = 'core'

urlpatterns = [
    # Auth Enhanced
    path('auth/', auth_page, name='auth'),
    path('api/auth/login/', login_view, name='api_login'),
    path('api/auth/register/', register_view, name='api_register'),
    path('logout/', logout_view, name='logout'),
    
    # Goals
    path('goals/', GoalListView.as_view(), name='goal_list'),
    path('goals/create/', GoalCreateView.as_view(), name='goal_create'),
    path('goals/<int:pk>/', GoalUpdateView.as_view(), name='goal_update'),
    path('goals/<int:pk>/delete/', GoalDeleteView.as_view(), name='goal_delete'),
    
    # Reviews
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/approve/', ReviewApproveView.as_view(), name='review_approve'),
    
    # Waiting List
    path('waiting-list/', WaitingListCreateView.as_view(), name='waiting_list_create'),
    path('waiting-list/<int:pk>/notify/', WaitingListNotifyView.as_view(), name='waiting_list_notify'),
    
    # Products
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/low-stock/', ProductLowStockView.as_view(), name='product_low_stock'),
    
    # Commissions
    path('commissions/', CommissionListView.as_view(), name='commission_list'),
    path('commissions/create/', CommissionCreateView.as_view(), name='commission_create'),
    path('commissions/<int:pk>/mark-paid/', CommissionMarkPaidView.as_view(), name='commission_mark_paid'),
    path('commissions/summary/', CommissionSummaryView.as_view(), name='commission_summary'),
    
    # Suppliers
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # Loyalty
    path('loyalty/me/', LoyaltyMeView.as_view(), name='loyalty_me'),
    path('loyalty/redeem/', LoyaltyRedeemView.as_view(), name='loyalty_redeem'),
    path('loyalty/history/', LoyaltyHistoryView.as_view(), name='loyalty_history'),
    
    # Recurring Appointments
    path('recurring/', RecurringListView.as_view(), name='recurring_list'),
    path('recurring/create/', RecurringCreateView.as_view(), name='recurring_create'),
    path('recurring/<int:pk>/', RecurringUpdateView.as_view(), name='recurring_update'),
    path('recurring/<int:pk>/delete/', RecurringDeleteView.as_view(), name='recurring_delete'),
    
    # Settings
    path('settings/', SettingsView.as_view(), name='settings'),
    
    # Chat e IA
    path('api/chat/send/', ChatSendMessageView.as_view(), name='chat_send'),
    path('api/chat/history/<int:appointment_id>/', ChatHistoryView.as_view(), name='chat_history'),
    path('api/chat/attention/', ChatRequiringAttentionView.as_view(), name='chat_attention'),
    path('api/chat/<int:message_id>/read/', ChatMarkReadView.as_view(), name='chat_mark_read'),
    
    # Configurações de IA
    path('api/ai-settings/', AISettingsListCreateView.as_view(), name='ai_settings_list'),
    path('api/ai-settings/<int:pk>/', AISettingsDetailView.as_view(), name='ai_settings_detail'),
    path('api/ai/stats/', AIStatsView.as_view(), name='ai_stats'),
    
    # Notificações
    path('api/notifications/send/', SendNotificationView.as_view(), name='notification_send'),
    path('api/notifications/', NotificationListView.as_view(), name='notification_list'),
    path('api/notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),
]

