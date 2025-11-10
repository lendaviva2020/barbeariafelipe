import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbearia.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Criar ou atualizar admin
if User.objects.filter(email='admin@barbearia.com').exists():
    admin = User.objects.get(email='admin@barbearia.com')
    admin.set_password('admin123')
    admin.role = 'admin'
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print('OK - Senha do admin resetada!')
else:
    admin = User.objects.create_superuser(
        email='admin@barbearia.com',
        password='admin123',
        name='Administrador'
    )
    print('OK - Admin criado!')

print('')
print('=== CREDENCIAIS ===')
print('Email: admin@barbearia.com')
print('Senha: admin123')
print('')
print('Acesse: http://localhost:8000/django-admin/')

