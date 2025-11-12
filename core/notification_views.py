"""
Views de notificações para o centro de notificações
"""
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.models import Notification
from core.serializers import NotificationSerializer
from django.utils import timezone


class NotificationUnreadView(generics.ListAPIView):
    """
    Lista notificações não lidas do usuário
    GET /api/notifications/unread/
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            status='pending'
        ).select_related('appointment', 'appointment__servico', 'appointment__barbeiro').order_by('-created_at')[:20]


class NotificationMarkReadView(APIView):
    """
    Marca notificação como lida
    POST /api/notifications/<id>/mark-read/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            notification = Notification.objects.get(
                pk=pk,
                user=request.user
            )
            
            notification.status = 'sent'
            notification.save()
            
            return Response({
                'success': True,
                'message': 'Notificação marcada como lida'
            })
        except Notification.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Notificação não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)


class NotificationMarkAllReadView(APIView):
    """
    Marca todas notificações como lidas
    POST /api/notifications/mark-all-read/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        updated = Notification.objects.filter(
            user=request.user,
            status='pending'
        ).update(status='sent')
        
        return Response({
            'success': True,
            'message': f'{updated} notificações marcadas como lidas',
            'count': updated
        })


class NotificationDeleteView(APIView):
    """
    Deleta uma notificação
    DELETE /api/notifications/<id>/delete/
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(
                pk=pk,
                user=request.user
            )
            
            notification.delete()
            
            return Response({
                'success': True,
                'message': 'Notificação excluída'
            })
        except Notification.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Notificação não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)


class NotificationStatsView(APIView):
    """
    Estatísticas de notificações
    GET /api/notifications/stats/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        total = Notification.objects.filter(user=request.user).count()
        unread = Notification.objects.filter(user=request.user, status='pending').count()
        sent = Notification.objects.filter(user=request.user, status='sent').count()
        failed = Notification.objects.filter(user=request.user, status='failed').count()
        
        return Response({
            'total': total,
            'unread': unread,
            'read': sent,
            'failed': failed
        })

