from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Cupom
from .serializers import CupomSerializer, CreateCupomSerializer

class CupomAdminListView(generics.ListAPIView):
    """Listar todos os cupons (admin)"""
    serializer_class = CupomSerializer
    permission_classes = (IsAdminUser,)
    queryset = Cupom.objects.all().order_by('-created_at')

class CupomAdminCreateView(generics.CreateAPIView):
    """Criar novo cupom (admin)"""
    serializer_class = CreateCupomSerializer
    permission_classes = (IsAdminUser,)

class CupomAdminUpdateView(generics.UpdateAPIView):
    """Atualizar cupom (admin)"""
    serializer_class = CreateCupomSerializer
    permission_classes = (IsAdminUser,)
    queryset = Cupom.objects.all()

class CupomAdminDeleteView(generics.DestroyAPIView):
    """Deletar cupom (admin)"""
    permission_classes = (IsAdminUser,)
    queryset = Cupom.objects.all()
