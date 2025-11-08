from rest_framework import serializers

from core.validators import validate_brazilian_phone

from .models import Barbeiro


class BarbeiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbeiro
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {"phone": {"validators": [validate_brazilian_phone]}}
