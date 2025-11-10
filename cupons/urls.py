from django.urls import path
from . import views

app_name = "cupons"

urlpatterns = [
    # Público
    path("", views.CupomListView.as_view(), name="list"),
    path("validate/", views.CupomValidateView.as_view(), name="validate"),
]
