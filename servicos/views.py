from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Servico
from .serializers import ServicoSerializer


class ServicoListView(generics.ListAPIView):
    """Listar todos os serviços ativos"""

    queryset = Servico.objects.filter(active=True)
    serializer_class = ServicoSerializer
    permission_classes = (AllowAny,)
