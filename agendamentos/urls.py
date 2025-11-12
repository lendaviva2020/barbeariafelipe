from django.urls import path

from cupons.views import CupomValidateView

from . import views
from .upload_views import upload_appointment_photo
from .product_views import register_appointment_products, get_appointment_products

app_name = "agendamentos"

urlpatterns = [
    path("", views.AgendamentoListView.as_view(), name="list"),
    path("create/", views.AgendamentoCreateView.as_view(), name="create"),
    path("<int:pk>/cancel/", views.AgendamentoCancelView.as_view(), name="cancel"),
    path(
        "available-slots/", views.AvailableSlotsView.as_view(), name="available_slots"
    ),
    path("validate-cupom/", CupomValidateView.as_view(), name="validate_cupom"),
    
    # Upload de fotos
    path("<int:pk>/upload-photo/", upload_appointment_photo, name="upload_photo"),
    
    # Registro de produtos usados
    path("<int:pk>/register-products/", register_appointment_products, name="register_products"),
    path("<int:pk>/products/", get_appointment_products, name="get_products"),
]
