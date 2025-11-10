from rest_framework import serializers
from .models import (
    BarbershopSettings, Review, WaitingList, Product,
    Commission, Goal, Supplier, LoyaltyProgram, RecurringAppointment
)
from users.serializers import UserSerializer
from servicos.serializers import ServicoSerializer
from barbeiros.serializers import BarbeiroSerializer

class BarbershopSettingsSerializer(serializers.ModelSerializer):
    """Serializer para configurações da barbearia"""
    class Meta:
        model = BarbershopSettings
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer para avaliações"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    barber_name = serializers.CharField(source='barber.name', read_only=True, allow_null=True)
    service_name = serializers.CharField(source='service.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_name', 'barber', 'barber_name',
            'service', 'service_name', 'rating', 'comment',
            'is_approved', 'created_at'
        ]
        read_only_fields = ['created_at', 'is_approved']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating deve ser entre 1 e 5")
        return value

class CreateReviewSerializer(serializers.ModelSerializer):
    """Serializer para criar avaliação"""
    class Meta:
        model = Review
        fields = ['barber', 'service', 'rating', 'comment']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating deve ser entre 1 e 5")
        return value

class WaitingListSerializer(serializers.ModelSerializer):
    """Serializer para lista de espera"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    barber_name = serializers.CharField(source='barber.name', read_only=True, allow_null=True)
    
    class Meta:
        model = WaitingList
        fields = '__all__'
        read_only_fields = ['created_at', 'notified']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer para produtos"""
    needs_restock = serializers.BooleanField(read_only=True)
    profit_margin = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_profit_margin(self, obj):
        if obj.cost_price == 0:
            return 0
        return ((obj.selling_price - obj.cost_price) / obj.cost_price) * 100
    
    def validate(self, data):
        if data.get('selling_price', 0) < data.get('cost_price', 0):
            raise serializers.ValidationError("Preço de venda não pode ser menor que o custo")
        return data

class CommissionSerializer(serializers.ModelSerializer):
    """Serializer para comissões"""
    barber_name = serializers.CharField(source='barber.name', read_only=True)
    month_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Commission
        fields = '__all__'
        read_only_fields = ['created_at', 'commission_amount', 'final_amount']
    
    def get_month_display(self, obj):
        return obj.month.strftime('%B %Y')

class GoalSerializer(serializers.ModelSerializer):
    """Serializer para metas"""
    barber_name = serializers.CharField(source='barber.name', read_only=True, allow_null=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['created_at', 'is_completed']
    
    def get_progress_percentage(self, obj):
        return obj.get_progress()

class SupplierSerializer(serializers.ModelSerializer):
    """Serializer para fornecedores"""
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['created_at']

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    """Serializer para programa de fidelidade"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    tier_display = serializers.CharField(source='get_tier_display', read_only=True)
    
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'tier', 'total_spent', 'total_visits']

class RecurringAppointmentSerializer(serializers.ModelSerializer):
    """Serializer para agendamentos recorrentes"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    barber_name = serializers.CharField(source='barber.name', read_only=True)
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)
    
    class Meta:
        model = RecurringAppointment
        fields = '__all__'
        read_only_fields = ['created_at']

