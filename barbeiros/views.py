from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Barbeiro
from .serializers import BarbeiroSerializer


class BarbeiroListView(generics.ListAPIView):
    """Listar todos os barbeiros ativos"""

    queryset = Barbeiro.objects.filter(active=True)
    serializer_class = BarbeiroSerializer
    permission_classes = (AllowAny,)
