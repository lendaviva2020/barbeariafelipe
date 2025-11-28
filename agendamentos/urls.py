from django.urls import path

from cupons.views import CupomValidateView

from . import views
from .upload_views import upload_appointment_photo
from .product_views import register_appointment_products, get_appointment_products
from .booking_views import (
    services_list, barbers_list, available_slots, 
    validate_coupon, create_booking
)

app_name = "agendamentos"

urlpatterns = [
    # APIs para o sistema de booking
    path("services/", services_list, name="api_services"),
    path("barbers/", barbers_list, name="api_barbers"),
    path("available-slots/", available_slots, name="api_available_slots"),
    path("validate-coupon/", validate_coupon, name="api_validate_coupon"),
    path("bookings/", create_booking, name="api_create_booking"),
    
    # APIs existentes (mantidas para compatibilidade)
    path("", views.AgendamentoListView.as_view(), name="list"),
    path("create/", views.AgendamentoCreateView.as_view(), name="create"),
    path("<int:pk>/cancel/", views.AgendamentoCancelView.as_view(), name="cancel"),
    path("validate-cupom/", CupomValidateView.as_view(), name="validate_cupom"),
    
    # Upload de fotos
    path("<int:pk>/upload-photo/", upload_appointment_photo, name="upload_photo"),
    
    # Registro de produtos usados
    path("<int:pk>/register-products/", register_appointment_products, name="register_products"),
    path("<int:pk>/products/", get_appointment_products, name="get_products"),
]
