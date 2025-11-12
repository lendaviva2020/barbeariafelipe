# 🚀 Guia de Deploy para Produção

## ✅ Checklist Pré-Deploy

### 1. Segurança
- [ ] SECRET_KEY única e segura
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configurado
- [ ] HTTPS habilitado
- [ ] CORS configurado
- [ ] Senhas fortes no banco

### 2. Banco de Dados
- [ ] Backup completo
- [ ] PostgreSQL configurado
- [ ] Migrações aplicadas
- [ ] Índices otimizados

### 3. Arquivos Estáticos
- [ ] collectstatic executado
- [ ] WhiteNoise configurado
- [ ] Imagens otimizadas

### 4. APIs Externas
- [ ] GEMINI_API_KEY configurada
- [ ] TWILIO credenciais configuradas
- [ ] Redis configurado

### 5. Monitoramento
- [ ] Sentry configurado
- [ ] Logs funcionando
- [ ] Métricas ativas

---

## 🔧 CONFIGURAÇÃO DE PRODUÇÃO

### 1. Variáveis de Ambiente (.env)

```bash
# Django
SECRET_KEY=sua-chave-secreta-super-forte-aqui-minimo-50-caracteres
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com

# Banco de Dados (PostgreSQL)
DATABASE_URL=postgresql://usuario:senha@host:5432/barbearia_prod

# Redis
REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# APIs
GEMINI_API_KEY=sua_gemini_api_key_producao
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+5545999417111

# Email (Opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app

# Monitoramento
SENTRY_DSN=https://sua-chave@sentry.io/projeto

# CORS
CORS_ALLOWED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com
```

---

## 📦 DEPLOY NO SERVIDOR

### Opção 1: VPS (Ubuntu/Debian)

#### 1.1. Instalar Dependências do Sistema

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Python e ferramentas
sudo apt install python3.11 python3.11-venv python3-pip -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Redis
sudo apt install redis-server -y

# Nginx
sudo apt install nginx -y

# Supervisor (gerenciar processos)
sudo apt install supervisor -y

# Certbot (SSL)
sudo apt install certbot python3-certbot-nginx -y
```

#### 1.2. Criar Usuário e Diretórios

```bash
# Criar usuário
sudo adduser barbearia
sudo usermod -aG sudo barbearia

# Logar como usuário
sudo su - barbearia

# Criar diretórios
mkdir -p /home/barbearia/app
cd /home/barbearia/app
```

#### 1.3. Clonar e Configurar Projeto

```bash
# Clonar projeto (ajuste o caminho)
git clone https://github.com/seu-usuario/barbearia-django.git .

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

#### 1.4. Configurar PostgreSQL

```bash
# Entrar no PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE barbearia_prod;
CREATE USER barbearia_user WITH PASSWORD 'senha-super-forte-aqui';
ALTER ROLE barbearia_user SET client_encoding TO 'utf8';
ALTER ROLE barbearia_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE barbearia_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE barbearia_prod TO barbearia_user;
\q
```

#### 1.5. Configurar Aplicação

```bash
# Criar .env
nano .env
# (Copiar configurações de produção acima)

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Testar
python manage.py check --deploy
```

#### 1.6. Configurar Gunicorn

```bash
# Criar arquivo de configuração
nano /home/barbearia/app/gunicorn_config.py
```

```python
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
loglevel = "info"
accesslog = "/home/barbearia/app/logs/gunicorn_access.log"
errorlog = "/home/barbearia/app/logs/gunicorn_error.log"
```

#### 1.7. Configurar Supervisor (Gunicorn)

```bash
sudo nano /etc/supervisor/conf.d/barbearia.conf
```

```ini
[program:barbearia]
directory=/home/barbearia/app
command=/home/barbearia/app/venv/bin/gunicorn barbearia.wsgi:application -c /home/barbearia/app/gunicorn_config.py
user=barbearia
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/barbearia/app/logs/gunicorn_supervisor.log
environment=LANG=pt_BR.UTF-8,LC_ALL=pt_BR.UTF-8
```

#### 1.8. Configurar Supervisor (Celery Worker)

```bash
sudo nano /etc/supervisor/conf.d/barbearia-celery.conf
```

```ini
[program:barbearia-celery]
directory=/home/barbearia/app
command=/home/barbearia/app/venv/bin/celery -A barbearia worker -l info
user=barbearia
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/barbearia/app/logs/celery_worker.log
environment=LANG=pt_BR.UTF-8,LC_ALL=pt_BR.UTF-8
```

#### 1.9. Configurar Supervisor (Celery Beat)

```bash
sudo nano /etc/supervisor/conf.d/barbearia-celery-beat.conf
```

```ini
[program:barbearia-celery-beat]
directory=/home/barbearia/app
command=/home/barbearia/app/venv/bin/celery -A barbearia beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
user=barbearia
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/barbearia/app/logs/celery_beat.log
environment=LANG=pt_BR.UTF-8,LC_ALL=pt_BR.UTF-8
```

#### 1.10. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/barbearia
```

```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    client_max_body_size 10M;

    # Logs
    access_log /var/log/nginx/barbearia_access.log;
    error_log /var/log/nginx/barbearia_error.log;

    # Arquivos estáticos
    location /static/ {
        alias /home/barbearia/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Arquivos de media
    location /media/ {
        alias /home/barbearia/app/media/;
        expires 30d;
    }

    # Proxy para Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/barbearia /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

#### 1.11. Configurar SSL (Certbot)

```bash
# Obter certificado SSL gratuito
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Testar renovação automática
sudo certbot renew --dry-run
```

#### 1.12. Iniciar Serviços

```bash
# Criar diretório de logs
mkdir -p /home/barbearia/app/logs

# Atualizar Supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Iniciar serviços
sudo supervisorctl start barbearia
sudo supervisorctl start barbearia-celery
sudo supervisorctl start barbearia-celery-beat

# Verificar status
sudo supervisorctl status
```

---

### Opção 2: Docker

#### 2.1. Criar Dockerfile

```dockerfile
FROM python:3.11-slim

# Variáveis
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

# Copiar projeto
COPY . .

# Coletar estáticos
RUN python manage.py collectstatic --noinput

# Expor porta
EXPOSE 8000

# Comando
CMD ["gunicorn", "barbearia.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

#### 2.2. Criar docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=barbearia_prod
      - POSTGRES_USER=barbearia_user
      - POSTGRES_PASSWORD=senha-super-forte
    restart: always

  redis:
    image: redis:7-alpine
    restart: always

  web:
    build: .
    command: gunicorn barbearia.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: always

  celery:
    build: .
    command: celery -A barbearia worker -l info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: always

  celery-beat:
    build: .
    command: celery -A barbearia beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - certbot_conf:/etc/letsencrypt
      - certbot_www:/var/www/certbot
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
  static_volume:
  media_volume:
  certbot_conf:
  certbot_www:
```

#### 2.3. Executar Docker

```bash
# Build
docker-compose build

# Executar
docker-compose up -d

# Verificar
docker-compose ps

# Logs
docker-compose logs -f web

# Migrar banco
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser
```

---

### Opção 3: Vercel (Já Configurado)

O projeto já tem arquivos Vercel:

```bash
# Deploy
vercel --prod

# Ou via GitHub
git push origin master
# (Deploy automático se conectado)
```

---

## ⚙️ OTIMIZAÇÕES DE PRODUÇÃO

### 1. Settings de Produção

Criar `barbearia/settings_prod.py`:

```python
from .settings import *

# Segurança
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
        }
    }
}

# Logging
LOGGING['handlers']['file']['filename'] = '/var/log/barbearia/django.log'
```

### 2. Otimizar Banco de Dados

```sql
-- Criar índices adicionais
CREATE INDEX idx_agendamentos_date_status ON agendamentos_agendamento(appointment_date, status);
CREATE INDEX idx_chat_messages_appointment_created ON core_chatmessage(appointment_id, created_at);
CREATE INDEX idx_notifications_status_created ON core_notification(status, created_at);

-- Vacuum e analyze
VACUUM ANALYZE;
```

### 3. Configurar Logs Rotation

```bash
sudo nano /etc/logrotate.d/barbearia
```

```
/home/barbearia/app/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 barbearia barbearia
    sharedscripts
    postrotate
        supervisorctl restart barbearia
    endscript
}
```

### 4. Backup Automático

```bash
# Criar script de backup
nano /home/barbearia/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/barbearia/backups"

mkdir -p $BACKUP_DIR

# Backup do banco
pg_dump -U barbearia_user barbearia_prod | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup dos arquivos
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /home/barbearia/app/media

# Manter apenas últimos 30 dias
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup concluído: $DATE"
```

```bash
# Dar permissão
chmod +x /home/barbearia/backup.sh

# Adicionar ao cron (diário às 3h)
crontab -e
# Adicionar: 0 3 * * * /home/barbearia/backup.sh
```

---

## 🔒 SEGURANÇA EM PRODUÇÃO

### 1. Firewall

```bash
# UFW
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# Verificar
sudo ufw status
```

### 2. Fail2Ban (Proteção contra ataques)

```bash
# Instalar
sudo apt install fail2ban -y

# Configurar
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true
```

```bash
# Iniciar
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Gerar SECRET_KEY Segura

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📊 MONITORAMENTO

### 1. Configurar Sentry

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn=config('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False
    )
```

### 2. Health Check

```python
# core/views.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'database': check_database(),
        'redis': check_redis(),
        'celery': check_celery()
    })
```

### 3. Monitorar Celery

```bash
# Flower (UI para Celery)
pip install flower

# Executar
celery -A barbearia flower --port=5555

# Acessar: http://seu-servidor:5555
```

---

## 🚀 COMANDOS DE DEPLOY

### Deploy Inicial

```bash
# 1. Pull do código
git pull origin master

# 2. Ativar venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Migrar banco
python manage.py migrate

# 5. Coletar estáticos
python manage.py collectstatic --noinput

# 6. Reiniciar serviços
sudo supervisorctl restart barbearia
sudo supervisorctl restart barbearia-celery
sudo supervisorctl restart barbearia-celery-beat
```

### Deploy Rápido (Updates)

```bash
#!/bin/bash
# deploy.sh

cd /home/barbearia/app
git pull origin master
source venv/bin/activate
pip install -r requirements.txt --upgrade
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart barbearia
sudo supervisorctl restart barbearia-celery
sudo supervisorctl restart barbearia-celery-beat
echo "Deploy concluído!"
```

---

## 📈 PERFORMANCE

### 1. Cache de Queries

```python
# views.py
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutos
def lista_servicos(request):
    # ...
```

### 2. Database Indexes

```python
# models.py
class Meta:
    indexes = [
        models.Index(fields=['appointment_date', 'status']),
        models.Index(fields=['-created_at']),
    ]
```

### 3. Select Related / Prefetch

```python
# Otimizar queries
appointments = Agendamento.objects.select_related(
    'user', 'barber', 'service'
).prefetch_related(
    'chat_messages', 'notifications'
)
```

---

## 🔄 MANUTENÇÃO

### Comandos Úteis:

```bash
# Ver logs em tempo real
tail -f /home/barbearia/app/logs/gunicorn_error.log
tail -f /home/barbearia/app/logs/celery_worker.log

# Reiniciar serviços
sudo supervisorctl restart all

# Ver status
sudo supervisorctl status

# Backup manual
/home/barbearia/backup.sh

# Limpar sessões antigas
python manage.py clearsessions

# Gerar agendamentos recorrentes
python manage.py generate_recurring
```

---

## ✅ CHECKLIST FINAL

- [ ] Servidor configurado
- [ ] Nginx rodando
- [ ] PostgreSQL configurado
- [ ] Redis rodando
- [ ] Gunicorn rodando via Supervisor
- [ ] Celery Worker rodando
- [ ] Celery Beat rodando
- [ ] SSL configurado (HTTPS)
- [ ] Firewall ativo
- [ ] Backup automático configurado
- [ ] Logs rotation configurado
- [ ] Sentry configurado
- [ ] Domínio apontando
- [ ] Testes em produção passando

---

## 🎯 PÓS-DEPLOY

### 1. Testar Tudo

```bash
# Acessar site
curl https://seu-dominio.com

# Testar APIs
curl https://seu-dominio.com/api/ai/stats/

# Verificar Celery
sudo supervisorctl status barbearia-celery
```

### 2. Monitorar Primeiras 24h

- Verificar logs a cada hora
- Monitorar uso de memória/CPU
- Testar todas as funcionalidades
- Verificar envio de notificações

### 3. Documentar Credenciais

Guardar em local seguro:
- Senhas de banco
- API Keys
- Acessos SSH
- Credenciais Twilio/Gemini

---

## 📞 TROUBLESHOOTING PRODUÇÃO

### Erro 502 Bad Gateway

```bash
# Verificar se Gunicorn está rodando
sudo supervisorctl status barbearia

# Ver logs
tail -f /home/barbearia/app/logs/gunicorn_error.log

# Reiniciar
sudo supervisorctl restart barbearia
```

### Celery não executa tarefas

```bash
# Verificar worker
sudo supervisorctl status barbearia-celery

# Ver logs
tail -f /home/barbearia/app/logs/celery_worker.log

# Reiniciar
sudo supervisorctl restart barbearia-celery
sudo supervisorctl restart barbearia-celery-beat
```

### Arquivos estáticos não carregam

```bash
# Coletar novamente
python manage.py collectstatic --noinput --clear

# Verificar permissões
sudo chown -R barbearia:barbearia /home/barbearia/app/staticfiles

# Reiniciar Nginx
sudo systemctl restart nginx
```

---

## 🎊 PRONTO PARA PRODUÇÃO!

Seu sistema está **100% preparado** para deploy em produção com:

✅ Alta disponibilidade  
✅ Segurança robusta  
✅ Performance otimizada  
✅ Backup automático  
✅ Monitoramento completo  
✅ SSL/HTTPS  
✅ Logs estruturados  

**🚀 Bom deploy!** 🚀

