# Extraído de modelos do React - Models adicionais
from django.db import models
from django.contrib.auth import get_user_model
from servicos.models import Servico
from barbeiros.models import Barbeiro
import json

User = get_user_model()


class AuditLog(models.Model):
    """Log de auditoria para rastreamento de ações administrativas"""
    ACTION_CHOICES = [
        ('CREATE', 'Criar'),
        ('UPDATE', 'Atualizar'),
        ('DELETE', 'Deletar'),
        ('INSERT', 'Inserir'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    table_name = models.CharField(max_length=100)
    record_id = models.CharField(max_length=100, null=True, blank=True)
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['table_name']),
            models.Index(fields=['action']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        user_name = self.user.name if self.user else 'Sistema'
        return f"{user_name} - {self.get_action_display()} em {self.table_name}"
    
    @staticmethod
    def log(user, action, table_name, record_id=None, old_data=None, new_data=None, request=None):
        """Helper method para criar logs de auditoria"""
        ip_address = None
        user_agent = ''
        
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        return AuditLog.objects.create(
            user=user,
            action=action,
            table_name=table_name,
            record_id=str(record_id) if record_id else None,
            old_data=old_data,
            new_data=new_data,
            ip_address=ip_address,
            user_agent=user_agent
        )

class BarbershopSettings(models.Model):
    """Configurações gerais da barbearia"""
    name = models.CharField(max_length=200, default="Barbearia Francisco")
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    description = models.TextField(blank=True)
    logo_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    
    # Configurações de horário
    opening_time = models.TimeField(default='08:00')
    closing_time = models.TimeField(default='20:00')
    
    # Configurações de agendamento
    slot_duration = models.IntegerField(default=30, help_text="Duração do slot em minutos")
    advance_booking_days = models.IntegerField(default=60, help_text="Dias de antecedência para agendamento")
    
    class Meta:
        verbose_name = "Configuração da Barbearia"
        verbose_name_plural = "Configurações da Barbearia"
    
    def __str__(self):
        return self.name

class Review(models.Model):
    """Avaliações dos clientes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    barber = models.ForeignKey(Barbeiro, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    service = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
    
    def __str__(self):
        return f"{self.user.name} - {self.rating}⭐"

class WaitingList(models.Model):
    """Lista de espera para horários indisponíveis"""
    STATUS_CHOICES = [
        ('waiting', 'Aguardando'),
        ('notified', 'Notificado'),
        ('contacted', 'Contactado'),
        ('scheduled', 'Agendado'),
        ('cancelled', 'Cancelado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Servico, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barbeiro, on_delete=models.CASCADE, null=True, blank=True)
    preferred_date = models.DateField()
    preferred_time_start = models.TimeField(null=True, blank=True)
    preferred_time_end = models.TimeField(null=True, blank=True)
    customer_name = models.CharField(max_length=200, default='')
    customer_phone = models.CharField(max_length=20, default='')
    customer_email = models.EmailField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    notified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Lista de Espera"
        verbose_name_plural = "Lista de Espera"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['preferred_date']),
        ]
    
    def __str__(self):
        return f"{self.customer_name} - {self.preferred_date}"

class Product(models.Model):
    """Produtos para inventário"""
    CATEGORY_CHOICES = [
        ('hair_care', 'Cuidados Capilares'),
        ('beard_care', 'Cuidados com Barba'),
        ('styling', 'Styling'),
        ('tools', 'Ferramentas'),
        ('other', 'Outros'),
    ]
    
    name = models.CharField(max_length=200, default='')
    description = models.TextField(blank=True, default='')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    brand = models.CharField(max_length=100, blank=True, default='')
    sku = models.CharField(max_length=100, unique=True, default='')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=5)
    image_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    @property
    def needs_restock(self):
        return self.stock_quantity <= self.min_stock_level

class Commission(models.Model):
    """Comissões dos barbeiros"""
    barber = models.ForeignKey(Barbeiro, on_delete=models.CASCADE, related_name='commissions')
    month = models.DateField()
    total_services = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=50.00, help_text="Porcentagem de comissão")
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-month']
        unique_together = ['barber', 'month']
        verbose_name = "Comissão"
        verbose_name_plural = "Comissões"
    
    def __str__(self):
        return f"{self.barber.name} - {self.month.strftime('%m/%Y')}"
    
    def calculate_commission(self):
        self.commission_amount = (self.total_revenue * self.commission_rate) / 100
        self.final_amount = self.commission_amount + self.bonus - self.deductions
        self.save()

class Goal(models.Model):
    """Metas individuais ou da equipe"""
    GOAL_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('team', 'Equipe'),
    ]
    
    METRIC_CHOICES = [
        ('revenue', 'Faturamento'),
        ('appointments', 'Agendamentos'),
        ('new_clients', 'Novos Clientes'),
        ('retention', 'Retenção'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    barber = models.ForeignKey(Barbeiro, on_delete=models.CASCADE, null=True, blank=True, related_name='goals')
    metric = models.CharField(max_length=50, choices=METRIC_CHOICES)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = "Meta"
        verbose_name_plural = "Metas"
    
    def __str__(self):
        return f"{self.name} ({self.get_progress()}%)"
    
    def get_progress(self):
        if self.target_value == 0:
            return 0
        return min(100, (self.current_value / self.target_value) * 100)

class Supplier(models.Model):
    """Fornecedores de produtos"""
    name = models.CharField(max_length=200, default='')
    company_name = models.CharField(max_length=200, blank=True, default='')
    cnpj = models.CharField(max_length=18, blank=True, default='')
    phone = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_person = models.CharField(max_length=200, blank=True)
    payment_terms = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
    
    def __str__(self):
        return self.name

class LoyaltyProgram(models.Model):
    """Programa de fidelidade"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loyalty')
    points = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_visits = models.IntegerField(default=0)
    tier = models.CharField(max_length=50, default='bronze', choices=[
        ('bronze', 'Bronze'),
        ('silver', 'Prata'),
        ('gold', 'Ouro'),
        ('platinum', 'Platinum'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Programa de Fidelidade"
        verbose_name_plural = "Programa de Fidelidade"
    
    def __str__(self):
        return f"{self.user.name} - {self.points} pontos ({self.tier})"
    
    def add_points(self, amount):
        """Adicionar pontos baseado no valor gasto"""
        # 1 ponto a cada R$ 10 gastos
        points_to_add = int(amount / 10)
        self.points += points_to_add
        self.total_spent += amount
        self.total_visits += 1
        self.update_tier()
        self.save()
    
    def update_tier(self):
        """Atualizar tier baseado em pontos"""
        if self.points >= 1000:
            self.tier = 'platinum'
        elif self.points >= 500:
            self.tier = 'gold'
        elif self.points >= 200:
            self.tier = 'silver'
        else:
            self.tier = 'bronze'

class RecurringAppointment(models.Model):
    """Agendamentos recorrentes"""
    FREQUENCY_CHOICES = [
        ('weekly', 'Semanal'),
        ('biweekly', 'Quinzenal'),
        ('monthly', 'Mensal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Servico, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barbeiro, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[(i, i) for i in range(7)], default=0, help_text="0=Segunda, 6=Domingo")
    time = models.TimeField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    customer_name = models.CharField(max_length=200, default='')
    customer_phone = models.CharField(max_length=20, default='')
    customer_email = models.EmailField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Agendamento Recorrente"
        verbose_name_plural = "Agendamentos Recorrentes"
    
    def __str__(self):
        return f"{self.customer_name} - {self.get_frequency_display()}"

class AISettings(models.Model):
    """Configurações de IA por barbeiro"""
    PERSONALITY_CHOICES = [
        ('friendly', 'Amigável'),
        ('professional', 'Profissional'),
    ]
    
    barber = models.OneToOneField(Barbeiro, on_delete=models.CASCADE, related_name='ai_settings')
    is_enabled = models.BooleanField(default=True, verbose_name="IA Habilitada")
    personality = models.CharField(max_length=20, choices=PERSONALITY_CHOICES, default='friendly', verbose_name="Personalidade")
    custom_instructions = models.TextField(blank=True, verbose_name="Instruções Personalizadas", help_text="Instruções específicas para personalizar o comportamento da IA")
    max_message_length = models.IntegerField(default=1000, verbose_name="Tamanho Máximo de Mensagem")
    response_time_seconds = models.IntegerField(default=5, verbose_name="Tempo de Resposta (segundos)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuração de IA"
        verbose_name_plural = "Configurações de IA"
    
    def __str__(self):
        return f"IA - {self.barber.name} ({self.get_personality_display()})"

class ChatMessage(models.Model):
    """Mensagens do chat entre cliente e barbeiro/IA"""
    appointment = models.ForeignKey('agendamentos.Agendamento', on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    message = models.TextField(verbose_name="Mensagem")
    is_ai_response = models.BooleanField(default=False, verbose_name="Resposta da IA")
    requires_human_attention = models.BooleanField(default=False, verbose_name="Requer Atenção Humana")
    is_read = models.BooleanField(default=False, verbose_name="Lida")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Lida em")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Mensagem de Chat"
        verbose_name_plural = "Mensagens de Chat"
        indexes = [
            models.Index(fields=['appointment', 'created_at']),
            models.Index(fields=['requires_human_attention']),
        ]
    
    def __str__(self):
        sender_name = self.sender.name if self.sender else 'IA'
        return f"{sender_name}: {self.message[:50]}..."
    
    def mark_as_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

class AIConversationContext(models.Model):
    """Contexto e histórico de conversas com IA"""
    appointment = models.OneToOneField('agendamentos.Agendamento', on_delete=models.CASCADE, related_name='ai_context')
    context_data = models.JSONField(default=dict, verbose_name="Dados de Contexto")
    last_summary = models.TextField(blank=True, verbose_name="Último Resumo")
    message_count = models.IntegerField(default=0, verbose_name="Contagem de Mensagens")
    last_user_message = models.TextField(blank=True, verbose_name="Última Mensagem do Usuário")
    last_ai_response = models.TextField(blank=True, verbose_name="Última Resposta da IA")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contexto de Conversa IA"
        verbose_name_plural = "Contextos de Conversa IA"
    
    def __str__(self):
        return f"Contexto - Agendamento #{self.appointment.id}"
    
    def increment_message_count(self):
        self.message_count += 1
        self.save()

class Notification(models.Model):
    """Registro de notificações enviadas"""
    TYPE_CHOICES = [
        ('confirmation', 'Confirmação'),
        ('reminder', 'Lembrete'),
        ('cancellation', 'Cancelamento'),
        ('rescheduled', 'Reagendamento'),
        ('completed', 'Concluído'),
    ]
    
    CHANNEL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('sent', 'Enviado'),
        ('failed', 'Falhou'),
        ('delivered', 'Entregue'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    appointment = models.ForeignKey('agendamentos.Agendamento', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Tipo")
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, verbose_name="Canal")
    recipient = models.CharField(max_length=200, verbose_name="Destinatário")
    message = models.TextField(verbose_name="Mensagem")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    error_message = models.TextField(blank=True, verbose_name="Mensagem de Erro")
    external_id = models.CharField(max_length=200, blank=True, verbose_name="ID Externo", help_text="ID da API externa (Twilio, etc)")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Enviado em")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Entregue em")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['appointment']),
            models.Index(fields=['type', 'channel']),
        ]
    
    def __str__(self):
        return f"{self.get_type_display()} via {self.get_channel_display()} - {self.recipient}"
    
    def mark_as_sent(self, external_id=None):
        from django.utils import timezone
        self.status = 'sent'
        self.sent_at = timezone.now()
        if external_id:
            self.external_id = external_id
        self.save()
    
    def mark_as_delivered(self):
        from django.utils import timezone
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save()
    
    def mark_as_failed(self, error_message):
        self.status = 'failed'
        self.error_message = error_message
        self.save()