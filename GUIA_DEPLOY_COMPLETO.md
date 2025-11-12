# 🚀 GUIA COMPLETO DE DEPLOY - BARBEARIA DJANGO

## 📋 Índice
1. [Preparação Inicial](#preparação-inicial)
2. [Deploy Local (Teste)](#deploy-local-teste)
3. [Deploy com Docker](#deploy-com-docker)
4. [Deploy em Servidor VPS](#deploy-em-servidor-vps)
5. [Deploy no Heroku](#deploy-no-heroku)
6. [Deploy no Railway](#deploy-no-railway)
7. [Pós-Deploy](#pós-deploy)

---

## ✅ STATUS ATUAL
- ✅ Sistema verificado e funcionando
- ✅ 234 arquivos estáticos coletados
- ✅ Todas as verificações de segurança aprovadas
- ✅ Banco de dados funcionando
- ✅ Health check implementado
- ✅ Pronto para deploy!

---

## 1️⃣ PREPARAÇÃO INICIAL

### Checklist Pré-Deploy
```bash
# 1. Verificar se tudo está funcionando
python manage.py check --deploy

# 2. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 3. Executar migrations
python manage.py migrate

# 4. Criar superusuário (se ainda não criou)
python manage.py createsuperuser
```

### Configurar Variáveis de Ambiente
Copie `.env.example` para `.env` e configure:

```env
# Django
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Database
DATABASE_URL=postgres://user:password@localhost:5432/barbearia

# Redis (opcional)
REDIS_URL=redis://localhost:6379/0

# APIs (opcional)
GEMINI_API_KEY=sua-chave-api-gemini
TWILIO_ACCOUNT_SID=seu-sid-twilio
TWILIO_AUTH_TOKEN=seu-token-twilio
TWILIO_WHATSAPP_NUMBER=+14155238886

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
```

---

## 2️⃣ DEPLOY LOCAL (TESTE)

### Opção 1: Django Development Server (NÃO USAR EM PRODUÇÃO)
```bash
python manage.py runserver 0.0.0.0:8000
```

### Opção 2: Gunicorn (Recomendado)
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar
gunicorn barbearia.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Testar Localmente
```bash
# Abrir no navegador
http://localhost:8000

# Testar health check
http://localhost:8000/health/

# Testar admin
http://localhost:8000/admin/
```

---

## 3️⃣ DEPLOY COM DOCKER

### Passo 1: Build da Imagem
```bash
# Build da imagem Docker
docker build -t barbearia-django .

# Verificar imagem criada
docker images
```

### Passo 2: Executar com Docker Compose
```bash
# Iniciar todos os serviços
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Verificar status
docker-compose -f docker-compose.prod.yml ps
```

### Passo 3: Configurar Banco de Dados
```bash
# Executar migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Criar superusuário
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Coletar static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### Passo 4: Acessar Aplicação
```
http://localhost:8000 - Aplicação
http://localhost:8000/admin/ - Painel Admin
http://localhost:8000/health/ - Health Check
```

### Comandos Úteis Docker
```bash
# Parar serviços
docker-compose -f docker-compose.prod.yml down

# Restart
docker-compose -f docker-compose.prod.yml restart

# Rebuild
docker-compose -f docker-compose.prod.yml up -d --build

# Ver logs de um serviço específico
docker-compose -f docker-compose.prod.yml logs -f web

# Executar comandos dentro do container
docker-compose -f docker-compose.prod.yml exec web bash
```

---

## 4️⃣ DEPLOY EM SERVIDOR VPS (Ubuntu)

### Passo 1: Preparar Servidor
```bash
# Conectar ao servidor via SSH
ssh usuario@seu-servidor-ip

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git
```

### Passo 2: Configurar PostgreSQL
```bash
# Entrar no PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE barbearia;
CREATE USER barbearia_user WITH PASSWORD 'senha_segura';
ALTER ROLE barbearia_user SET client_encoding TO 'utf8';
ALTER ROLE barbearia_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE barbearia_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE barbearia TO barbearia_user;
\q
```

### Passo 3: Clonar Projeto
```bash
# Ir para diretório home
cd ~

# Clonar repositório (ou fazer upload via FTP)
git clone https://github.com/seu-usuario/barbearia-django.git
cd barbearia-django

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### Passo 4: Configurar .env
```bash
# Criar arquivo .env
nano .env

# Adicionar variáveis (copiar do exemplo acima)
# Salvar: Ctrl+X, Y, Enter
```

### Passo 5: Executar Migrations
```bash
# Com ambiente virtual ativado
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Passo 6: Configurar Gunicorn como Serviço
```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/gunicorn.service
```

Adicionar:
```ini
[Unit]
Description=Gunicorn daemon for Barbearia Django
After=network.target

[Service]
User=seu-usuario
Group=www-data
WorkingDirectory=/home/seu-usuario/barbearia-django
Environment="PATH=/home/seu-usuario/barbearia-django/venv/bin"
EnvironmentFile=/home/seu-usuario/barbearia-django/.env
ExecStart=/home/seu-usuario/barbearia-django/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          barbearia.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar e iniciar serviço
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

### Passo 7: Configurar Nginx
```bash
# Criar configuração do site
sudo nano /etc/nginx/sites-available/barbearia
```

Adicionar:
```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/seu-usuario/barbearia-django/staticfiles/;
    }

    location /media/ {
        alias /home/seu-usuario/barbearia-django/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/barbearia /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Permitir Nginx no firewall
sudo ufw allow 'Nginx Full'
```

### Passo 8: Configurar SSL com Let's Encrypt (HTTPS)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Certificado será renovado automaticamente
```

### Passo 9: Configurar Celery (Opcional)
```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/celery.service
```

Adicionar:
```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=seu-usuario
Group=www-data
WorkingDirectory=/home/seu-usuario/barbearia-django
Environment="PATH=/home/seu-usuario/barbearia-django/venv/bin"
EnvironmentFile=/home/seu-usuario/barbearia-django/.env
ExecStart=/home/seu-usuario/barbearia-django/venv/bin/celery -A barbearia worker --loglevel=info --detach

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar e iniciar
sudo systemctl start celery
sudo systemctl enable celery
```

---

## 5️⃣ DEPLOY NO HEROKU

### Passo 1: Preparar Projeto
```bash
# Instalar Heroku CLI
# Windows: https://devcenter.heroku.com/articles/heroku-cli
# Linux/Mac: curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login
```

### Passo 2: Criar App
```bash
# Criar novo app
heroku create nome-sua-barbearia

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:mini

# Adicionar Redis (opcional)
heroku addons:create heroku-redis:mini
```

### Passo 3: Configurar Variáveis
```bash
# Configurar SECRET_KEY
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Configurar DEBUG
heroku config:set DEBUG=False

# Configurar outras variáveis
heroku config:set ALLOWED_HOSTS=.herokuapp.com
heroku config:set DJANGO_SETTINGS_MODULE=barbearia.settings_prod

# Ver todas as configs
heroku config
```

### Passo 4: Deploy
```bash
# Adicionar remote
git remote add heroku https://git.heroku.com/nome-sua-barbearia.git

# Push para Heroku
git push heroku master

# Executar migrations
heroku run python manage.py migrate

# Criar superusuário
heroku run python manage.py createsuperuser

# Coletar static files
heroku run python manage.py collectstatic --noinput

# Abrir app
heroku open
```

### Passo 5: Ver Logs
```bash
# Ver logs em tempo real
heroku logs --tail

# Ver logs específicos
heroku logs --source app --tail
```

---

## 6️⃣ DEPLOY NO RAILWAY

### Passo 1: Preparar Projeto
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login
```

### Passo 2: Criar Projeto
```bash
# Inicializar Railway no projeto
railway init

# Adicionar PostgreSQL
railway add --plugin postgresql

# Adicionar Redis (opcional)
railway add --plugin redis
```

### Passo 3: Configurar Variáveis
```bash
# No painel Railway (railway.app)
# Vá em Variables e adicione:

SECRET_KEY=sua-chave-secreta
DEBUG=False
ALLOWED_HOSTS=.railway.app
DATABASE_URL=postgresql://... (gerado automaticamente)
REDIS_URL=redis://... (gerado automaticamente)
```

### Passo 4: Deploy
```bash
# Deploy
railway up

# Ver logs
railway logs

# Executar comandos
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic --noinput
```

---

## 7️⃣ PÓS-DEPLOY

### Verificações Importantes
```bash
# 1. Testar Health Check
curl https://seudominio.com/health/

# 2. Testar Admin
curl https://seudominio.com/admin/

# 3. Verificar Static Files
curl https://seudominio.com/static/css/style.css

# 4. Verificar SSL
curl -I https://seudominio.com
```

### Configurar Backups Automáticos
```bash
# No servidor VPS
crontab -e

# Adicionar backup diário às 3h da manhã
0 3 * * * /home/seu-usuario/barbearia-django/backup.sh
```

### Monitoramento
```bash
# 1. Configurar UptimeRobot ou Pingdom
# https://uptimerobot.com (grátis)

# 2. Monitorar /health/ endpoint

# 3. Configurar alertas por email
```

### Performance
```bash
# 1. Ativar Gzip no Nginx (já está no nginx.conf)
# 2. Configurar CDN para static files
# 3. Usar Redis para cache
# 4. Configurar Database Index
```

---

## 🆘 TROUBLESHOOTING

### Problema: "502 Bad Gateway"
```bash
# Verificar status do Gunicorn
sudo systemctl status gunicorn

# Ver logs
sudo journalctl -u gunicorn

# Restart
sudo systemctl restart gunicorn
```

### Problema: "Static files não carregam"
```bash
# Verificar permissões
sudo chown -R seu-usuario:www-data /home/seu-usuario/barbearia-django/staticfiles

# Coletar novamente
python manage.py collectstatic --noinput

# Restart Nginx
sudo systemctl restart nginx
```

### Problema: "Database connection failed"
```bash
# Verificar PostgreSQL
sudo systemctl status postgresql

# Testar conexão
psql -U barbearia_user -d barbearia -h localhost

# Ver logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### Problema: "Celery não está funcionando"
```bash
# Verificar status
sudo systemctl status celery

# Ver logs
sudo journalctl -u celery

# Restart
sudo systemctl restart celery
```

---

## 📊 MONITORAMENTO

### Comandos Úteis
```bash
# Ver uso de recursos
htop

# Ver uso de disco
df -h

# Ver logs do Django
tail -f /var/log/gunicorn/access.log

# Ver logs do Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Ver conexões ativas
netstat -an | grep :80 | wc -l
```

### Métricas Importantes
- ✅ Uptime > 99.9%
- ✅ Response time < 200ms
- ✅ CPU usage < 70%
- ✅ Memory usage < 80%
- ✅ Disk usage < 80%

---

## 🎯 PRÓXIMOS PASSOS

### Melhorias Recomendadas
1. **Configurar CDN** (Cloudflare)
2. **Adicionar monitoring** (Sentry, New Relic)
3. **Configurar auto-scaling**
4. **Implementar CI/CD** (GitHub Actions)
5. **Adicionar testes automatizados**
6. **Configurar backup em cloud** (AWS S3, Google Cloud)

### Segurança
1. **Configurar fail2ban**
2. **Atualizar sistema regularmente**
3. **Fazer backup de .env**
4. **Rotacionar SECRET_KEY periodicamente**
5. **Monitorar logs de segurança**

---

## ✅ CHECKLIST FINAL

- [ ] Sistema funcionando em produção
- [ ] SSL/HTTPS configurado
- [ ] Backups automáticos configurados
- [ ] Monitoramento ativo
- [ ] Logs configurados
- [ ] Documentação atualizada
- [ ] Equipe treinada
- [ ] Plano de contingência definido

---

## 📞 SUPORTE

### Links Úteis
- [Django Documentation](https://docs.djangoproject.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)

### Comandos de Emergência
```bash
# Rollback rápido
git reset --hard HEAD~1
git push -f

# Restart completo
sudo systemctl restart gunicorn nginx postgresql redis

# Modo manutenção
# Criar arquivo: /home/seu-usuario/barbearia-django/maintenance.html
# Configurar Nginx para servir este arquivo
```

---

## 🎉 PARABÉNS!

Seu sistema está pronto para produção! 🚀

**Lembre-se:**
- Monitore sempre
- Faça backups regulares
- Mantenha sistema atualizado
- Teste antes de atualizar produção

---

**Última atualização:** 12 de Novembro de 2025
**Versão do Sistema:** 1.0.0
**Status:** ✅ PRONTO PARA PRODUÇÃO

