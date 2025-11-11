from django.db import models


class Servico(models.Model):
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
    image_url = models.URLField(blank=True, verbose_name="URL da Imagem")
    badge = models.CharField(max_length=50, blank=True, verbose_name="Badge/Destaque")
    features = models.JSONField(default=list, blank=True, verbose_name="Características")
    
    # Campos para combos
    is_combo = models.BooleanField(default=False, verbose_name="É um Combo?")
    original_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Preço Original"
    )
    combo_services = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        blank=True, 
        related_name='combos',
        verbose_name="Serviços do Combo"
    )
    
    active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=['active', 'category']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - R$ {self.price}"
    
    @property
    def savings(self):
        """Calcula economia para combos"""
        if self.is_combo and self.original_price:
            return self.original_price - self.price
        return 0
    
    @property
    def savings_percentage(self):
        """Calcula percentual de economia"""
        if self.is_combo and self.original_price and self.original_price > 0:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0
