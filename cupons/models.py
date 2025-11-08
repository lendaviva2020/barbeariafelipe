from django.db import models


class Cupom(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ("percentage", "Porcentagem"),
        ("fixed", "Valor Fixo"),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Desconto"
    )
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default="percentage",
        verbose_name="Tipo de Desconto",
    )
    description = models.TextField(blank=True, verbose_name="Descrição")
    expiry_date = models.DateField(
        null=True, blank=True, verbose_name="Data de Expiração"
    )
    max_uses = models.IntegerField(
        default=0, verbose_name="Usos Máximos", help_text="0 para ilimitado"
    )
    current_uses = models.IntegerField(default=0, verbose_name="Usos Atuais")
    active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Cupom"
        verbose_name_plural = "Cupons"
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.code} - {self.discount}{"%" if self.discount_type == "percentage" else " R$"}'

    @property
    def is_valid(self):
        from django.utils import timezone

        if not self.active:
            return False
        if self.expiry_date and self.expiry_date < timezone.now().date():
            return False
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            return False
        return True
