from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import datetime
from .models import (
    Goal, Review, WaitingList, Product, BarbershopSettings,
    Commission, Supplier, LoyaltyProgram, RecurringAppointment
)
from .serializers import (
    GoalSerializer, ReviewSerializer, CreateReviewSerializer,
    WaitingListSerializer, ProductSerializer, BarbershopSettingsSerializer,
    CommissionSerializer, SupplierSerializer, LoyaltyProgramSerializer,
    RecurringAppointmentSerializer
)

# Error handlers
def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)

def custom_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def health_check(request):
    return JsonResponse({'status': 'ok'})

# Goals Views
class GoalListView(generics.ListAPIView):
    """List all goals"""
    serializer_class = GoalSerializer
    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        queryset = Goal.objects.all().select_related('barber')
        
        # Filter by barber if provided
        barber_id = self.request.query_params.get('barber_id')
        if barber_id:
            queryset = queryset.filter(barber_id=barber_id)
        
        return queryset.order_by('-created_at')

class GoalCreateView(generics.CreateAPIView):
    """Create new goal"""
    serializer_class = GoalSerializer
    permission_classes = (IsAdminUser,)

class GoalUpdateView(generics.UpdateAPIView):
    """Update goal"""
    serializer_class = GoalSerializer
    permission_classes = (IsAdminUser,)
    queryset = Goal.objects.all()

class GoalDeleteView(generics.DestroyAPIView):
    """Delete goal"""
    permission_classes = (IsAdminUser,)
    queryset = Goal.objects.all()

# Reviews Views
class ReviewListView(generics.ListAPIView):
    """List approved reviews (public)"""
    serializer_class = ReviewSerializer
    permission_classes = ()
    
    def get_queryset(self):
        return Review.objects.filter(is_approved=True).select_related(
            'user', 'barber', 'service'
        ).order_by('-created_at')

class ReviewCreateView(generics.CreateAPIView):
    """Create review (authenticated users)"""
    serializer_class = CreateReviewSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewApproveView(APIView):
    """Approve review (admin only)"""
    permission_classes = (IsAdminUser,)
    
    def post(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.is_approved = True
            review.save()
            return Response({'message': 'Review aprovado'})
        except Review.DoesNotExist:
            return Response(
                {'error': 'Review não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

# Waiting List Views
class WaitingListCreateView(generics.CreateAPIView):
    """Add to waiting list"""
    serializer_class = WaitingListSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WaitingListNotifyView(APIView):
    """Notify waiting list user (admin)"""
    permission_classes = (IsAdminUser,)
    
    def post(self, request, pk):
        try:
            waiting = WaitingList.objects.get(pk=pk)
            waiting.notified = True
            waiting.save()
            
            # TODO: Send notification (WhatsApp/Email)
            
            return Response({'message': 'Notificação enviada'})
        except WaitingList.DoesNotExist:
            return Response(
                {'error': 'Registro não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

# Products Views
class ProductListView(generics.ListAPIView):
    """List products (admin)"""
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    queryset = Product.objects.all().order_by('name')

class ProductLowStockView(generics.ListAPIView):
    """List low stock products (admin)"""
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    
    def get_queryset(self):
        return Product.objects.filter(
            stock_quantity__lte=models.F('min_stock_level')
        ).order_by('stock_quantity')

# Settings View
class SettingsView(APIView):
    """Get/Update barbershop settings"""
    permission_classes = (IsAdminUser,)
    
    def get(self, request):
        settings = BarbershopSettings.objects.first()
        if not settings:
            settings = BarbershopSettings.objects.create(
                name="Barbearia Francisco"
            )
        serializer = BarbershopSettingsSerializer(settings)
        return Response(serializer.data)
    
    def patch(self, request):
        settings = BarbershopSettings.objects.first()
        if not settings:
            settings = BarbershopSettings.objects.create()
        
        serializer = BarbershopSettingsSerializer(
            settings, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from django.db import models

# ========== COMMISSIONS VIEWS ==========

class CommissionListView(generics.ListAPIView):
    """List commissions (filtro por barbeiro/mês)"""
    serializer_class = CommissionSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        queryset = Commission.objects.all().select_related('barber')
        
        # Filtro por barbeiro
        barber_id = self.request.query_params.get('barber_id')
        if barber_id:
            queryset = queryset.filter(barber_id=barber_id)
        
        # Filtro por mês/ano
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        if month and year:
            queryset = queryset.filter(
                month__month=int(month),
                month__year=int(year)
            )
        
        # Se não é admin, mostrar apenas suas comissões (barbeiros)
        if not self.request.user.is_staff:
            queryset = queryset.filter(barber__user=self.request.user)
        
        return queryset.order_by('-month')

class CommissionCreateView(generics.CreateAPIView):
    """Create commission (admin only)"""
    serializer_class = CommissionSerializer
    permission_classes = (IsAdminUser,)

class CommissionMarkPaidView(APIView):
    """Mark commission as paid"""
    permission_classes = (IsAdminUser,)
    
    def post(self, request, pk):
        try:
            commission = Commission.objects.get(pk=pk)
            commission.is_paid = True
            commission.paid_at = timezone.now()
            commission.save()
            
            return Response({
                'message': 'Comissão marcada como paga',
                'commission': CommissionSerializer(commission).data
            })
        except Commission.DoesNotExist:
            return Response(
                {'error': 'Comissão não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

class CommissionSummaryView(APIView):
    """Get commission summary (total, pending, paid)"""
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        queryset = Commission.objects.all()
        
        # Filtro por barbeiro
        barber_id = request.query_params.get('barber_id')
        if barber_id:
            queryset = queryset.filter(barber_id=barber_id)
        elif not request.user.is_staff:
            # Se não é admin, mostrar apenas suas comissões
            queryset = queryset.filter(barber__user=request.user)
        
        summary = queryset.aggregate(
            total=Sum('final_amount'),
            pending=Sum('final_amount', filter=models.Q(is_paid=False)),
            paid=Sum('final_amount', filter=models.Q(is_paid=True)),
            count_pending=Count('id', filter=models.Q(is_paid=False)),
            count_paid=Count('id', filter=models.Q(is_paid=True))
        )
        
        return Response({
            'total': float(summary['total'] or 0),
            'pending': float(summary['pending'] or 0),
            'paid': float(summary['paid'] or 0),
            'count_pending': summary['count_pending'] or 0,
            'count_paid': summary['count_paid'] or 0
        })

# ========== SUPPLIERS VIEWS ==========

class SupplierListView(generics.ListAPIView):
    """List all suppliers"""
    serializer_class = SupplierSerializer
    permission_classes = (IsAdminUser,)
    queryset = Supplier.objects.all().order_by('name')

class SupplierCreateView(generics.CreateAPIView):
    """Create supplier"""
    serializer_class = SupplierSerializer
    permission_classes = (IsAdminUser,)

class SupplierUpdateView(generics.UpdateAPIView):
    """Update supplier"""
    serializer_class = SupplierSerializer
    permission_classes = (IsAdminUser,)
    queryset = Supplier.objects.all()

class SupplierDeleteView(generics.DestroyAPIView):
    """Delete supplier"""
    permission_classes = (IsAdminUser,)
    queryset = Supplier.objects.all()

# ========== LOYALTY VIEWS ==========

class LoyaltyMeView(APIView):
    """Get user's loyalty program data"""
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        loyalty, created = LoyaltyProgram.objects.get_or_create(
            user=request.user,
            defaults={'points': 0, 'tier': 'bronze'}
        )
        
        serializer = LoyaltyProgramSerializer(loyalty)
        return Response(serializer.data)

class LoyaltyRedeemView(APIView):
    """Redeem loyalty points"""
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        points_to_redeem = request.data.get('points', 0)
        
        try:
            loyalty = LoyaltyProgram.objects.get(user=request.user)
            
            if points_to_redeem > loyalty.points:
                return Response(
                    {'error': 'Pontos insuficientes'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Redeem points (100 pontos = R$ 10 de desconto)
            discount_value = (points_to_redeem / 100) * 10
            
            loyalty.points -= points_to_redeem
            loyalty.save()
            
            # TODO: Gerar cupom automático com desconto
            
            return Response({
                'message': 'Pontos resgatados com sucesso',
                'discount_value': discount_value,
                'remaining_points': loyalty.points
            })
        except LoyaltyProgram.DoesNotExist:
            return Response(
                {'error': 'Programa de fidelidade não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

class LoyaltyHistoryView(generics.ListAPIView):
    """Get loyalty points history"""
    serializer_class = LoyaltyProgramSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return LoyaltyProgram.objects.filter(user=self.request.user)

# ========== RECURRING APPOINTMENTS VIEWS ==========

class RecurringListView(generics.ListAPIView):
    """List recurring appointments"""
    serializer_class = RecurringAppointmentSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return RecurringAppointment.objects.filter(
            user=self.request.user,
            is_active=True
        ).select_related('service', 'barber')

class RecurringCreateView(generics.CreateAPIView):
    """Create recurring appointment"""
    serializer_class = RecurringAppointmentSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecurringUpdateView(generics.UpdateAPIView):
    """Update recurring appointment"""
    serializer_class = RecurringAppointmentSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return RecurringAppointment.objects.filter(user=self.request.user)

class RecurringDeleteView(generics.DestroyAPIView):
    """Delete recurring appointment"""
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return RecurringAppointment.objects.filter(user=self.request.user)
