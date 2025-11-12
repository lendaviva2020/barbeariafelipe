from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from core.decorators import admin_required, admin_required_api
from users.models import User
from core.models import AuditLog


@admin_required
def users_view(request):
    """Página de gerenciamento de usuários"""
    return render(request, 'admin/users.html')


@admin_required_api
def users_list_api(request):
    """API: Lista de usuários com filtros"""
    # Filtros
    role_filter = request.GET.get('role', 'all')
    search = request.GET.get('search', '')
    
    # Query base
    users = User.objects.all()
    
    # Filtro por role
    if role_filter == 'admin':
        users = users.filter(is_staff=True)
    elif role_filter == 'active':
        users = users.filter(is_active=True)
    elif role_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Busca
    if search:
        users = users.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    # Ordenar
    users = users.order_by('-created_at')
    
    # Limitar resultados
    users = users[:200]
    
    # Serializar
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone or '',
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None,
        })
    
    return JsonResponse({'users': data})


@admin_required_api
@require_http_methods(["POST"])
def toggle_admin_api(request, pk):
    """API: Alternar status de administrador"""
    try:
        user = User.objects.get(pk=pk)
        
        # Não permitir remover admin do próprio usuário
        if user.id == request.user.id:
            return JsonResponse({
                'error': 'Você não pode alterar suas próprias permissões'
            }, status=400)
        
        old_value = user.is_staff
        user.is_staff = not user.is_staff
        user.save()
        
        # Log de auditoria
        AuditLog.log(
            user=request.user,
            action='UPDATE',
            table_name='users',
            record_id=pk,
            old_data={'is_staff': old_value},
            new_data={'is_staff': user.is_staff},
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Permissões atualizadas',
            'is_staff': user.is_staff
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@admin_required_api
@require_http_methods(["POST"])
def toggle_active_api(request, pk):
    """API: Ativar/desativar usuário"""
    try:
        user = User.objects.get(pk=pk)
        
        # Não permitir desativar o próprio usuário
        if user.id == request.user.id:
            return JsonResponse({
                'error': 'Você não pode desativar sua própria conta'
            }, status=400)
        
        old_value = user.is_active
        user.is_active = not user.is_active
        user.save()
        
        # Log de auditoria
        AuditLog.log(
            user=request.user,
            action='UPDATE',
            table_name='users',
            record_id=pk,
            old_data={'is_active': old_value},
            new_data={'is_active': user.is_active},
            request=request
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Status atualizado',
            'is_active': user.is_active
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

