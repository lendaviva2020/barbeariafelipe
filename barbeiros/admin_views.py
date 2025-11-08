import logging

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Barbeiro
from .serializers import BarbeiroSerializer

logger = logging.getLogger(__name__)


class BarbeiroAdminListCreateView(generics.ListCreateAPIView):
    """Listar e criar barbeiros (admin)"""

    queryset = Barbeiro.objects.all()
    serializer_class = BarbeiroSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.query_params.get("active")

        if active is not None:
            queryset = queryset.filter(active=active.lower() == "true")

        return queryset.order_by("-created_at")


class BarbeiroAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Recuperar, atualizar e deletar barbeiro (admin)"""

    queryset = Barbeiro.objects.all()
    serializer_class = BarbeiroSerializer
    permission_classes = (IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Admin {request.user.email} deletou barbeiro: {instance.name}")
        return super().destroy(request, *args, **kwargs)
