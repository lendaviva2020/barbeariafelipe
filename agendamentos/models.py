import uuid
from django.conf import settings
from django.db import models

from barbeiros.models import Barbeiro
from cupons.models import Cupom
from servicos.models import Servico


class Agendamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("confirmed", "Confirmado"),
        ("completed", "Concluído"),
        ("cancelled", "Cancelado"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Dinheiro"),
        ("credit", "Cartão de Crédito"),
        ("debit", "Cartão de Débito"),
        ("pix", "PIX"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="agendamentos",
        verbose_name="Usuário",
        db_column="user_id",
    )
    service = models.ForeignKey(
        Servico, on_delete=models.PROTECT, verbose_name="Serviço", db_column="service_id"
    )
    barber = models.ForeignKey(
        Barbeiro, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Barbeiro", db_column="barber_id"
    )

    # Dados do agendamento
    appointment_date = models.DateField(verbose_name="Data")
    appointment_time = models.TimeField(verbose_name="Horário")

    # Dados do cliente
    customer_name = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    customer_phone = models.CharField(max_length=20, verbose_name="Telefone do Cliente")
    customer_email = models.EmailField(blank=True, verbose_name="Email do Cliente")
    notes = models.TextField(blank=True, verbose_name="Observações")

    # Pagamento
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default="cash",
        verbose_name="Forma de Pagamento",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço", null=True, blank=True)

    # Cupom aplicado
    coupon_code = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Código do Cupom", db_column="coupon_code"
    )

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Status", null=True, blank=True
    )
    cancelled_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Cancelado em"
    )
    cancel_reason = models.TextField(blank=True, verbose_name="Motivo do Cancelamento")
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Concluído em"
    )

    # Foto do resultado (opcional) - pode não existir na tabela
    # photo_url = models.URLField(blank=True, verbose_name="Foto do Resultado")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        db_table = "appointments"
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ["-appointment_date", "-appointment_time"]
        indexes = [
            models.Index(fields=["appointment_date", "appointment_time"]),
            models.Index(fields=["status"]),
            models.Index(fields=["user_id"]),
            models.Index(fields=["barber_id"]),
        ]

    def __str__(self):
        return f"{self.customer_name} - {self.appointment_date} {self.appointment_time}"

    @property
    def final_price(self):
        if self.price:
            return self.price
        return 0

    def cancel(self, reason=""):
        from django.utils import timezone

        self.status = "cancelled"
        self.cancelled_at = timezone.now()
        self.cancel_reason = reason
        self.save()

    def complete(self):
        from django.utils import timezone

        self.status = "completed"
        self.completed_at = timezone.now()
        self.save()
