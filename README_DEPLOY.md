# 🚀 DEPLOY RÁPIDO - BARBEARIA DJANGO

## ⚡ INÍCIO RÁPIDO

### Opção 1: Deploy Local (MAIS FÁCIL)
```bash
# 1. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar migrations
python manage.py migrate

# 4. Criar superusuário
python manage.py createsuperuser

# 5. Coletar static files
python manage.py collectstatic --noinput

# 6. Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

**Pronto!** Acesse: `http://localhost:8000`

---

### Opção 2: Deploy com Docker (RECOMENDADO)
```bash
# 1. Construir e iniciar
docker-compose -f docker-compose.prod.yml up -d

# 2. Executar migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# 3. Criar superusuário
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# 4. Coletar static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

**Pronto!** Acesse: `http://localhost:8000`

---

### Opção 3: Script Automatizado
```bash
# Dar permissão de execução
chmod +x deploy_automated.sh

# Executar
./deploy_automated.sh

# Escolher opção no menu
```

---

## 📋 PRÉ-REQUISITOS

### Para Deploy Local
- ✅ Python 3.11+
- ✅ pip
- ✅ Ambiente virtual (venv)

### Para Deploy Docker
- ✅ Docker
- ✅ Docker Compose

### Para Deploy em Produção
- ✅ Servidor VPS (Ubuntu 20.04+)
- ✅ Domínio próprio
- ✅ Acesso SSH

---

## ⚙️ CONFIGURAÇÃO

### 1. Variáveis de Ambiente
Copie `.env.example` para `.env`:
```bash
cp .env.example .env
```

### 2. Edite o arquivo `.env`:
```env
# OBRIGATÓRIO
SECRET_KEY=cole-uma-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,localhost

# BANCO DE DADOS (opcional, usa SQLite por padrão)
DATABASE_URL=postgresql://user:password@localhost:5432/barbearia

# REDIS (opcional)
REDIS_URL=redis://localhost:6379/0

# APIs (opcional)
GEMINI_API_KEY=sua-chave-gemini
TWILIO_ACCOUNT_SID=seu-sid
TWILIO_AUTH_TOKEN=seu-token
```

### 3. Gerar SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🌐 DEPLOY EM PRODUÇÃO

### Passo 1: Servidor VPS
```bash
# Conectar ao servidor
ssh usuario@seu-servidor-ip

# Clonar projeto
git clone https://github.com/seu-usuario/barbearia-django.git
cd barbearia-django

# Executar script de setup
chmod +x deploy_automated.sh
./deploy_automated.sh
```

### Passo 2: Configurar Domínio
1. Configure DNS apontando para o IP do servidor
2. Aguarde propagação (pode levar até 48h)

### Passo 3: Configurar SSL (HTTPS)
```bash
# No servidor
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

**Pronto!** Acesse: `https://seudominio.com`

---

## 🎯 ACESSO AO SISTEMA

### URLs Principais
- **Site:** `http://localhost:8000/`
- **Admin:** `http://localhost:8000/admin/`
- **API:** `http://localhost:8000/api/`
- **Health Check:** `http://localhost:8000/health/`
- **Documentação API:** `http://localhost:8000/api/docs/`

### Credenciais Padrão
Depois de criar o superusuário, use:
- **Email:** (definido na criação)
- **Senha:** (definida na criação)

---

## 🔧 COMANDOS ÚTEIS

### Desenvolvimento
```bash
# Rodar servidor
python manage.py runserver

# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Shell Django
python manage.py shell

# Ver rotas
python manage.py show_urls
```

### Docker
```bash
# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Parar containers
docker-compose -f docker-compose.prod.yml down

# Restart
docker-compose -f docker-compose.prod.yml restart

# Rebuild
docker-compose -f docker-compose.prod.yml up -d --build

# Entrar no container
docker-compose -f docker-compose.prod.yml exec web bash
```

### Produção (VPS)
```bash
# Ver logs do Gunicorn
sudo journalctl -u gunicorn -f

# Restart Gunicorn
sudo systemctl restart gunicorn

# Ver logs do Nginx
sudo tail -f /var/log/nginx/error.log

# Restart Nginx
sudo systemctl restart nginx

# Ver status dos serviços
sudo systemctl status gunicorn nginx postgresql redis
```

---

## 🐛 PROBLEMAS COMUNS

### 1. "502 Bad Gateway"
```bash
sudo systemctl restart gunicorn nginx
```

### 2. "Static files não carregam"
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### 3. "Database connection failed"
```bash
sudo systemctl status postgresql
python manage.py migrate
```

### 4. "Port 8000 already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

## 📚 DOCUMENTAÇÃO COMPLETA

- **Guia Completo:** `GUIA_DEPLOY_COMPLETO.md`
- **Produção:** `PRONTO_PARA_PRODUCAO.md`
- **Checklist:** `CHECKLIST_PRODUCAO.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`
- **Índice:** `INDICE_COMPLETO.md`

---

## ✅ CHECKLIST PRÉ-DEPLOY

Antes de fazer deploy em produção:

- [ ] `.env` configurado
- [ ] `SECRET_KEY` gerada e segura
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Banco de dados configurado
- [ ] Migrations executadas
- [ ] Superusuário criado
- [ ] Static files coletados
- [ ] Sistema verificado (`python manage.py check --deploy`)
- [ ] Backups configurados
- [ ] SSL/HTTPS configurado
- [ ] Monitoramento ativo

---

## 📊 STATUS DO SISTEMA

### ✅ Funcionalidades Implementadas
- ✅ Sistema de agendamentos
- ✅ Gestão de barbeiros
- ✅ Gestão de serviços
- ✅ Sistema de cupons
- ✅ Painel administrativo
- ✅ Dashboard com métricas
- ✅ Relatórios
- ✅ API RESTful
- ✅ Sistema de notificações
- ✅ Chat com IA (opcional)
- ✅ WhatsApp (opcional)
- ✅ Programa de fidelidade
- ✅ Lista de espera
- ✅ Sistema de avaliações
- ✅ Controle de estoque
- ✅ Comissões
- ✅ Metas
- ✅ E muito mais!

### 🔧 Tecnologias
- **Backend:** Django 5.1
- **Frontend:** HTML, CSS, JavaScript
- **Banco de Dados:** PostgreSQL (produção) / SQLite (dev)
- **Cache:** Redis (opcional)
- **API:** Django REST Framework
- **Tarefas:** Celery (opcional)
- **IA:** Google Gemini (opcional)
- **WhatsApp:** Twilio (opcional)
- **Servidor:** Gunicorn + Nginx
- **Container:** Docker + Docker Compose

---

## 🎉 PRONTO!

Seu sistema de barbearia está **100% funcional** e pronto para uso!

### Próximos Passos
1. **Testar localmente** primeiro
2. **Configurar domínio** e SSL
3. **Fazer backup** regularmente
4. **Monitorar** o sistema
5. **Treinar equipe**

### Suporte
- Leia a documentação completa
- Verifique os arquivos de troubleshooting
- Revise os logs em caso de erro

---

**Versão:** 1.0.0  
**Status:** ✅ PRONTO PARA PRODUÇÃO  
**Última atualização:** 12 de Novembro de 2025

---

## 🚀 BOM DEPLOY!

> "A melhor hora para fazer deploy foi ontem. A segunda melhor hora é agora!" 😄

