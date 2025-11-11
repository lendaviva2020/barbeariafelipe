from rest_framework import serializers

from core.validators import validate_duration_positive, validate_price_positive

from .models import Servico


class ServicoSerializer(serializers.ModelSerializer):
    savings = serializers.ReadOnlyField()
    savings_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Servico
        fields = [
            "id", "name", "description", "price", "duration", "category",
            "image_url", "badge", "features", "is_combo", "original_price",
            "savings", "savings_percentage", "active", "created_at", "updated_at"
        ]
        read_only_fields = ("created_at", "updated_at", "savings", "savings_percentage")
        extra_kwargs = {
            "price": {"validators": [validate_price_positive]},
            "duration": {"validators": [validate_duration_positive]},
        }
