from django.urls import path

from . import views

app_name = "barbeiros"

urlpatterns = [
    path("", views.BarbeiroListView.as_view(), name="list"),
]
