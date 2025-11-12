# 🔧 Troubleshooting - Soluções Rápidas

## 🚨 Problemas Comuns e Soluções

---

### ❌ Erro: "No module named 'django'"

**Causa:** Ambiente virtual não ativado ou Django não instalado

**Solução:**
```bash
# Windows
.\venv\Scripts\activate

# Se ainda der erro
pip install django
# ou
pip install -r requirements.txt
```

---

### ❌ Erro: "no such table: core_auditlog"

**Causa:** Migrations não aplicadas

**Solução:**
```bash
python manage.py migrate
```

---

### ❌ Erro: "403 Forbidden" ao acessar painel

**Causa:** Usuário não é administrador (is_staff=False)

**Solução:**
```bash
python manage.py shell
```
```python
from users.models import User

# Listar usuários
User.objects.all().values('id', 'name', 'email', 'is_staff')

# Tornar admin
user = User.objects.get(email='seu@email.com')  # ← SUBSTITUA
user.is_staff = True
user.is_superuser = True
user.save()

print(f"✅ {user.name} agora é admin!")
exit()
```

---

### ❌ Página em branco ou não carrega

**Causa:** Erro de JavaScript

**Solução:**
1. Abra Console do navegador (F12)
2. Veja mensagens de erro em vermelho
3. Verifique se HTMX/Alpine.js/Chart.js carregaram
4. Confirme que há dados no banco:
```bash
python manage.py shell
>>> from agendamentos.models import Agendamento
>>> Agendamento.objects.count()  # Deve retornar > 0
```

---

### ❌ Gráficos não aparecem

**Causa:** Chart.js não carregou ou sem dados

**Solução:**
1. Verifique conexão internet (Chart.js vem de CDN)
2. Abra F12 e veja se há erro
3. Confirme que há agendamentos no banco
4. Teste API diretamente: `http://localhost:8000/admin-painel/api/dashboard/stats/`

---

### ❌ "CSRF token missing"

**Causa:** Token CSRF não enviado no POST

**Solução:**
- O código já inclui `'X-CSRFToken': '{{ csrf_token }}'` em todos os POSTs
- Se ainda der erro, certifique-se que está usando o template correto
- Verifique se middleware CSRF está ativo em settings.py

---

### ❌ WhatsApp não abre

**Causa:** Formato de telefone incorreto

**Solução:**
- Use formato: (45) 99999-9999
- O sistema remove caracteres não numéricos automaticamente
- Verifique `core/whatsapp.py`

---

### ❌ "OperationalError: no such column"

**Causa:** Estrutura do banco desatualizada

**Solução:**
```bash
# Opção 1: Aplicar migrations
python manage.py migrate

# Opção 2: Se der erro, fake a migration
python manage.py migrate core --fake

# Opção 3: Recriar banco (CUIDADO: perde dados!)
del db.sqlite3
python manage.py migrate
python populate_db.py
```

---

### ❌ Templates não encontrados (404)

**Causa:** Caminho do template incorreto

**Solução:**
- Verifique se arquivo existe em `templates/admin/`
- Confirme que `base_admin.html` está lá
- Verifique settings.py:
```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],  # ← Deve estar assim
        ...
    }
]
```

---

### ❌ CSS não carrega (página sem estilo)

**Causa:** Arquivos estáticos não encontrados

**Solução:**
```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Verificar configuração
python manage.py findstatic css/admin-dashboard.css
```

---

### ❌ "ImportError: cannot import name"

**Causa:** Função importada não existe no arquivo

**Solução:**
- Verifique o nome da função no arquivo de origem
- Confirme que o arquivo foi criado corretamente
- Exemplo: se `dashboard_views.py` não existe, crie-o

---

### ❌ Dados não atualizam automaticamente

**Causa:** Auto-refresh não funciona

**Solução:**
1. Abra Console (F12)
2. Veja erros de JavaScript
3. Verifique se Alpine.js está carregado
4. Force refresh manual (Ctrl+R)
5. Limpe cache do navegador

---

### ❌ Modal não abre ao clicar "Novo"

**Causa:** Alpine.js não inicializou

**Solução:**
1. F12 → Console → veja erros
2. Confirme que Alpine.js CDN está carregando
3. Verifique se há `x-cloak` style no template
4. Recarregue a página

---

### ❌ "500 Internal Server Error"

**Causa:** Erro no código Python

**Solução:**
```bash
# Ver logs detalhados
python manage.py runserver

# Ou ver arquivo de log
type logs\django.log

# Ou com DEBUG=True, ver stacktrace no navegador
```

---

### ❌ Usuário não consegue fazer login

**Causa:** Senha incorreta ou usuário inativo

**Solução:**
```bash
python manage.py shell
```
```python
from users.models import User

# Resetar senha
user = User.objects.get(email='email@exemplo.com')
user.set_password('nova_senha_123')
user.is_active = True
user.save()
```

---

### ❌ "Permission Denied" em arquivos

**Causa:** Permissões do Windows

**Solução:**
- Execute CMD/PowerShell como Administrador
- Ou verifique permissões da pasta do projeto

---

### ❌ Porta 8000 já em uso

**Causa:** Outro processo usando a porta

**Solução:**
```bash
# Usar outra porta
python manage.py runserver 8001

# Ou matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 🔍 Diagnóstico Rápido

### Teste 1: Django Funciona?
```bash
python manage.py --version
```
✅ Deve mostrar versão do Django (ex: 4.2.x)

### Teste 2: Banco de Dados OK?
```bash
python manage.py showmigrations
```
✅ Todas as migrations devem ter [X]

### Teste 3: Admin Existe?
```bash
python manage.py shell
```
```python
from users.models import User
admins = User.objects.filter(is_staff=True)
print(f"Admins: {admins.count()}")
for admin in admins:
    print(f"- {admin.name} ({admin.email})")
```
✅ Deve mostrar pelo menos 1 admin

### Teste 4: URLs Funcionam?
```bash
python manage.py show_urls | findstr admin-painel
```
✅ Deve listar todas as URLs do painel

### Teste 5: Templates Existem?
```bash
dir templates\admin
```
✅ Deve mostrar todos os templates .html

---

## 🆘 Problemas Não Listados?

### Passos de Diagnóstico:

1. **Ativar DEBUG**
```python
# settings.py ou .env
DEBUG=True
```

2. **Ver Logs Detalhados**
```bash
# Terminal com runserver mostra erros
python manage.py runserver

# Ou ver arquivo
type logs\django.log
```

3. **Testar API Diretamente**
```bash
# Usar navegador ou curl
http://localhost:8000/admin-painel/api/dashboard/stats/
```

4. **Verificar Console do Navegador**
- F12 → Console
- Procurar erros em vermelho
- Ver Network tab para requests falhando

5. **Testar no Shell**
```bash
python manage.py shell
```
```python
# Testar imports
from admin_painel.dashboard_views import dashboard_view
from core.models import AuditLog
from core.decorators import admin_required

print("✅ Todos os imports funcionaram!")
```

---

## 📞 Recursos de Ajuda

### Documentação
- **Django:** https://docs.djangoproject.com/
- **HTMX:** https://htmx.org/docs/
- **Alpine.js:** https://alpinejs.dev/
- **Chart.js:** https://www.chartjs.org/docs/

### Comandos Úteis
```bash
# Ver todas as URLs
python manage.py show_urls

# Verificar migrations
python manage.py showmigrations

# Criar superuser
python manage.py createsuperuser

# Shell interativo
python manage.py shell

# Verificar configuração
python manage.py check
```

---

## ✅ Lista de Verificação Pré-Execução

Antes de reportar problema, verifique:

- [ ] Ambiente virtual ativado
- [ ] Django instalado (`pip list | findstr Django`)
- [ ] Migrations aplicadas (`python manage.py migrate`)
- [ ] Usuário admin existe (`is_staff=True`)
- [ ] Servidor rodando sem erros
- [ ] Browser atualizado (Chrome/Firefox/Edge)
- [ ] JavaScript habilitado no navegador
- [ ] Conexão internet OK (para CDNs)

---

## 🎯 Teste Rápido de Funcionamento

Execute este script para verificar tudo:

```bash
python manage.py shell
```

```python
from users.models import User
from agendamentos.models import Agendamento
from barbeiros.models import Barbeiro
from servicos.models import Servico
from core.models import AuditLog

print("=== VERIFICAÇÃO DO SISTEMA ===\n")

print(f"✅ Usuários: {User.objects.count()}")
print(f"   - Admins: {User.objects.filter(is_staff=True).count()}")

print(f"✅ Agendamentos: {Agendamento.objects.count()}")
print(f"✅ Barbeiros: {Barbeiro.objects.count()}")
print(f"✅ Serviços: {Servico.objects.count()}")
print(f"✅ Logs Auditoria: {AuditLog.objects.count()}")

print("\n=== TUDO OK! ===")
```

Se tudo passar: **Sistema está OK!** ✅

---

## 🎊 Ainda com Problemas?

1. Releia **START_HERE.md**
2. Execute passo a passo do **COMANDOS_EXECUCAO.md**
3. Verifique **PAINEL_ADMIN_COMPLETO.md**
4. Confira este troubleshooting novamente

**Se nada resolver:**
- Verifique logs em `logs/django.log`
- Teste com `DEBUG=True`
- Recrie o ambiente virtual
- Reinstale dependências

---

## 💡 Dica Final

Na maioria dos casos, 90% dos problemas são resolvidos por:

1. ✅ Ativar ambiente virtual
2. ✅ Aplicar migrations
3. ✅ Ter usuário com is_staff=True
4. ✅ Limpar cache do navegador

**Boa sorte!** 🍀

