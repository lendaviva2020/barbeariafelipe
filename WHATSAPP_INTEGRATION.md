# 📱 Guia de Integração WhatsApp

Sistema completo de notificações WhatsApp com Twilio e fallback para wa.me.

## 📋 Índice

- [Configuração](#configuração)
- [Tipos de Notificações](#tipos-de-notificações)
- [Twilio Setup](#twilio-setup)
- [Uso](#uso)
- [Troubleshooting](#troubleshooting)

## ⚙️ Configuração

### Opção 1: Básica (wa.me)

Funciona sem configuração adicional, abre WhatsApp Web com mensagem pré-preenchida.

Adicione ao `.env`:

```bash
WHATSAPP_PHONE=5545999417111
```

### Opção 2: Avançada (Twilio API)

Envio automático via API do Twilio.

## 🚀 Twilio Setup

### 1. Criar Conta Twilio

1. Acesse [Twilio.com](https://www.twilio.com/try-twilio)
2. Cadastre-se gratuitamente
3. Verifique seu número de telefone

### 2. Obter Credenciais

No Dashboard do Twilio:

1. Copie o **Account SID**
2. Copie o **Auth Token**
3. Anote o número WhatsApp do Twilio

### 3. Configurar WhatsApp Sandbox

Para testes (gratuito):

1. Console > Messaging > Try it out > Try WhatsApp
2. Siga instruções para conectar seu WhatsApp
3. Envie mensagem "join [seu-código]" para o número sandbox

Para produção:

1. Solicite aprovação do WhatsApp Business
2. Configure número WhatsApp próprio
3. Processo pode levar alguns dias

### 4. Configurar Variáveis de Ambiente

Adicione ao `.env`:

```bash
# Twilio WhatsApp API
TWILIO_ACCOUNT_SID=AC1234567890abcdef
TWILIO_AUTH_TOKEN=sua_auth_token_aqui
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 5. Instalar Dependências

```bash
pip install twilio==8.11.0
```

### 6. Testar Integração

```bash
python manage.py shell
```

```python
from core.whatsapp import send_notification
from agendamentos.models import Agendamento

# Enviar notificação de teste
appointment = Agendamento.objects.first()
result = send_notification(appointment, 'confirmation', appointment.user)
print(result)
```

## 📬 Tipos de Notificações

### 1. Confirmação (confirmation)

Enviada quando agendamento é criado/confirmado.

```
🔥 AGENDAMENTO CONFIRMADO 🔥

👤 Cliente: João Silva
📞 Telefone: (45) 99999-9999
✂️ Serviço: Corte + Barba
💰 Valor: R$ 50.00
📅 Data: 15/11/2025
⏰ Horário: 14:00
💈 Barbeiro: Francisco

📍 Local: Rua José R Filho, N° 150...
```

### 2. Lembrete (reminder)

Enviada 1 dia antes do agendamento.

```
⏰ Lembrete de Agendamento

Olá João!

Lembrete: seu agendamento é amanhã!
📅 Data: 15/11/2025
🕐 Horário: 14:00
✂️ Serviço: Corte + Barba
💈 Barbeiro: Francisco
```

### 3. Conclusão (completed)

Enviada após conclusão do serviço.

```
✨ Obrigado pela Preferência!

Olá João!

Esperamos que tenha gostado do resultado! 😊

📸 Adoraríamos ver o resultado final!
Tire uma foto e envie para nós.

⭐ Não esqueça de deixar sua avaliação!
```

### 4. Cancelamento (cancellation)

Enviada quando agendamento é cancelado.

```
❌ Agendamento Cancelado

Olá João,

Seu agendamento foi cancelado.
📅 Data: 15/11/2025
🕐 Horário: 14:00
```

### 5. Reagendamento (rescheduled)

Enviada quando data/hora é alterada.

```
🔄 Agendamento Reagendado

Olá João!

Seu agendamento foi reagendado:
📅 Nova data: 16/11/2025
🕐 Novo horário: 15:00
✂️ Serviço: Corte + Barba
💈 Barbeiro: Francisco
```

## 💻 Uso

### Via API

```python
POST /api/notifications/send/
{
    "appointment_id": 123,
    "notification_type": "confirmation"
}
```

### Via Python

```python
from core.whatsapp import send_notification

result = send_notification(
    appointment=appointment,
    notification_type='confirmation',
    user=request.user
)

if result['success']:
    print("Enviado via Twilio!")
else:
    print(f"Fallback URL: {result['whatsapp_url']}")
```

### Via Celery (Automático)

Lembretes são enviados automaticamente via Celery:

```bash
# Iniciar Celery Worker
celery -A barbearia worker -l info

# Iniciar Celery Beat (tarefas periódicas)
celery -A barbearia beat -l info
```

## 🔧 Troubleshooting

### Erro "Invalid WhatsApp Phone Number"

**Problema**: Número não está registrado no Twilio

**Soluções**:

1. Verificar formato: +5545999999999
2. Registrar número no Sandbox (desenvolvimento)
3. Aprovar número com WhatsApp Business (produção)

### Erro "Twilio Authentication Failed"

**Problema**: Credenciais inválidas

**Soluções**:

1. Verificar TWILIO_ACCOUNT_SID
2. Verificar TWILIO_AUTH_TOKEN
3. Gerar novas credenciais se necessário

### Mensagens Não Chegam

**Problema**: API retorna sucesso mas mensagem não chega

**Soluções**:

1. Verificar se número está no Sandbox
2. Verificar se enviou "join [código]" primeiro
3. Verificar logs do Twilio Console
4. Verificar saldo da conta Twilio

### Erro 402 "Insufficient Funds"

**Problema**: Créditos Twilio esgotados

**Soluções**:

1. Adicionar créditos na conta Twilio
2. Usar modo gratuito (Sandbox) para testes
3. Usar fallback wa.me temporariamente

### Fallback para wa.me

Se Twilio falhar, sistema automaticamente:

1. Cria notificação com status 'failed'
2. Retorna URL wa.me
3. Usuário pode copiar/clicar no link

## 📊 Monitoramento

### Visualizar Notificações Enviadas

```
http://localhost:8000/api/notifications/
```

### Estatísticas

- Total enviadas
- Taxa de sucesso
- Erros comuns
- Tempo de entrega

### Logs

```bash
# Ver logs em tempo real
tail -f logs/django.log | grep WhatsApp

# Ver erros
tail -f logs/django.log | grep ERROR | grep whatsapp
```

## 🚀 Tarefas Automáticas

### Lembretes Diários

Configurado em `barbearia/celery.py`:

```python
# Executar diariamente às 18:00
'send-daily-reminders': {
    'task': 'core.tasks.send_reminder_notifications',
    'schedule': crontab(hour=18, minute=0),
}
```

### Retentar Envios Falhados

```python
# Executar a cada 6 horas
'retry-failed-notifications': {
    'task': 'core.tasks.retry_failed_notifications',
    'schedule': crontab(hour='*/6', minute=0),
}
```

## 💰 Custos

### Twilio Sandbox (Gratuito)

- Ideal para testes
- Limitado a números registrados
- Sem custos

### Twilio Produção

- ~$0.005 por mensagem
- Requer aprovação WhatsApp Business
- Taxa mensal do número

### Alternativa Gratuita

Usar apenas wa.me (sem Twilio):

- Gratuito
- Manual (abre WhatsApp)
- Sem envio automático

## 📞 Suporte

- [Twilio Docs](https://www.twilio.com/docs/whatsapp)
- [WhatsApp Business](https://business.whatsapp.com/)
- Código: `core/whatsapp.py`

