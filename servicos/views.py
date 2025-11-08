from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Servico
from .serializers import ServicoSerializer


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache por 15 minutos
class ServicoListView(generics.ListAPIView):
    """Listar todos os serviços ativos

    Cache: 15 minutos
    """

    queryset = Servico.objects.filter(active=True)
    serializer_class = ServicoSerializer
    permission_classes = (AllowAny,)
