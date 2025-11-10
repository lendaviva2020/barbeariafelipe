from django.urls import path
from .views import (
    CupomListView, 
    CupomValidateView
)
from .admin_views import (
    CupomAdminListView,
    CupomAdminCreateView,
    CupomAdminUpdateView,
    CupomAdminDeleteView
)

urlpatterns = [
    # Public endpoints
    path('', CupomListView.as_view(), name='cupom_list'),
    path('validate/', CupomValidateView.as_view(), name='cupom_validate'),
    
    # Admin endpoints
    path('admin/', CupomAdminListView.as_view(), name='cupom_admin_list'),
    path('admin/create/', CupomAdminCreateView.as_view(), name='cupom_admin_create'),
    path('admin/<int:pk>/', CupomAdminUpdateView.as_view(), name='cupom_admin_update'),
    path('admin/<int:pk>/delete/', CupomAdminDeleteView.as_view(), name='cupom_admin_delete'),
]

