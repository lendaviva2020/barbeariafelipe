from rest_framework import serializers

from core.validators import (validate_discount_percentage,
                             validate_price_positive)

from .models import Cupom


class CupomSerializer(serializers.ModelSerializer):
    is_valid_now = serializers.ReadOnlyField(source="is_valid")

    class Meta:
        model = Cupom
        fields = [
            "id",
            "code",
            "discount",
            "discount_type",
            "description",
            "expiry_date",
            "max_uses",
            "current_uses",
            "active",
            "is_valid_now",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "current_uses"]

    def validate_discount(self, value):
        """Validar desconto baseado no tipo"""
        discount_type = self.initial_data.get("discount_type", "percentage")

        if discount_type == "percentage":
            validate_discount_percentage(value)
        else:  # fixed
            validate_price_positive(value)

        return value


class ValidateCupomSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)

    # Não validar no serializer, deixar para a view lidar com isso
    # para poder retornar responses customizadas
