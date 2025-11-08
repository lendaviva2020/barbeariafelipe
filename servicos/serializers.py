from rest_framework import serializers

from .models import Servico


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
