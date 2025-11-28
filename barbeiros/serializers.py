from rest_framework import serializers

from core.validators import validate_phone

from .models import Barbeiro


class BarbeiroSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    
    class Meta:
        model = Barbeiro
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "photo")
        extra_kwargs = {"phone": {"validators": [validate_phone]}}
    
    def get_photo(self, obj):
        """Retorna URL da foto ou None"""
        return obj.photo_url if hasattr(obj, 'photo_url') and obj.photo_url else None
