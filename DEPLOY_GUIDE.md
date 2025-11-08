# 🚀 Guia de Deploy - Barbearia Django

## 📋 Pré-requisitos

✅ Projeto Django funcionando localmente  
✅ Conta na Vercel ou Railway  
✅ Git configurado  

## 🎯 Deploy na Vercel

### PASSO 1: Preparar o Projeto

```bash
# Garantir que está tudo OK
python manage.py check
python manage.py collectstatic --noinput
```

### PASSO 2: Criar Repositório Git

```bash
git init
git add .
git commit -m "feat: projeto Django completo"
git branch -M main
git remote add origin [SEU_REPOSITORIO_GIT]
git push -u origin main
```

### PASSO 3: Conectar na Vercel

1. Acesse: https://vercel.com/new
2. Clique em "Import Git Repository"
3. Selecione seu repositório
4. Configure:
   - Framework Preset: **Other**
   - Build Command: `bash vercel_build.sh`
   - Output Directory: **deixe vazio**

### PASSO 4: Configurar Variáveis de Ambiente

Na Vercel, vá em Settings → Environment Variables e adicione:

```
SECRET_KEY=django-prod-secret-key-change-this-to-random-string
DEBUG=False
ALLOWED_HOSTS=.vercel.app
WHATSAPP_PHONE=5545999417111
```

### PASSO 5: Deploy!

Clique em **"Deploy"** e aguarde 2-3 minutos.

---

## 🎯 Deploy no Railway

### PASSO 1: Criar Conta

1. Acesse: https://railway.app
2. Conecte com GitHub

### PASSO 2: Novo Projeto

1. Clique em "New Project"
2. Selecione "Deploy from GitHub repo"
3. Escolha seu repositório

### PASSO 3: Variáveis de Ambiente

No Railway, configure:

```
SECRET_KEY=django-prod-secret-key
DEBUG=False
ALLOWED_HOSTS=.railway.app
WHATSAPP_PHONE=5545999417111
```

### PASSO 4: Deploy Automático

Railway detecta o Procfile e faz deploy automaticamente!

---

## ✅ Verificações Pós-Deploy

### 1. Site Carrega?
```
Acesse: https://seu-projeto.vercel.app
```

### 2. Admin Funciona?
```
Acesse: https://seu-projeto.vercel.app/django-admin/
Login com superuser
```

### 3. API Funciona?
```
GET https://seu-projeto.vercel.app/api/servicos/
Deve retornar lista de serviços
```

### 4. Login Funciona?
```
Vá em /auth/
Tente fazer login
```

---

## 🐛 Troubleshooting

### Erro: "Internal Server Error"

**Solução:**
```
1. Veja logs no Vercel/Railway
2. Verifique variáveis de ambiente
3. Verifique se DEBUG=False em produção
4. Rode: python manage.py check --deploy
```

### Erro: Static files não carregam

**Solução:**
```
1. Execute: python manage.py collectstatic
2. Verifique STATIC_ROOT no settings.py
3. Verifique WhiteNoise no MIDDLEWARE
```

### Erro: "DisallowedHost"

**Solução:**
```
Adicione o domínio da Vercel/Railway em ALLOWED_HOSTS:
ALLOWED_HOSTS=.vercel.app,.railway.app
```

---

## 📊 Comandos Úteis

### Ver logs (local)
```bash
python manage.py runserver --noreload
```

### Criar superuser (produção)
```bash
python manage.py createsuperuser
```

### Backup do banco
```bash
python manage.py dumpdata > backup.json
```

### Restaurar backup
```bash
python manage.py loaddata backup.json
```

---

## 🎉 Pronto!

Sua aplicação Django está no ar! 🚀

**URLs importantes:**
- Site: https://seu-projeto.vercel.app
- Admin: https://seu-projeto.vercel.app/django-admin/
- API: https://seu-projeto.vercel.app/api/

**Próximos passos:**
1. ✅ Configurar domínio customizado
2. ✅ Adicionar dados iniciais
3. ✅ Testar todas as funcionalidades
4. ✅ Monitorar logs de erro

**Boa sorte! 🎊**

