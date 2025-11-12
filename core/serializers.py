from rest_framework import serializers
from .models import (
    BarbershopSettings, Review, WaitingList, Product,
    Commission, Goal, Supplier, LoyaltyProgram, RecurringAppointment,
    AISettings, ChatMessage, AIConversationContext, Notification
)
from users.serializers import UserSerializer
from servicos.serializers import ServicoSerializer
from barbeiros.serializers import BarbeiroSerializer

class BarbershopSettingsSerializer(serializers.ModelSerializer):
    """Serializer para configurações da barbearia"""
    class Meta:
        model = BarbershopSettings
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer para avaliações"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    barber_name = serializers.CharField(source='barber.name', read_only=True, allow_null=True)
    service_name = serializers.CharField(source='service.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_name', 'barber', 'barber_name',
            'service', 'service_name', 'rating', 'comment',
            'is_approved', 'created_at'
        ]
        read_only_fields = ['created_at', 'is_approved']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating deve ser entre 1 e 5")
        return value

class CreateReviewSerializer(serializers.ModelSerializer):
    """Serializer para criar avaliação"""
    class Meta:
        model = Review
        fields = ['barber', 'service', 'rating', 'comment']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating deve ser entre 1 e 5")
        return value

class WaitingListSerializer(serializers.ModelSerializer):
    """Serializer para lista de espera"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    barber_name = serializers.CharField(source='barber.name', read_only=True, allow_null=True)
    
    class Meta:
        model = WaitingList
        fields = '__all__'
        read_only_fields = ['created_at', 'notified']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer para produtos"""
    needs_restock = serializers.BooleanField(read_only=True)
    profit_margin = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_profit_margin(self, obj):
        if obj.cost_price == 0:
            return 0
        return ((obj.selling_price - obj.cost_price) / obj.cost_price) * 100
    
    def validate(self, data):
        if data.get('selling_price', 0) < data.get('cost_price', 0):
            raise serializers.ValidationError("Preço de venda não pode ser menor que o custo")
        return data

class CommissionSerializer(serializers.ModelSerializer):
    """Serializer para comissões"""
    barber_name = serializers.CharField(source='barber.name', read_only=True)
    month_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Commission
        fields = '__all__'
        read_only_fields = ['created_at', 'commission_amount', 'final_amount']
    
    def get_month_display(self, obj):
        return obj.month.strftime('%B %Y')

class GoalSerializer(serializers.ModelSerializer):
    """Serializer para metas"""
    barber_name = serializers.CharField(source='barber.name', read_only=True, allow_null=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['created_at', 'is_completed']
    
    def get_progress_percentage(self, obj):
        return obj.get_progress()

class SupplierSerializer(serializers.ModelSerializer):
    """Serializer para fornecedores"""
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['created_at']

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    """Serializer para programa de fidelidade"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    tier_display = serializers.CharField(source='get_tier_display', read_only=True)
    
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'tier', 'total_spent', 'total_visits']

class RecurringAppointmentSerializer(serializers.ModelSerializer):
    """Serializer para agendamentos recorrentes"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    barber_name = serializers.CharField(source='barber.name', read_only=True)
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)
    
    class Meta:
        model = RecurringAppointment
        fields = '__all__'
        read_only_fields = ['created_at']


class AISettingsSerializer(serializers.ModelSerializer):
    """Serializer para configurações de IA"""
    barber_name = serializers.CharField(source='barber.name', read_only=True)
    personality_display = serializers.CharField(source='get_personality_display', read_only=True)
    
    class Meta:
        model = AISettings
        fields = [
            'id', 'barber', 'barber_name', 'is_enabled', 'personality',
            'personality_display', 'custom_instructions', 'max_message_length',
            'response_time_seconds', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_max_message_length(self, value):
        if value < 100 or value > 5000:
            raise serializers.ValidationError("Tamanho deve estar entre 100 e 5000 caracteres")
        return value
    
    def validate_response_time_seconds(self, value):
        if value < 1 or value > 60:
            raise serializers.ValidationError("Tempo de resposta deve estar entre 1 e 60 segundos")
        return value


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer para mensagens de chat"""
    sender_name = serializers.CharField(source='sender.name', read_only=True, allow_null=True)
    appointment_details = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'appointment', 'appointment_details', 'sender', 'sender_name',
            'message', 'is_ai_response', 'requires_human_attention',
            'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = ['created_at', 'is_ai_response', 'requires_human_attention', 'is_read', 'read_at']
    
    def get_appointment_details(self, obj):
        return {
            'id': obj.appointment.id,
            'date': obj.appointment.appointment_date,
            'time': obj.appointment.appointment_time,
            'customer_name': obj.appointment.customer_name
        }
    
    def validate_message(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Mensagem não pode estar vazia")
        if len(value) > 1000:
            raise serializers.ValidationError("Mensagem muito longa (máximo 1000 caracteres)")
        return value


class ChatMessageCreateSerializer(serializers.Serializer):
    """Serializer para criar mensagem de chat"""
    appointment_id = serializers.IntegerField()
    message = serializers.CharField(max_length=1000)
    
    def validate_message(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Mensagem não pode estar vazia")
        return value


class AIConversationContextSerializer(serializers.ModelSerializer):
    """Serializer para contexto de conversa"""
    appointment_info = serializers.SerializerMethodField()
    
    class Meta:
        model = AIConversationContext
        fields = [
            'id', 'appointment', 'appointment_info', 'context_data',
            'last_summary', 'message_count', 'last_user_message',
            'last_ai_response', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_appointment_info(self, obj):
        return {
            'id': obj.appointment.id,
            'customer_name': obj.appointment.customer_name,
            'date': obj.appointment.appointment_date,
            'time': obj.appointment.appointment_time
        }


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para notificações"""
    user_name = serializers.CharField(source='user.name', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    channel_display = serializers.CharField(source='get_channel_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    appointment_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_name', 'appointment', 'appointment_info',
            'type', 'type_display', 'channel', 'channel_display',
            'recipient', 'message', 'status', 'status_display',
            'error_message', 'external_id', 'sent_at', 'delivered_at', 'created_at'
        ]
        read_only_fields = ['created_at', 'sent_at', 'delivered_at', 'status', 'external_id']
    
    def get_appointment_info(self, obj):
        return {
            'id': obj.appointment.id,
            'customer_name': obj.appointment.customer_name,
            'date': obj.appointment.appointment_date,
            'time': obj.appointment.appointment_time
        }


class SendNotificationSerializer(serializers.Serializer):
    """Serializer para enviar notificação"""
    appointment_id = serializers.IntegerField()
    notification_type = serializers.ChoiceField(choices=[
        'confirmation', 'reminder', 'cancellation', 'rescheduled', 'completed'
    ])
    
    def validate_notification_type(self, value):
        valid_types = ['confirmation', 'reminder', 'cancellation', 'rescheduled', 'completed']
        if value not in valid_types:
            raise serializers.ValidationError(f"Tipo inválido. Deve ser um de: {', '.join(valid_types)}")
        return value

