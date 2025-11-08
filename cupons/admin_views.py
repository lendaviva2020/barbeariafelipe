import logging

from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cupom
from .serializers import CupomSerializer, ValidateCupomSerializer

logger = logging.getLogger(__name__)


class CupomAdminListCreateView(generics.ListCreateAPIView):
    """Listar e criar cupons (admin)"""

    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.query_params.get("active")
        filter_type = self.request.query_params.get("filter")

        if active is not None:
            queryset = queryset.filter(active=active.lower() == "true")

        # Filtro por status (active/expired)
        if filter_type == "active":
            queryset = [c for c in queryset if c.is_valid]
            return queryset
        elif filter_type == "expired":
            queryset = [c for c in queryset if not c.is_valid]
            return queryset

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Se é uma lista filtrada (não queryset)
        if isinstance(queryset, list):
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)


class CupomAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Recuperar, atualizar e deletar cupom (admin)"""

    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer
    permission_classes = (IsAdminUser,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Admin {request.user.email} deletou cupom: {instance.code}")
        return super().destroy(request, *args, **kwargs)


class ValidateCupomView(APIView):
    """Validar cupom antes de aplicar em agendamento"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ValidateCupomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"].upper()

        try:
            cupom = Cupom.objects.get(code=code)

            if not cupom.is_valid:
                return Response(
                    {"valid": False, "message": "Cupom inválido, expirado ou esgotado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response({"valid": True, "cupom": CupomSerializer(cupom).data})
        except Cupom.DoesNotExist:
            return Response(
                {"valid": False, "message": "Cupom não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
