from rest_framework import serializers


from .models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)
    barber_name = serializers.CharField(source="barber.name", read_only=True)
    final_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Agendamento
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")


class CreateAgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = (
            "service",
            "barber",
            "appointment_date",
            "appointment_time",
            "customer_name",
            "customer_phone",
            "customer_email",
            "notes",
            "payment_method",
            "price",
            "discount_amount",
            "coupon_code",
        )

    def validate(self, data):
        # Verificar se já existe agendamento no mesmo horário
        existing = Agendamento.objects.filter(
            appointment_date=data["appointment_date"],
            appointment_time=data["appointment_time"],
            barber=data["barber"],
            status__in=["pending", "confirmed"],
        ).exists()

        if existing:
            raise serializers.ValidationError("Horário já está ocupado")

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
