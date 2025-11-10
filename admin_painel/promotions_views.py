"""
Promotions Management Views
Extraído de Promotions.tsx (687 linhas)
"""

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Promotion
from .serializers import PromotionSerializer

class PromotionListView(generics.ListAPIView):
    """List all promotions with filter"""
    serializer_class = PromotionSerializer
    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        queryset = Promotion.objects.all().order_by('-created_at')
        
        # Filter by status
        filter_type = self.request.query_params.get('filter', 'all')
        now = timezone.now().date()
        
        if filter_type == 'active':
            queryset = queryset.filter(
                active=True,
                start_date__lte=now,
                end_date__gte=now
            )
        elif filter_type == 'inactive':
            queryset = queryset.filter(active=False)
        elif filter_type == 'expired':
            queryset = queryset.filter(
                active=True,
                end_date__lt=now
            )
        
        return queryset

class PromotionCreateView(generics.CreateAPIView):
    """Create new promotion"""
    serializer_class = PromotionSerializer
    permission_classes = (IsAdminUser,)

class PromotionUpdateView(generics.UpdateAPIView):
    """Update promotion"""
    serializer_class = PromotionSerializer
    permission_classes = (IsAdminUser,)
    queryset = Promotion.objects.all()

class PromotionDeleteView(generics.DestroyAPIView):
    """Delete promotion"""
    permission_classes = (IsAdminUser,)
    queryset = Promotion.objects.all()

class PromotionToggleView(generics.UpdateAPIView):
    """Toggle promotion active status"""
    permission_classes = (IsAdminUser,)
    queryset = Promotion.objects.all()
    
    def patch(self, request, pk):
        try:
            promotion = Promotion.objects.get(pk=pk)
            promotion.active = not promotion.active
            promotion.save()
            
            return Response({
                'message': f'Promoção {"ativada" if promotion.active else "desativada"}',
                'active': promotion.active
            })
        except Promotion.DoesNotExist:
            return Response(
                {'error': 'Promoção não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

