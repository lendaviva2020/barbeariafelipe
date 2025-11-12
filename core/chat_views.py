"""
Views REST para Chat com IA e Notificações
"""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import (
    AISettings, ChatMessage, AIConversationContext,
    Notification
)
from agendamentos.models import Agendamento
from .serializers import (
    AISettingsSerializer, ChatMessageSerializer,
    ChatMessageCreateSerializer, AIConversationContextSerializer,
    NotificationSerializer, SendNotificationSerializer
)
from .permissions import (
    IsBarberOrAdmin, IsChatParticipant,
    CanManageAISettings, CanSendNotifications
)
from .decorators import check_rate_limit
from .ai_chat import process_chat_message, get_ai_statistics
from .whatsapp import send_notification
import logging

logger = logging.getLogger(__name__)


class ChatSendMessageView(APIView):
    """
    Envia uma mensagem de chat e recebe resposta da IA
    POST /api/chat/send/
    """
    permission_classes = [IsAuthenticated]
    
    @check_rate_limit(key_prefix='chat_send', limit=30, period=60)
    def post(self, request):
        serializer = ChatMessageCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Dados inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment_id = serializer.validated_data['appointment_id']
        message = serializer.validated_data['message']
        
        # Buscar agendamento
        try:
            appointment = Agendamento.objects.get(id=appointment_id)
        except Agendamento.DoesNotExist:
            return Response(
                {'error': 'Agendamento não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar permissão (usuário deve ser dono do agendamento)
        if appointment.user != request.user:
            return Response(
                {'error': 'Acesso negado'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Processar mensagem e gerar resposta da IA
        result = process_chat_message(appointment, request.user, message)
        
        if not result.get('success'):
            return Response(
                {'error': 'Erro ao processar mensagem', 'details': result.get('error')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Serializar resposta
        user_msg_data = ChatMessageSerializer(result['user_message']).data
        ai_msg_data = ChatMessageSerializer(result['ai_message']).data
        
        return Response({
            'success': True,
            'user_message': user_msg_data,
            'ai_message': ai_msg_data,
            'requires_human_attention': result.get('requires_human_attention', False)
        }, status=status.HTTP_201_CREATED)


class ChatHistoryView(generics.ListAPIView):
    """
    Busca histórico de mensagens de um agendamento
    GET /api/chat/history/<appointment_id>/
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        appointment_id = self.kwargs.get('appointment_id')
        
        # Verificar se agendamento existe e se usuário tem permissão
        try:
            appointment = Agendamento.objects.get(id=appointment_id)
        except Agendamento.DoesNotExist:
            return ChatMessage.objects.none()
        
        # Verificar permissão
        is_owner = appointment.user == self.request.user
        is_barber = hasattr(self.request.user, 'barbeiro') and appointment.barber == self.request.user.barbeiro
        is_admin = self.request.user.role == 'admin' or self.request.user.is_staff
        
        if not (is_owner or is_barber or is_admin):
            return ChatMessage.objects.none()
        
        return ChatMessage.objects.filter(appointment=appointment).order_by('created_at')


class AISettingsListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria configurações de IA
    GET/POST /api/ai-settings/
    """
    serializer_class = AISettingsSerializer
    permission_classes = [IsAuthenticated, IsBarberOrAdmin]
    
    def get_queryset(self):
        # Admin vê todos, barbeiro vê apenas o seu
        if self.request.user.role == 'admin' or self.request.user.is_staff:
            return AISettings.objects.all()
        elif hasattr(self.request.user, 'barbeiro'):
            return AISettings.objects.filter(barber=self.request.user.barbeiro)
        return AISettings.objects.none()
    
    def perform_create(self, serializer):
        serializer.save()


class AISettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalhe, atualiza e deleta configurações de IA
    GET/PUT/DELETE /api/ai-settings/<id>/
    """
    serializer_class = AISettingsSerializer
    permission_classes = [IsAuthenticated, CanManageAISettings]
    queryset = AISettings.objects.all()


class AIStatsView(APIView):
    """
    Retorna estatísticas do sistema de IA
    GET /api/ai/stats/
    """
    permission_classes = [IsAuthenticated, IsBarberOrAdmin]
    
    def get(self, request):
        # Se for barbeiro, filtrar por barbeiro
        barber = None
        if hasattr(request.user, 'barbeiro'):
            barber = request.user.barbeiro
        
        stats = get_ai_statistics(barber=barber)
        return Response(stats, status=status.HTTP_200_OK)


class ChatRequiringAttentionView(generics.ListAPIView):
    """
    Lista mensagens que requerem atenção humana
    GET /api/chat/attention/
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated, IsBarberOrAdmin]
    
    def get_queryset(self):
        # Filtrar mensagens não lidas que requerem atenção
        queryset = ChatMessage.objects.filter(
            requires_human_attention=True,
            is_read=False
        ).select_related('appointment', 'sender').order_by('-created_at')
        
        # Se for barbeiro, filtrar apenas seus agendamentos
        if hasattr(self.request.user, 'barbeiro'):
            queryset = queryset.filter(appointment__barber=self.request.user.barbeiro)
        
        return queryset


class ChatMarkReadView(APIView):
    """
    Marca mensagem como lida
    POST /api/chat/<message_id>/read/
    """
    permission_classes = [IsAuthenticated, IsBarberOrAdmin]
    
    def post(self, request, message_id):
        try:
            message = ChatMessage.objects.get(id=message_id)
        except ChatMessage.DoesNotExist:
            return Response(
                {'error': 'Mensagem não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar permissão
        is_barber = hasattr(request.user, 'barbeiro') and message.appointment.barber == request.user.barbeiro
        is_admin = request.user.role == 'admin' or request.user.is_staff
        
        if not (is_barber or is_admin):
            return Response(
                {'error': 'Acesso negado'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.mark_as_read()
        
        return Response(
            {'success': True, 'message': 'Mensagem marcada como lida'},
            status=status.HTTP_200_OK
        )


class SendNotificationView(APIView):
    """
    Envia notificação WhatsApp
    POST /api/notifications/send/
    """
    permission_classes = [IsAuthenticated, CanSendNotifications]
    
    @check_rate_limit(key_prefix='notification_send', limit=20, period=60)
    def post(self, request):
        serializer = SendNotificationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Dados inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment_id = serializer.validated_data['appointment_id']
        notification_type = serializer.validated_data['notification_type']
        
        # Buscar agendamento
        try:
            appointment = Agendamento.objects.get(id=appointment_id)
        except Agendamento.DoesNotExist:
            return Response(
                {'error': 'Agendamento não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Enviar notificação
        result = send_notification(appointment, notification_type, request.user)
        
        if result.get('success'):
            return Response({
                'success': True,
                'message': 'Notificação enviada com sucesso',
                'whatsapp_url': result.get('whatsapp_url'),
                'notification_id': result.get('notification_id')
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': result.get('error'),
                'whatsapp_url': result.get('whatsapp_url'),  # URL de fallback
                'notification_id': result.get('notification_id')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotificationListView(generics.ListAPIView):
    """
    Lista notificações
    GET /api/notifications/
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Admin vê todas, usuários veem apenas as suas
        if self.request.user.role == 'admin' or self.request.user.is_staff:
            return Notification.objects.all().order_by('-created_at')
        else:
            return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class NotificationDetailView(generics.RetrieveAPIView):
    """
    Detalhe de notificação
    GET /api/notifications/<id>/
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Admin vê todas, usuários veem apenas as suas
        if self.request.user.role == 'admin' or self.request.user.is_staff:
            return Notification.objects.all()
        else:
            return Notification.objects.filter(user=self.request.user)

