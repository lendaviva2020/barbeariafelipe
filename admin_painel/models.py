from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """Log de auditoria para ações administrativas"""

    ACTION_CHOICES = [
        ("create", "Criação"),
        ("update", "Atualização"),
        ("delete", "Exclusão"),
        ("login", "Login"),
        ("logout", "Logout"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Usuário",
    )
    action = models.CharField(
        max_length=10, choices=ACTION_CHOICES, verbose_name="Ação"
    )
    model_name = models.CharField(max_length=100, verbose_name="Modelo")
    object_id = models.CharField(
        max_length=100, blank=True, verbose_name="ID do Objeto"
    )
    details = models.JSONField(default=dict, verbose_name="Detalhes")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")

    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} ({self.created_at})"


class Promotion(models.Model):
    """Promoções automáticas"""

    PROMOTION_TYPE_CHOICES = [
        ("first_visit", "Primeira Visita"),
        ("happy_hour", "Happy Hour"),
        ("combo", "Combo"),
        ("loyalty", "Fidelidade"),
    ]

    DISCOUNT_TYPE_CHOICES = [
        ("percentage", "Porcentagem"),
        ("fixed", "Valor Fixo"),
    ]

    name = models.CharField(max_length=200, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")
    promotion_type = models.CharField(
        max_length=20, choices=PROMOTION_TYPE_CHOICES, verbose_name="Tipo"
    )
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default="percentage",
        verbose_name="Tipo de Desconto",
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor do Desconto"
    )

    # Condições (JSON)
    conditions = models.JSONField(
        default=dict,
        verbose_name="Condições",
        help_text='Ex: {"days_of_week": [0, 6], "time_start": "08:00", "time_end": "12:00"}',
    )

    active = models.BooleanField(default=True, verbose_name="Ativa")
    start_date = models.DateField(null=True, blank=True, verbose_name="Data de Início")
    end_date = models.DateField(null=True, blank=True, verbose_name="Data de Fim")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Promoção"
        verbose_name_plural = "Promoções"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
