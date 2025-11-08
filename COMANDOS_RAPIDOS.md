# Comandos Rapidos - Barbearia Django

## RODAR O SERVIDOR

```powershell
cd C:\Users\98911\OneDrive\Desktop\barbearia-django
venv\Scripts\python.exe manage.py runserver
```

Acesse: http://localhost:8000

## PARAR O SERVIDOR

```
Ctrl + C no terminal
```

## POPULAR BANCO DE DADOS

```powershell
cd C:\Users\98911\OneDrive\Desktop\barbearia-django
venv\Scripts\python.exe populate_db.py
```

## CRIAR SUPERUSER NOVO

```powershell
venv\Scripts\python.exe manage.py createsuperuser
```

## FAZER MIGRACOES

```powershell
venv\Scripts\python.exe manage.py makemigrations
venv\Scripts\python.exe manage.py migrate
```

## COLETAR ARQUIVOS ESTATICOS

```powershell
venv\Scripts\python.exe manage.py collectstatic --noinput
```

## ABRIR SHELL DJANGO

```powershell
venv\Scripts\python.exe manage.py shell
```

## VERIFICAR PROJETO

```powershell
venv\Scripts\python.exe manage.py check
```

---

## CREDENCIAIS DE TESTE

### Admin:
- Email: admin@barbearia.com
- Senha: admin123

### Barbeiro:
- Email: joao@barbearia.com
- Senha: barber123

### Cliente:
- Email: cliente@teste.com
- Senha: cliente123

---

## PAGINAS DISPONIVEIS

- Home: http://localhost:8000/
- Servicos: http://localhost:8000/servicos/
- Contato: http://localhost:8000/contato/
- Galeria: http://localhost:8000/galeria/
- Login: http://localhost:8000/auth/
- Agendar: http://localhost:8000/agendar/
- Perfil: http://localhost:8000/perfil/
- Historico: http://localhost:8000/historico/
- Admin: http://localhost:8000/admin-painel/
- Django Admin: http://localhost:8000/django-admin/

---

## TESTAR API

### Listar servicos (publico):
```powershell
curl http://localhost:8000/api/servicos/
```

### Login:
```powershell
curl -X POST http://localhost:8000/api/users/login/ `
  -H "Content-Type: application/json" `
  -d '{"email":"cliente@teste.com","password":"cliente123"}'
```

---

## DEPLOY

Quando estiver pronto:
1. Crie repositorio Git
2. Suba para GitHub
3. Conecte na Vercel ou Railway
4. Configure variaveis de ambiente
5. Deploy automatico!

Veja: DEPLOY_GUIDE.md

---

Projeto: Barbearia Francisco Django
Data: 08/11/2025
Status: 100% FUNCIONAL

