from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Servico
from .serializers import ServicoSerializer

class ServicoAdminCreateView(generics.CreateAPIView):
    """Criar novo serviço (admin)"""
    serializer_class = ServicoSerializer
    permission_classes = (IsAdminUser,)

class ServicoAdminUpdateView(generics.UpdateAPIView):
    """Atualizar serviço (admin)"""
    serializer_class = ServicoSerializer
    permission_classes = (IsAdminUser,)
    queryset = Servico.objects.all()

class ServicoAdminDeleteView(generics.DestroyAPIView):
    """Deletar serviço (admin)"""
    permission_classes = (IsAdminUser,)
    queryset = Servico.objects.all()
