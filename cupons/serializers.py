from rest_framework import serializers
from .models import Cupom
from django.utils import timezone

class CupomSerializer(serializers.ModelSerializer):
    """Serializer para listar cupons"""
    is_valid = serializers.SerializerMethodField()
    discount_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Cupom
        fields = [
            'id', 'code', 'discount', 'discount_type', 'description',
            'expiry_date', 'max_uses', 'current_uses', 'active',
            'is_valid', 'discount_display', 'created_at'
        ]
        read_only_fields = ['created_at', 'current_uses']
    
    def get_is_valid(self, obj):
        """Verificar se cupom é válido"""
        if not obj.active:
            return False
        if obj.expiry_date and obj.expiry_date < timezone.now().date():
            return False
        if obj.max_uses and obj.current_uses >= obj.max_uses:
            return False
        return True
    
    def get_discount_display(self, obj):
        """Formatação do desconto para exibição"""
        if obj.discount_type == 'percentage':
            return f"{obj.discount}%"
        return f"R$ {obj.discount:.2f}"

class CreateCupomSerializer(serializers.ModelSerializer):
    """Serializer para criar/editar cupons (admin)"""
    class Meta:
        model = Cupom
        fields = [
            'code', 'discount', 'discount_type', 'description',
            'expiry_date', 'max_uses', 'active'
        ]
    
    def validate_code(self, value):
        """Validar código do cupom"""
        if len(value) < 3:
            raise serializers.ValidationError("Código deve ter no mínimo 3 caracteres")
        return value.upper()
    
    def validate_discount(self, value):
        """Validar valor do desconto"""
        if value <= 0:
            raise serializers.ValidationError("Desconto deve ser maior que zero")
        return value
    
    def validate(self, data):
        """Validação cross-field"""
        if data.get('discount_type') == 'percentage' and data.get('discount', 0) > 100:
            raise serializers.ValidationError({
                'discount': 'Desconto percentual não pode ser maior que 100%'
            })
        return data

class ValidateCupomSerializer(serializers.Serializer):
    """Serializer para validar cupom"""
    code = serializers.CharField(max_length=50)
    
    def validate_code(self, value):
        return value.upper()
