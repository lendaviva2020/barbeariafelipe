from django.urls import path

from cupons.views import CupomValidateView

from . import views

app_name = "agendamentos"

urlpatterns = [
    path("", views.AgendamentoListView.as_view(), name="list"),
    path("create/", views.AgendamentoCreateView.as_view(), name="create"),
    path("<int:pk>/cancel/", views.AgendamentoCancelView.as_view(), name="cancel"),
    path(
        "available-slots/", views.AvailableSlotsView.as_view(), name="available_slots"
    ),
    path("validate-cupom/", CupomValidateView.as_view(), name="validate_cupom"),
]
