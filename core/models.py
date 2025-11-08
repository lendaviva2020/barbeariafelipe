from django.conf import settings
from django.db import models


class BarbershopSettings(models.Model):
    """Configurações gerais da barbearia"""

    name = models.CharField(
        max_length=200, default="Barbearia Francisco", verbose_name="Nome"
    )
    description = models.TextField(blank=True, verbose_name="Descrição")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    whatsapp = models.CharField(
        max_length=20, default="5545999417111", verbose_name="WhatsApp"
    )
    email = models.EmailField(blank=True, verbose_name="E-mail")
    address = models.TextField(blank=True, verbose_name="Endereço")

    # Horário de funcionamento
    opening_hours = models.JSONField(
        default=dict, verbose_name="Horário de Funcionamento"
    )

    # Redes sociais
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    facebook = models.URLField(blank=True, verbose_name="Facebook")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Configuração da Barbearia"
        verbose_name_plural = "Configurações da Barbearia"

    def __str__(self):
        return self.name


class Review(models.Model):
    """Avaliações dos clientes"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Usuário",
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], verbose_name="Nota"
    )
    comment = models.TextField(verbose_name="Comentário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    approved = models.BooleanField(default=False, verbose_name="Aprovado")

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.name} - {self.rating} estrelas"


class WaitingList(models.Model):
    """Lista de espera para horários"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário"
    )
    date = models.DateField(verbose_name="Data")
    time = models.TimeField(verbose_name="Horário")
    service = models.ForeignKey(
        "servicos.Servico", on_delete=models.CASCADE, verbose_name="Serviço"
    )
    barber = models.ForeignKey(
        "barbeiros.Barbeiro",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Barbeiro",
    )
    notified = models.BooleanField(default=False, verbose_name="Notificado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Lista de Espera"
        verbose_name_plural = "Lista de Espera"
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.user.name} - {self.date} {self.time}"
