from rest_framework import serializers

from .models import Barbeiro


class BarbeiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbeiro
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
