from django.conf import settings
from django.db import models

from barbeiros.models import Barbeiro
from cupons.models import Cupom
from servicos.models import Servico


class Agendamento(models.Model):
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
    )
    service = models.ForeignKey(
        Servico, on_delete=models.PROTECT, verbose_name="Serviço"
    )
    barber = models.ForeignKey(
        Barbeiro, on_delete=models.PROTECT, verbose_name="Barbeiro"
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
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Desconto"
    )

    # Cupom aplicado
    coupon = models.ForeignKey(
        Cupom, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cupom"
    )
    coupon_code = models.CharField(
        max_length=20, blank=True, verbose_name="Código do Cupom"
    )
    promotion_applied = models.CharField(
        max_length=200, blank=True, verbose_name="Promoção Aplicada"
    )

    # Status
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Status"
    )
    cancelled_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Cancelado em"
    )
    cancel_reason = models.TextField(blank=True, verbose_name="Motivo do Cancelamento")
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Concluído em"
    )

    # Foto do resultado (opcional)
    photo_url = models.URLField(blank=True, verbose_name="Foto do Resultado")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ["-appointment_date", "-appointment_time"]
        indexes = [
            models.Index(fields=["appointment_date", "appointment_time"]),
            models.Index(fields=["status"]),
            models.Index(fields=["user"]),
            models.Index(fields=["barber"]),
        ]

    def __str__(self):
        return f"{self.customer_name} - {self.appointment_date} {self.appointment_time}"

    @property
    def final_price(self):
        return self.price - self.discount_amount

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
