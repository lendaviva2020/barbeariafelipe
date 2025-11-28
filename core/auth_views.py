"""
Views de autenticação melhoradas com verificação de admin
Baseado no código Auth.tsx do React
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from users.models import User
from core.models import AuditLog
import json


def auth_page(request):
    """Página de autenticação com tabs login/registro"""
    if request.user.is_authenticated:
        # Se já estiver autenticado e houver next, redirecionar
        next_url = request.GET.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('core:home')
    
    # Verificar parâmetros de URL
    redirect_param = request.GET.get('redirect', '')
    mode = request.GET.get('mode', 'login')
    is_admin_login = redirect_param == 'admin'
    service_id = request.GET.get('service', '')
    barber_id = request.GET.get('barber', '')
    next_url = request.GET.get('next', '')
    
    context = {
        'mode': mode,
        'is_admin_login': is_admin_login,
        'redirect_param': redirect_param,
        'service_id': service_id,
        'barber_id': barber_id,
        'next_url': next_url
    }
    
    return render(request, 'auth/auth_enhanced.html', context)


@require_http_methods(["POST"])
def login_view(request):
    """Login com verificação de admin"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '')
        is_admin_login = data.get('isAdminLogin', False)
        
        # Validar campos
        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Email e senha são obrigatórios'
            }, status=400)
        
        # Autenticar
        user = authenticate(request, email=email, password=password)
        
        if not user:
            # Log tentativa falhada
            AuditLog.log(
                user=None,
                action='INSERT',
                table_name='auth_login',
                old_data={'email': email, 'success': False},
                request=request
            )
            
            return JsonResponse({
                'success': False,
                'error': 'Email ou senha incorretos'
            }, status=401)
        
        if not user.is_active:
            return JsonResponse({
                'success': False,
                'error': 'Usuário inativo. Entre em contato com o suporte.'
            }, status=403)
        
        # Login admin - verificar permissões
        if is_admin_login:
            if not user.is_staff:
                # Log tentativa de acesso admin negada
                AuditLog.log(
                    user=user,
                    action='INSERT',
                    table_name='auth_admin_denied',
                    new_data={'reason': 'not_staff'},
                    request=request
                )
                
                return JsonResponse({
                    'success': False,
                    'error': 'Você não tem permissões de administrador',
                    'redirect': '/'
                }, status=403)
            
            # Log acesso admin bem-sucedido
            AuditLog.log(
                user=user,
                action='INSERT',
                table_name='auth_admin_login',
                new_data={'success': True},
                request=request
            )
        
        # Fazer login
        auth_login(request, user)
        
        # Log login bem-sucedido
        AuditLog.log(
            user=user,
            action='INSERT',
            table_name='auth_login',
            new_data={'success': True, 'is_admin': is_admin_login},
            request=request
        )
        
        # Determinar redirect
        redirect_url = '/admin-painel/dashboard/' if is_admin_login else '/'
        
        return JsonResponse({
            'success': True,
            'message': 'Login realizado com sucesso',
            'redirect': redirect_url,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'is_staff': user.is_staff
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        print(f"Erro no login: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Erro interno. Tente novamente.'
        }, status=500)


@require_http_methods(["POST"])
def register_view(request):
    """Registro de novo usuário"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        phone = data.get('phone', '').strip()
        
        # Validações
        errors = {}
        
        if not name or len(name) < 2:
            errors['name'] = 'Nome deve ter pelo menos 2 caracteres'
        
        if not email:
            errors['email'] = 'Email é obrigatório'
        elif '@' not in email or '.' not in email:
            errors['email'] = 'Email inválido'
        
        if not password:
            errors['password'] = 'Senha é obrigatória'
        elif len(password) < 6:
            errors['password'] = 'Senha deve ter pelo menos 6 caracteres'
        
        if password != confirm_password:
            errors['confirmPassword'] = 'As senhas não conferem'
        
        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
        
        # Verificar se email já existe
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'errors': {'email': 'Este email já está cadastrado'}
            }, status=400)
        
        # Criar usuário
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            phone=phone
        )
        
        # Log registro
        AuditLog.log(
            user=user,
            action='CREATE',
            table_name='users',
            record_id=user.id,
            new_data={'name': name, 'email': email},
            request=request
        )
        
        # Fazer login automático
        auth_login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Conta criada com sucesso!',
            'redirect': '/',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Dados inválidos'
        }, status=400)
    except Exception as e:
        print(f"Erro no registro: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Erro ao criar conta. Tente novamente.'
        }, status=500)


def logout_view(request):
    """Logout do usuário"""
    user_name = request.user.name if request.user.is_authenticated else None
    
    # Log logout
    if request.user.is_authenticated:
        AuditLog.log(
            user=request.user,
            action='INSERT',
            table_name='auth_logout',
            new_data={'name': user_name},
            request=request
        )
    
    auth_logout(request)
    messages.success(request, 'Logout realizado com sucesso')
    return redirect('core:home')

