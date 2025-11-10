from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Cupom
from .serializers import CupomSerializer, ValidateCupomSerializer

class CupomListView(generics.ListAPIView):
    """Listar cupons ativos (público)"""
    serializer_class = CupomSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        # Retornar apenas cupons ativos e não expirados
        return Cupom.objects.filter(
            active=True,
            expiry_date__gte=timezone.now().date()
        ).exclude(
            max_uses__lte=models.F('current_uses')
        ).order_by('-created_at')

class CupomValidateView(APIView):
    """Validar cupom (usado no booking)"""
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = ValidateCupomSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Código inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        code = serializer.validated_data['code']
        
        try:
            cupom = Cupom.objects.get(code=code, active=True)
            
            # Verificar expiração
            if cupom.expiry_date and cupom.expiry_date < timezone.now().date():
                return Response(
                    {'error': 'Cupom expirado'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar limite de uso
            if cupom.max_uses and cupom.current_uses >= cupom.max_uses:
                return Response(
                    {'error': 'Cupom esgotado'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Cupom válido
            return Response({
                'id': cupom.id,
                'code': cupom.code,
                'discount': float(cupom.discount),
                'discount_type': cupom.discount_type,
                'description': cupom.description,
                'valid': True
            })
            
        except Cupom.DoesNotExist:
            return Response(
                {'error': 'Cupom não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Import django.db.models for F expressions
from django.db import models
