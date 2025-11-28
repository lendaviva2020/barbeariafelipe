import uuid
from django.conf import settings
from django.db import models


class Barbeiro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="barbeiro_profile",
        db_column="user_id",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200, verbose_name="Nome")
    specialty = models.CharField(
        max_length=200, blank=True, verbose_name="Especialidade"
    )
    bio = models.TextField(blank=True, verbose_name="Biografia")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    photo_url = models.URLField(blank=True, null=True, verbose_name="URL da Foto")
    active = models.BooleanField(default=True, verbose_name="Ativo")

    # Horários de trabalho (JSON)
    working_hours = models.JSONField(
        default=dict,
        verbose_name="Horários de Trabalho",
        help_text='Ex: {"monday": {"active": true, "start": "08:00", "end": "18:00"}}',
        blank=True,
        null=True,
    )
    # days_off no Supabase é date[], não JSON - não usar via Django
    # days_off = models.JSONField(...)  # Removido - usar SQL direto se necessário

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        db_table = "barbers"
        verbose_name = "Barbeiro"
        verbose_name_plural = "Barbeiros"
        ordering = ["name"]
        indexes = [
            models.Index(fields=['active']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
