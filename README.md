# 🎯 Barbearia Francisco - Django

Sistema completo de gerenciamento de barbearia construído com Django + SQLite + Templates HTML.

## ✨ Funcionalidades

### 👥 Para Clientes
- ✅ Registro e login
- ✅ Agendamento online de serviços
- ✅ Seleção de barbeiro e horário
- ✅ Histórico de agendamentos
- ✅ Confirmação via WhatsApp

### 🛡️ Para Administradores
- ✅ Dashboard com métricas em tempo real
- ✅ Gerenciamento de agendamentos (pendentes, confirmados, completados, cancelados)
- ✅ CRUD de serviços
- ✅ CRUD de barbeiros
- ✅ CRUD de cupons
- ✅ Relatórios e estatísticas

## 🚀 Tecnologias

- **Backend:** Django 5.1
- **API:** Django REST Framework 3.15
- **Auth:** SimpleJWT (JWT tokens)
- **Database:** SQLite 
- **Frontend:** HTML5 + CSS3 + JavaScript Vanilla
- **Deploy:** Vercel / Railway

## 📦 Estrutura do Projeto

```
barbearia-django/
├── barbearia/              # Configuração principal
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Utils e configurações
│   ├── models.py          # BarbershopSettings, Review, WaitingList
│   └── whatsapp.py        # Integração WhatsApp
├── users/                  # Autenticação
│   ├── models.py          # User customizado
│   ├── views.py           # Login, Register, JWT
│   └── serializers.py
├── agendamentos/           # Sistema de agendamento
│   ├── models.py          # Agendamento
│   ├── views.py           # CRUD agendamentos
│   └── serializers.py
├── servicos/               # Catálogo de serviços
│   ├── models.py          # Servico
│   └── views.py
├── barbeiros/              # Gestão de barbeiros
│   ├── models.py          # Barbeiro
│   └── views.py
├── cupons/                 # Sistema de cupons
│   └── models.py          # Cupom
├── admin_painel/           # Dashboard administrativo
│   ├── models.py          # AuditLog, Promotion
│   └── views.py           # Dashboard stats, gerenciamento
├── templates/              # Templates HTML
│   ├── base.html
│   ├── home.html
│   ├── auth/login.html
│   ├── agendamentos/criar.html
│   └── admin/dashboard.html
├── static/                 # CSS, JS, imagens
│   ├── css/
│   ├── js/
│   └── images/
├── requirements.txt
├── Procfile
└── manage.py
```

## ⚙️ Instalação Local

### 1. Clone o repositório

```bash
cd barbearia-django
```

### 2. Crie ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure variáveis de ambiente

Crie arquivo `.env`:
```
SECRET_KEY=your-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
WHATSAPP_PHONE=5545999417111
```

### 6. Execute as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crie superusuário (admin)

```bash
python manage.py createsuperuser
```

### 8. Colete arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 9. Rode o servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

## 📡 API Endpoints

### Autenticação
- `POST /api/users/register/` - Registro
- `POST /api/users/login/` - Login
- `POST /api/users/logout/` - Logout
- `POST /api/users/token/refresh/` - Refresh token
- `GET /api/users/me/` - Dados do usuário

### Agendamentos
- `GET /api/agendamentos/` - Listar agendamentos
- `POST /api/agendamentos/create/` - Criar agendamento
- `POST /api/agendamentos/<id>/cancel/` - Cancelar agendamento
- `GET /api/agendamentos/available-slots/` - Horários disponíveis

### Serviços
- `GET /api/servicos/` - Listar serviços

### Barbeiros
- `GET /api/barbeiros/` - Listar barbeiros

### Admin (requer permissão admin)
- `GET /api/admin/dashboard/stats/` - Estatísticas do dashboard
- `GET /api/admin/agendamentos/` - Todos os agendamentos
- `PATCH /api/admin/agendamentos/<id>/status/` - Atualizar status

## 🎨 Pages (URLs HTML)

- `/` - Home
- `/servicos/` - Catálogo de serviços
- `/contato/` - Contato
- `/galeria/` - Galeria
- `/auth/` - Login/Registro
- `/agendar/` - Criar agendamento
- `/perfil/` - Perfil do usuário
- `/historico/` - Histórico de agendamentos
- `/admin-painel/` - Dashboard administrativo

## 🚀 Deploy

### Vercel (Recomendado)

1. Instale Vercel CLI:
```bash
npm install -g vercel
```

2. Configure variáveis de ambiente na Vercel:
```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=.vercel.app
WHATSAPP_PHONE=5545999417111
```

3. Deploy:
```bash
vercel --prod
```

### Railway

1. Conecte seu repositório no Railway
2. Configure as mesmas variáveis de ambiente
3. Deploy automático!

## 📊 Dados Iniciais

Para popular o banco com dados de exemplo:

```bash
python manage.py shell
```

```python
from servicos.models import Servico
from barbeiros.models import Barbeiro
from users.models import User

# Criar usuário admin
admin = User.objects.create_superuser(
    email='admin@barbearia.com',
    password='admin123',
    name='Administrador'
)

# Criar barbeiro
barbeiro_user = User.objects.create_user(
    email='barbeiro@barbearia.com',
    password='barber123',
    name='João Silva',
    role='barber'
)

barbeiro = Barbeiro.objects.create(
    user=barbeiro_user,
    name='João Silva',
    specialty='Cortes clássicos',
    active=True,
    working_hours={
        "monday": {"active": True, "start": "08:00", "end": "18:00"},
        "tuesday": {"active": True, "start": "08:00", "end": "18:00"},
        "wednesday": {"active": True, "start": "08:00", "end": "18:00"},
        "thursday": {"active": True, "start": "08:00", "end": "18:00"},
        "friday": {"active": True, "start": "08:00", "end": "18:00"},
        "saturday": {"active": True, "start": "08:00", "end": "16:00"},
        "sunday": {"active": False}
    }
)

# Criar serviços
Servico.objects.create(
    name='Corte Social',
    description='Corte clássico e moderno',
    price=45.00,
    duration=30,
    category='haircut',
    active=True
)

Servico.objects.create(
    name='Barba Completa',
    description='Aparar e modelar com navalha',
    price=35.00,
    duration=30,
    category='beard',
    active=True
)

Servico.objects.create(
    name='Corte + Barba',
    description='Pacote completo',
    price=70.00,
    duration=60,
    category='combo',
    active=True
)

print("✅ Dados iniciais criados!")
```

## 🔧 Troubleshooting

### Erro: "No module named 'django'"
```bash
# Ative o venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Erro: Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Erro: CSRF token missing
```
Desabilite temporariamente no settings.py para testes:
CSRF_COOKIE_SECURE = False
```

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação ou entre em contato.

## 🎉 Pronto!

Sua aplicação Django está configurada e pronta para uso! 

**Próximos passos:**
1. ✅ Popular banco com dados iniciais
2. ✅ Testar localmente
3. ✅ Fazer deploy na Vercel/Railway
4. ✅ Configurar domínio customizado (opcional)

**Bom trabalho! 🚀**

