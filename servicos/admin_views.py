import logging

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Servico
from .serializers import ServicoSerializer

logger = logging.getLogger(__name__)


class ServicoAdminListCreateView(generics.ListCreateAPIView):
    """Listar e criar serviços (admin)"""

    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.query_params.get("active")

        if active is not None:
            queryset = queryset.filter(active=active.lower() == "true")

        return queryset.order_by("-created_at")


class ServicoAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Recuperar, atualizar e deletar serviço (admin)"""

    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    permission_classes = (IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Admin {request.user.email} deletou serviço: {instance.name}")
        return super().destroy(request, *args, **kwargs)
