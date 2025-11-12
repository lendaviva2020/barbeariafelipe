# 🇧🇷 DEPLOY NO BRASIL - GUIA COMPLETO

## 📍 Servidores e Plataformas Brasileiras

Este guia mostra como fazer deploy em servidores e plataformas populares no Brasil.

---

## 1️⃣ HOSTINGER (Mais Popular no Brasil)

### Especificações
- ✅ Preço: R$ 6,99/mês (compartilhado) até R$ 149/mês (VPS)
- ✅ Suporte em português
- ✅ Pagamento em R$
- ✅ Datacenters no Brasil

### Passo a Passo

#### Opção A: Hospedagem Compartilhada (Mais Barata)
```bash
# 1. Contratar plano Premium ou Business (com SSH)

# 2. Conectar via SSH
ssh u123456@seu-dominio.com

# 3. Preparar ambiente
cd public_html
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configurar .htaccess para Django
# (A Hostinger tem tutoriais específicos)
```

**Limitação:** Hospedagem compartilhada não é ideal para Django em produção.

#### Opção B: VPS Hostinger (Recomendado)
```bash
# 1. Contratar VPS (recomendado: VPS 2 - R$ 39/mês)

# 2. Escolher Ubuntu 22.04

# 3. Conectar via SSH
ssh root@seu-ip

# 4. Seguir o guia de VPS deste documento
```

**Site:** https://www.hostinger.com.br/vps-hospedagem

---

## 2️⃣ UMBLER (Django-Friendly)

### Especificações
- ✅ Plataforma brasileira
- ✅ Suporte a Django nativo
- ✅ Deploy via Git
- ✅ Preço: R$ 19/mês a R$ 149/mês

### Passo a Passo
```bash
# 1. Criar conta em https://www.umbler.com

# 2. Criar novo app Django no painel

# 3. Conectar repositório Git
git remote add umbler <url-fornecida>

# 4. Criar arquivo Procfile na raiz do projeto
echo "web: gunicorn barbearia.wsgi:application" > Procfile

# 5. Configurar requirements.txt
pip freeze > requirements.txt

# 6. Fazer push
git add .
git commit -m "Deploy inicial"
git push umbler master

# 7. Configurar variáveis de ambiente no painel
# SECRET_KEY
# DEBUG=False
# ALLOWED_HOSTS

# 8. Executar migrations no console do Umbler
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

**Vantagens:** Deploy automático via Git, suporte brasileiro, fácil configuração.

**Site:** https://www.umbler.com

---

## 3️⃣ LOCAWEB (Grande no Brasil)

### Especificações
- ✅ Maior empresa de hosting no Brasil
- ✅ Suporte 24/7 em português
- ✅ VPS e Cloud Server
- ✅ Preço: R$ 60/mês a R$ 300/mês (VPS)

### Passo a Passo
```bash
# 1. Contratar Cloud Server Linux

# 2. Escolher Ubuntu 22.04

# 3. Acessar painel de controle

# 4. Configurar SSH

# 5. Seguir guia de deploy VPS (similar ao guia principal)
```

**Diferencial:** Suporte técnico robusto em português.

**Site:** https://www.locaweb.com.br

---

## 4️⃣ DIGITAL OCEAN (Internacional, aceita cartão BR)

### Especificações
- ✅ Aceita cartão brasileiro
- ✅ Datacenter em São Paulo
- ✅ Preço: $6/mês (~R$ 30/mês)
- ✅ Muito estável

### Passo a Passo
```bash
# 1. Criar conta em https://www.digitalocean.com

# 2. Criar Droplet (VPS)
# - Escolher Ubuntu 22.04
# - Região: São Paulo
# - Plano: Basic ($6/mês)

# 3. Conectar via SSH
ssh root@seu-droplet-ip

# 4. Executar script de deploy
cd /root
git clone seu-repositorio
cd barbearia-django
chmod +x deploy_automated.sh
./deploy_automated.sh

# 5. Configurar domínio no DNS
# Adicionar registro A apontando para o IP do Droplet
```

**Vantagem:** Performance excelente, datacenter em SP, interface intuitiva.

**Site:** https://www.digitalocean.com

---

## 5️⃣ CONTABO (Melhor Custo-Benefício)

### Especificações
- ✅ Europeia mas aceita BR
- ✅ Preço: €4,50/mês (~R$ 25/mês)
- ✅ 4 CPUs, 8GB RAM
- ✅ Muito barato para o hardware

### Passo a Passo
```bash
# 1. Criar conta em https://contabo.com

# 2. Escolher VPS S
# - 4 vCPU Cores
# - 8 GB RAM
# - 200 GB SSD
# - €4,50/mês

# 3. Escolher Ubuntu 22.04

# 4. Aguardar setup (até 24h)

# 5. Receber credenciais por email

# 6. Conectar e fazer deploy
ssh root@seu-vps-ip
```

**Vantagem:** Hardware excelente pelo preço.

**Site:** https://contabo.com

---

## 6️⃣ RENDER (Grátis para começar!)

### Especificações
- ✅ Plano gratuito disponível
- ✅ Deploy automático via Git
- ✅ PostgreSQL grátis
- ✅ Fácil configuração

### Passo a Passo
```bash
# 1. Criar conta em https://render.com

# 2. Criar novo Web Service

# 3. Conectar repositório GitHub

# 4. Configurar:
# - Environment: Python 3
# - Build Command: pip install -r requirements.txt
# - Start Command: gunicorn barbearia.wsgi:application

# 5. Adicionar PostgreSQL (grátis)

# 6. Configurar variáveis de ambiente:
SECRET_KEY=...
DEBUG=False
DATABASE_URL=${{Postgres.DATABASE_URL}}
ALLOWED_HOSTS=.onrender.com

# 7. Deploy automático!
```

**Vantagem:** Grátis para começar, fácil de usar.

**Limitação:** Plano gratuito tem sleep após 15 min de inatividade.

**Site:** https://render.com

---

## 7️⃣ RAILWAY (Alternativa ao Heroku)

### Especificações
- ✅ $5/mês de crédito grátis
- ✅ Deploy via Git
- ✅ PostgreSQL e Redis inclusos
- ✅ Interface moderna

### Passo a Passo
```bash
# 1. Criar conta em https://railway.app

# 2. New Project > Deploy from GitHub

# 3. Conectar repositório

# 4. Adicionar PostgreSQL

# 5. Configurar variáveis:
SECRET_KEY=...
DEBUG=False
DATABASE_URL=${{Postgres.DATABASE_URL}}

# 6. Deploy automático!

# 7. Executar migrations
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

**Vantagem:** Muito fácil, interface moderna.

**Site:** https://railway.app

---

## 8️⃣ VERCEL (Apenas com adaptações)

### ⚠️ Atenção
Vercel é otimizado para Next.js/Node.js. Django precisa de adaptações.

**Alternativa:** Use Vercel apenas para frontend e hospede o Django em outro lugar.

---

## 🎯 COMPARAÇÃO DE PREÇOS (Mensal em R$)

| Plataforma | Grátis | Básico | Intermediário | Pro |
|------------|--------|--------|---------------|-----|
| **Render** | ✅ Sim | - | R$ 35 | R$ 140 |
| **Railway** | ✅ $5 crédito | R$ 25 | R$ 50 | R$ 100 |
| **Hostinger VPS** | ❌ | R$ 39 | R$ 69 | R$ 149 |
| **Umbler** | ❌ | R$ 19 | R$ 49 | R$ 149 |
| **Digital Ocean** | ❌ | R$ 30 | R$ 60 | R$ 120 |
| **Contabo** | ❌ | R$ 25 | R$ 50 | R$ 100 |
| **Locaweb** | ❌ | R$ 60 | R$ 150 | R$ 300 |

---

## 💳 FORMAS DE PAGAMENTO ACEITAS NO BRASIL

### Cartão de Crédito Brasileiro
- ✅ Digital Ocean
- ✅ Contabo
- ✅ Render
- ✅ Railway
- ✅ Hostinger
- ✅ Locaweb
- ✅ Umbler

### Boleto Bancário
- ✅ Hostinger
- ✅ Locaweb
- ✅ Umbler

### PIX
- ✅ Hostinger (alguns planos)
- ✅ Locaweb
- ✅ Umbler

---

## 🇧🇷 RECOMENDAÇÕES POR PERFIL

### Para Iniciantes
**Recomendado:** Railway ou Render
- Deploy fácil via Git
- Plano gratuito para testar
- Documentação clara

### Para Pequenos Negócios
**Recomendado:** Hostinger VPS ou Umbler
- Suporte em português
- Preço acessível em R$
- Pagamento em boleto/PIX

### Para Performance
**Recomendado:** Digital Ocean (SP) ou Contabo
- Melhor hardware
- Datacenter em SP (DO)
- Preço competitivo

### Para Escala
**Recomendado:** Digital Ocean ou AWS
- Auto-scaling
- Load balancers
- Infraestrutura robusta

---

## 🔧 CONFIGURAÇÃO DE DOMÍNIO BRASILEIRO (.com.br)

### Registro.br (Domínios .com.br, .net.br, etc.)
```bash
# 1. Registrar domínio em https://registro.br

# 2. Configurar DNS
# Adicionar registro A:
# Host: @
# Type: A
# Value: IP-DO-SEU-SERVIDOR
# TTL: 3600

# Adicionar registro A para www:
# Host: www
# Type: A
# Value: IP-DO-SEU-SERVIDOR
# TTL: 3600

# 3. Aguardar propagação (até 48h)

# 4. Configurar SSL
sudo certbot --nginx -d seudominio.com.br -d www.seudominio.com.br
```

---

## 📊 CHECKLIST DE DEPLOY NO BRASIL

- [ ] Servidor escolhido e contratado
- [ ] Domínio registrado (.com.br ou .com)
- [ ] DNS configurado
- [ ] SSL/HTTPS ativo
- [ ] Backup configurado
- [ ] Email de notificações configurado
- [ ] WhatsApp configurado (Twilio)
- [ ] Sistema testado em produção
- [ ] Equipe treinada
- [ ] Documentação entregue

---

## 🆘 SUPORTE EM PORTUGUÊS

### Comunidades Brasileiras
- **Django Brasil:** https://github.com/django-brasil
- **Python Brasil:** https://python.org.br
- **Stack Overflow PT:** https://pt.stackoverflow.com

### Telegram
- Django Brasil
- Python Brasil
- Dev Brasil

### YouTube (Canais BR)
- Curso em Vídeo
- Hashtag Programação
- DevAprender

---

## 💰 CUSTOS ESTIMADOS MENSAIS (R$)

### Setup Mínimo
```
Servidor (Railway/Render): R$ 0-35
Domínio .com.br: R$ 40/ano (R$ 3,33/mês)
SSL: Grátis (Let's Encrypt)
-----------
Total: R$ 3-38/mês
```

### Setup Recomendado
```
VPS (Hostinger/DO): R$ 30-40
Domínio .com.br: R$ 40/ano (R$ 3,33/mês)
SSL: Grátis
Email (Google Workspace): R$ 25/mês (opcional)
Backup (Cloud): R$ 10/mês (opcional)
-----------
Total: R$ 33-78/mês
```

### Setup Profissional
```
VPS (Digital Ocean): R$ 60
Domínio .com.br: R$ 40/ano
SSL: Grátis
CDN (Cloudflare Pro): R$ 100/mês
Email: R$ 25/mês
Backup: R$ 30/mês
Monitoramento: R$ 50/mês
-----------
Total: R$ 265-300/mês
```

---

## 🎉 PRONTO PARA DECOLAR!

Escolha a plataforma que melhor se encaixa no seu orçamento e necessidades, e faça o deploy!

### Dica Final
Comece com o **plano gratuito do Render ou Railway** para testar. Depois, migre para um VPS quando precisar de mais recursos.

---

**Boa sorte com seu deploy!** 🚀🇧🇷

