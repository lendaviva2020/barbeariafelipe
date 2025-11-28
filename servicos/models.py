import uuid
from django.db import models


class Servico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CATEGORY_CHOICES = [
        ("haircut", "Corte"),
        ("beard", "Barba"),
        ("treatment", "Tratamento"),
        ("combo", "Combo"),
    ]

    name = models.CharField(max_length=200, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    duration = models.IntegerField(default=30, verbose_name="Duração (minutos)")
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
        default="haircut",
        verbose_name="Categoria",
    )
    image_url = models.URLField(blank=True, null=True, verbose_name="URL da Imagem")
    
    # Campos que podem não existir no Supabase - marcados como opcionais
    is_active = models.BooleanField(default=True, verbose_name="Ativo", null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name="Ativo", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        db_table = "services"
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=['active', 'category']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - R$ {self.price}"
