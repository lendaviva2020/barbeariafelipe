"""
Permissões personalizadas para Django REST Framework
"""
from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Permissão que permite acesso apenas para usuários com role 'admin' ou is_staff
    """
    message = 'Acesso negado. Apenas administradores podem acessar este recurso.'
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser)
        )


class IsBarberOrAdmin(permissions.BasePermission):
    """
    Permissão que permite acesso para barbeiros ou administradores
    """
    message = 'Acesso negado. Apenas barbeiros e administradores podem acessar este recurso.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        is_admin = request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser
        is_barber = request.user.role == 'barber'
        
        return is_admin or is_barber


class IsAppointmentOwner(permissions.BasePermission):
    """
    Permissão que verifica se o usuário é dono do agendamento
    Também permite acesso para o barbeiro do agendamento e admins
    """
    message = 'Você não tem permissão para acessar este agendamento.'
    
    def has_object_permission(self, request, view, obj):
        # obj deve ser um Agendamento
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins sempre tem acesso
        if request.user.role == 'admin' or request.user.is_staff:
            return True
        
        # Dono do agendamento tem acesso
        if obj.user == request.user:
            return True
        
        # Barbeiro do agendamento tem acesso
        if hasattr(request.user, 'barbeiro') and obj.barber == request.user.barbeiro:
            return True
        
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão que permite escrita apenas para o dono do objeto
    Leitura é permitida para todos autenticados
    """
    def has_object_permission(self, request, view, obj):
        # Leitura permitida para qualquer usuário autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Escrita apenas para o dono
        return obj.user == request.user


class IsChatParticipant(permissions.BasePermission):
    """
    Permissão que verifica se o usuário é participante do chat
    (cliente do agendamento ou barbeiro ou admin)
    """
    message = 'Você não tem permissão para acessar este chat.'
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins sempre tem acesso
        if request.user.role == 'admin' or request.user.is_staff:
            return True
        
        # Para ChatMessage, verificar pelo agendamento
        if hasattr(obj, 'appointment'):
            appointment = obj.appointment
        else:
            # obj é o próprio agendamento
            appointment = obj
        
        # Cliente do agendamento
        if appointment.user == request.user:
            return True
        
        # Barbeiro do agendamento
        if hasattr(request.user, 'barbeiro') and appointment.barber == request.user.barbeiro:
            return True
        
        return False


class CanManageAISettings(permissions.BasePermission):
    """
    Permissão para gerenciar configurações de IA
    Apenas admins ou o próprio barbeiro podem configurar sua IA
    """
    message = 'Você não tem permissão para gerenciar configurações de IA.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins sempre podem
        if request.user.role == 'admin' or request.user.is_staff:
            return True
        
        # Barbeiro pode gerenciar suas próprias configurações
        if hasattr(obj, 'barber') and hasattr(request.user, 'barbeiro'):
            return obj.barber == request.user.barbeiro
        
        return False


class IsBarberOwner(permissions.BasePermission):
    """
    Permissão que verifica se o usuário é o dono do perfil de barbeiro
    Ou se é admin
    """
    message = 'Você não tem permissão para editar este perfil de barbeiro.'
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Leitura permitida para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admins podem editar qualquer barbeiro
        if request.user.role == 'admin' or request.user.is_staff:
            return True
        
        # Barbeiro pode editar apenas seu próprio perfil
        return obj.user == request.user


class CanSendNotifications(permissions.BasePermission):
    """
    Permissão para enviar notificações
    Apenas admins e barbeiros podem enviar notificações
    """
    message = 'Você não tem permissão para enviar notificações.'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        is_admin = request.user.role == 'admin' or request.user.is_staff
        is_barber = request.user.role == 'barber'
        
        return is_admin or is_barber


class CanManageRecurring(permissions.BasePermission):
    """
    Permissão para gerenciar agendamentos recorrentes
    Cliente pode gerenciar seus próprios, barbeiros e admins podem gerenciar todos
    """
    message = 'Você não tem permissão para gerenciar agendamentos recorrentes.'
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admins e barbeiros podem gerenciar todos
        if request.user.role in ['admin', 'barber'] or request.user.is_staff:
            return True
        
        # Cliente pode gerenciar apenas os seus
        return obj.user == request.user

