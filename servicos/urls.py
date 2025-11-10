from django.urls import path

from . import views
from .upload_views import UploadServiceImageView

app_name = "servicos"

urlpatterns = [
    path("", views.ServicoListView.as_view(), name="list"),
    path("<int:service_id>/upload-image/", UploadServiceImageView.as_view(), name="upload_image"),
]
