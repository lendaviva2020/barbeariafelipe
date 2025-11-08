from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Barbeiro
from .serializers import BarbeiroSerializer


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache por 15 minutos
class BarbeiroListView(generics.ListAPIView):
    """Listar todos os barbeiros ativos

    Cache: 15 minutos
    """

    queryset = Barbeiro.objects.filter(active=True).select_related("user")
    serializer_class = BarbeiroSerializer
    permission_classes = (AllowAny,)
