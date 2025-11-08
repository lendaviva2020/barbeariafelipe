from rest_framework import serializers

from .models import AuditLog, Promotion


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "user_name",
            "action",
            "model_name",
            "object_id",
            "details",
            "ip_address",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class PromotionSerializer(serializers.ModelSerializer):
    is_active_now = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "description",
            "promotion_type",
            "discount_type",
            "discount_value",
            "conditions",
            "active",
            "start_date",
            "end_date",
            "is_active_now",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_is_active_now(self, obj):
        from django.utils import timezone

        now = timezone.now().date()

        if not obj.active:
            return False

        if obj.start_date and obj.start_date > now:
            return False

        if obj.end_date and obj.end_date < now:
            return False

        return True
