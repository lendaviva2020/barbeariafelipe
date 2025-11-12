# 🤖 Guia de Chat com IA

Sistema de chat com inteligência artificial usando Google Gemini para responder automaticamente clientes.

## 📋 Índice

- [Configuração](#configuração)
- [Como Usar](#como-usar)
- [Personalização](#personalização)
- [Monitoramento](#monitoramento)
- [Troubleshooting](#troubleshooting)

## ⚙️ Configuração

### 1. Obter API Key do Google Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

### 2. Configurar Variáveis de Ambiente

Adicione ao seu arquivo `.env`:

```bash
GEMINI_API_KEY=sua_api_key_aqui
```

### 3. Instalar Dependências

```bash
pip install google-generativeai==0.3.2
```

### 4. Aplicar Migrações

```bash
python manage.py migrate
```

### 5. Configurar IA para Barbeiros

Acesse o painel admin e configure a IA para cada barbeiro:

```
http://localhost:8000/admin-painel/ia/settings/
```

## 📱 Como Usar

### Para Clientes

1. Acesse seu agendamento
2. Clique no botão "Chat"
3. Digite sua mensagem
4. A IA responderá automaticamente

### Para Barbeiros/Admin

1. Acesse "Monitoramento de Chat" no painel admin
2. Visualize mensagens que requerem atenção humana
3. Responda manualmente quando necessário

## 🎨 Personalização

### Personalidade da IA

Escolha entre dois estilos:

- **Amigável**: Tom descontraído e uso de emojis
- **Profissional**: Tom formal e objetivo

### Instruções Personalizadas

Adicione instruções específicas para cada barbeiro:

```
Sempre mencionar nossos serviços premium
Focar em produtos de cuidados com barba
Sempre perguntar se o cliente quer agendar serviço adicional
```

### Configurações Avançadas

- **Tamanho Máximo da Mensagem**: 100-5000 caracteres
- **Tempo de Resposta**: 1-60 segundos
- **Ativar/Desativar**: Toggle para habilitar/desabilitar IA

## 📊 Monitoramento

### Estatísticas Disponíveis

- Total de mensagens
- Mensagens respondidas pela IA
- Taxa de resposta da IA
- Mensagens que requerem atenção humana

### Detecção Automática de Atenção Humana

A IA detecta automaticamente quando precisa de intervenção humana:

- Solicitações de cancelamento
- Reagendamentos
- Reclamações
- Problemas técnicos

## 🔧 Troubleshooting

### IA não responde

**Problema**: Cliente envia mensagem mas não recebe resposta

**Soluções**:

1. Verificar se `GEMINI_API_KEY` está configurada
2. Verificar se IA está habilitada para o barbeiro
3. Verificar logs: `tail -f logs/django.log`
4. Testar API Key manualmente

### Respostas Inadequadas

**Problema**: IA dá respostas fora do contexto

**Soluções**:

1. Ajustar instruções personalizadas
2. Mudar personalidade (amigável <-> profissional)
3. Revisar histórico de conversas
4. Adicionar mais contexto nas instruções

### Erro "Rate Limit Exceeded"

**Problema**: Muitas requisições à API

**Soluções**:

1. Aguardar alguns minutos
2. Verificar plano da API Gemini
3. Implementar cache de respostas
4. Ajustar rate limiting no código

### Mensagens Não Sanitizadas

**Problema**: Caracteres especiais em mensagens

**Soluções**:

1. Sistema já sanitiza automaticamente
2. Verificar função `sanitize_input()` em `core/ai_chat.py`
3. Ajustar regex de sanitização se necessário

## 🚀 Boas Práticas

### 1. Monitoramento Regular

- Revisar diariamente mensagens que requerem atenção
- Responder manualmente quando necessário
- Ajustar instruções baseado em feedback

### 2. Testes Periódicos

- Enviar mensagens de teste
- Verificar qualidade das respostas
- Ajustar configurações conforme necessário

### 3. Backup de Configurações

- Documentar instruções personalizadas
- Fazer backup das configurações de IA
- Manter histórico de mudanças

### 4. Treinamento da Equipe

- Ensinar barbeiros a usar o monitoramento
- Explicar quando intervir manualmente
- Documentar casos especiais

## 📞 Suporte

Para mais informações ou suporte, consulte:

- [Documentação Django](https://docs.djangoproject.com/)
- [Google Gemini API](https://ai.google.dev/)
- Arquivo `core/ai_chat.py` para detalhes técnicos

