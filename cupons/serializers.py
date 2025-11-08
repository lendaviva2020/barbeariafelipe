from rest_framework import serializers

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


class ValidateCupomSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=20)

    def validate_code(self, value):
        try:
            cupom = Cupom.objects.get(code=value.upper())
            if not cupom.is_valid:
                raise serializers.ValidationError(
                    "Cupom inválido, expirado ou esgotado"
                )
            return value
        except Cupom.DoesNotExist:
            raise serializers.ValidationError("Cupom não encontrado")
