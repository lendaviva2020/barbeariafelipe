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
    serializer_class = ServicoSerializer
    permission_classes = (AllowAny,)
    pagination_class = None  # Desabilitar paginação para retornar array direto
    
    def get_queryset(self):
        """Retorna serviços ativos, tratando campos active/is_active"""
        try:
            # Tentar filtrar por active=True primeiro
            queryset = Servico.objects.filter(active=True)
            if queryset.exists():
                return queryset
        except Exception:
            pass
        
        try:
            # Se não funcionar, tentar is_active=True
            queryset = Servico.objects.filter(is_active=True)
            if queryset.exists():
                return queryset
        except Exception:
            pass
        
        # Se nenhum campo de ativo existir, retornar todos
        return Servico.objects.all()
    
    def list(self, request, *args, **kwargs):
        """Override para tratar erros"""
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            from rest_framework.response import Response
            from rest_framework import status
            return Response({
                'error': str(e),
                'detail': 'Erro ao carregar serviços'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
