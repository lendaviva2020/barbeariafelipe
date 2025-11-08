from rest_framework import serializers

from core.validators import validate_duration_positive, validate_price_positive

from .models import Servico


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {
            "price": {"validators": [validate_price_positive]},
            "duration": {"validators": [validate_duration_positive]},
        }
