# ⚡ Comandos Rápidos - Sistema IA e Chat

## 🚀 Instalação e Configuração

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Aplicar Migrações
```bash
python manage.py migrate
```

### 3. Configurar .env
```bash
# Copiar exemplo
cp env.example .env

# Editar e adicionar:
GEMINI_API_KEY=sua_chave_aqui
TWILIO_ACCOUNT_SID=seu_sid (opcional)
TWILIO_AUTH_TOKEN=seu_token (opcional)
```

---

## 🤖 Sistema de IA

### Testar IA (Python Shell)
```bash
python manage.py shell
```

```python
from core.ai_chat import process_chat_message
from agendamentos.models import Agendamento
from users.models import User

# Buscar agendamento e usuário
appointment = Agendamento.objects.first()
user = User.objects.first()

# Enviar mensagem
result = process_chat_message(appointment, user, "Olá, qual o horário?")
print(result)
```

### Estatísticas da IA
```bash
python manage.py shell
```

```python
from core.ai_chat import get_ai_statistics

stats = get_ai_statistics()
print(stats)
```

---

## 📱 Notificações WhatsApp

### Enviar Notificação Manual
```bash
python manage.py shell
```

```python
from core.whatsapp import send_notification
from agendamentos.models import Agendamento
from users.models import User

appointment = Agendamento.objects.first()
user = User.objects.first()

# Tipos: 'confirmation', 'reminder', 'completed', 'cancellation', 'rescheduled'
result = send_notification(appointment, 'confirmation', user)
print(result)
```

### Testar Twilio
```bash
python manage.py shell
```

```python
from core.whatsapp import send_whatsapp_via_twilio

result = send_whatsapp_via_twilio(
    phone="5545999417111",
    message="Teste de mensagem WhatsApp!"
)
print(result)
```

---

## 🔄 Agendamentos Recorrentes

### Gerar Agendamentos (Próximos 7 dias)
```bash
python manage.py generate_recurring
```

### Gerar para Mais Dias
```bash
python manage.py generate_recurring --days=14
```

### Ver Apenas Estatísticas
```bash
python manage.py generate_recurring --stats-only
```

### Via Python
```bash
python manage.py shell
```

```python
from core.recurring_scheduler import generate_recurring_appointments

result = generate_recurring_appointments(days_ahead=7)
print(result)
```

---

## 🔥 Celery (Tarefas Automáticas)

### Iniciar Worker
```bash
celery -A barbearia worker -l info
```

### Iniciar Beat (Tarefas Periódicas)
```bash
celery -A barbearia beat -l info
```

### Ambos Juntos (Desenvolvimento)
```bash
celery -A barbearia worker -B -l info
```

### Executar Tarefa Manualmente
```bash
python manage.py shell
```

```python
from core.tasks import send_reminder_notifications

# Executar agora
result = send_reminder_notifications.delay()
print(result.get())
```

### Listar Tarefas Agendadas
```bash
python manage.py shell
```

```python
from celery import current_app

scheduled = current_app.conf.beat_schedule
for name, config in scheduled.items():
    print(f"{name}: {config['schedule']}")
```

---

## 🧪 Testes

### Executar Todos os Testes
```bash
pytest
```

### Testes Específicos
```bash
# IA
pytest core/tests/test_ai_chat.py -v

# WhatsApp
pytest core/tests/test_whatsapp.py -v
```

### Testes com Cobertura
```bash
pytest --cov=core --cov-report=html
```

---

## 📊 Monitoramento

### Ver Logs em Tempo Real
```bash
tail -f logs/django.log
```

### Ver Erros
```bash
tail -f logs/django.log | grep ERROR
```

### Ver Logs de IA
```bash
tail -f logs/django.log | grep "IA respondeu"
```

### Ver Logs de WhatsApp
```bash
tail -f logs/django.log | grep WhatsApp
```

---

## 🔧 Troubleshooting

### Verificar Configurações
```bash
python manage.py check
```

### Verificar Migrações Pendentes
```bash
python manage.py showmigrations
```

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Limpar Cache
```bash
python manage.py shell
```

```python
from django.core.cache import cache
cache.clear()
```

### Recriar Banco de Dados (CUIDADO!)
```bash
# Backup primeiro!
python manage.py dumpdata > backup.json

# Deletar banco
rm db.sqlite3

# Recriar
python manage.py migrate

# Restaurar (se necessário)
python manage.py loaddata backup.json
```

---

## 📱 Acessar Interfaces

### Frontend de Chat
```
http://localhost:8000/chat/<appointment_id>/
```

### Painel Admin - Configurações de IA
```
http://localhost:8000/admin-painel/ia/settings/
```

### Painel Admin - Monitoramento de Chat
```
http://localhost:8000/admin-painel/chat/monitoring/
```

### API - Estatísticas de IA
```
http://localhost:8000/api/ai/stats/
```

### API - Notificações
```
http://localhost:8000/api/notifications/
```

---

## 🚀 Produção

### Coletar Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### Executar com Gunicorn
```bash
gunicorn barbearia.wsgi:application --bind 0.0.0.0:8000
```

### Celery em Background
```bash
# Worker
celery -A barbearia worker -l info --detach

# Beat
celery -A barbearia beat -l info --detach
```

### Verificar Status Celery
```bash
celery -A barbearia inspect active
celery -A barbearia inspect stats
```

---

## 🔐 Segurança

### Gerar Nova SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Testar Rate Limiting
```bash
# Enviar 100 requisições rápidas
for i in {1..100}; do
  curl -X POST http://localhost:8000/api/chat/send/ \
    -H "Content-Type: application/json" \
    -d '{"appointment_id": 1, "message": "Test"}' &
done
```

---

## 📦 Backup e Restore

### Backup Completo
```bash
# Banco de dados
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Arquivos estáticos e media
tar -czf static_backup_$(date +%Y%m%d).tar.gz static/ media/
```

### Restore
```bash
# Restaurar banco
python manage.py loaddata backup_20251112.json

# Restaurar arquivos
tar -xzf static_backup_20251112.tar.gz
```

---

## 🎯 Quick Start Completo

### Setup Inicial (1ª vez)
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar .env
cp env.example .env
# Editar .env com suas chaves

# 3. Migrar banco
python manage.py migrate

# 4. Criar admin
python manage.py createsuperuser

# 5. Rodar servidor
python manage.py runserver

# 6. (Opcional) Rodar Celery
celery -A barbearia worker -B -l info
```

### Desenvolvimento Diário
```bash
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Celery (opcional)
celery -A barbearia worker -B -l info

# Terminal 3: Logs
tail -f logs/django.log
```

---

## 📞 APIs REST - Exemplos cURL

### Enviar Mensagem Chat
```bash
curl -X POST http://localhost:8000/api/chat/send/ \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": 1,
    "message": "Olá, preciso de ajuda"
  }'
```

### Buscar Histórico
```bash
curl http://localhost:8000/api/chat/history/1/
```

### Enviar Notificação WhatsApp
```bash
curl -X POST http://localhost:8000/api/notifications/send/ \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": 1,
    "notification_type": "confirmation"
  }'
```

### Estatísticas IA
```bash
curl http://localhost:8000/api/ai/stats/
```

---

## ✅ Checklist Pós-Instalação

- [ ] Dependências instaladas
- [ ] Migrações aplicadas
- [ ] .env configurado
- [ ] GEMINI_API_KEY funcionando
- [ ] Redis rodando (para Celery)
- [ ] Celery worker rodando
- [ ] Celery beat rodando
- [ ] IA respondendo mensagens
- [ ] WhatsApp enviando (wa.me ou Twilio)
- [ ] Agendamentos recorrentes gerando
- [ ] Testes passando
- [ ] Logs sendo gerados

---

**✨ Pronto para usar!**

