from django.urls import path

from . import views

app_name = "servicos"

urlpatterns = [
    path("", views.ServicoListView.as_view(), name="list"),
]
