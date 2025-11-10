from django.urls import path
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

urlpatterns = [
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
]

