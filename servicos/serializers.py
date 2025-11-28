from rest_framework import serializers

from core.validators import validate_duration_positive, validate_price_positive

from .models import Servico


class ServicoSerializer(serializers.ModelSerializer):
    # Campos calculados/compatibilidade
    badge = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    is_combo = serializers.SerializerMethodField()
    original_price = serializers.SerializerMethodField()
    savings = serializers.SerializerMethodField()
    savings_percentage = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()
    
    class Meta:
        model = Servico
        fields = [
            "id", "name", "description", "price", "duration", "category",
            "image_url", "badge", "features", "is_combo", "original_price",
            "savings", "savings_percentage", "active", "created_at", "updated_at"
        ]
        read_only_fields = ("created_at", "updated_at", "badge", "features", "is_combo", 
                           "original_price", "savings", "savings_percentage", "active")
        extra_kwargs = {
            "price": {"validators": [validate_price_positive]},
            "duration": {"validators": [validate_duration_positive]},
        }
    
    def get_badge(self, obj):
        """Retorna badge baseado na categoria ou nome"""
        if 'premium' in obj.name.lower() or 'vip' in obj.name.lower():
            return 'Premium'
        elif 'popular' in obj.name.lower() or obj.category == 'haircut':
            return 'Popular'
        elif obj.category == 'combo':
            return 'Combo'
        return None
    
    def get_features(self, obj):
        """Retorna lista de features padrão"""
        return ['Atendimento profissional', 'Produtos premium', 'Ambiente climatizado']
    
    def get_is_combo(self, obj):
        """Verifica se é combo baseado na categoria"""
        return obj.category == 'combo'
    
    def get_original_price(self, obj):
        """Retorna preço original (para combos, pode ter desconto)"""
        if obj.category == 'combo':
            # Se for combo, pode ter um preço original maior
            return float(obj.price) * 1.1  # 10% de desconto simulado
        return None
    
    def get_savings(self, obj):
        """Calcula economia se for combo"""
        if obj.category == 'combo' and self.get_original_price(obj):
            original = self.get_original_price(obj)
            return float(original) - float(obj.price)
        return None
    
    def get_savings_percentage(self, obj):
        """Calcula percentual de economia"""
        if self.get_savings(obj):
            original = self.get_original_price(obj)
            savings = self.get_savings(obj)
            return round((savings / original) * 100, 0)
        return None
    
    def get_active(self, obj):
        """Retorna se o serviço está ativo"""
        # Verificar active ou is_active
        active = getattr(obj, 'active', None)
        is_active = getattr(obj, 'is_active', None)
        return active if active is not None else (is_active if is_active is not None else True)
