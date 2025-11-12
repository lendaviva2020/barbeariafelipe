# 🚀 COMANDOS PARA EXECUTAR O PAINEL ADMIN

## ⚡ Start Rápido (3 passos)

```bash
# 1. Ativar ambiente virtual
cd c:\Users\98911\OneDrive\Desktop\barbearia-django
.\venv\Scripts\activate

# 2. Criar admin (se necessário)
python manage.py shell
```

No shell:
```python
from users.models import User
user = User.objects.get(email='seu@email.com')  # Substitua pelo seu email
user.is_staff = True
user.is_superuser = True
user.save()
print(f"✅ {user.name} agora é administrador!")
exit()
```

```bash
# 3. Executar servidor
python manage.py runserver
```

**Acesse:** http://localhost:8000/admin-painel/dashboard/

---

## 📋 Checklist de Verificação

Antes de usar, verifique:

- [ ] Ambiente virtual ativado
- [ ] Django instalado (`python -c "import django; print(django.get_version())"`)
- [ ] Banco de dados migrado (`python manage.py migrate`)
- [ ] Usuário com `is_staff=True` criado
- [ ] Servidor rodando

---

## 🧪 Teste de Cada Seção

### 1. Dashboard
```
URL: http://localhost:8000/admin-painel/dashboard/
```
- [ ] Cards de métricas carregam
- [ ] Gráfico de faturamento aparece
- [ ] Gráfico de status aparece
- [ ] Ações rápidas funcionam

### 2. Agendamentos
```
URL: http://localhost:8000/admin-painel/appointments/
```
- [ ] Lista de agendamentos carrega
- [ ] Filtros funcionam
- [ ] Botão "Confirmar" funciona
- [ ] Botão "Completar" funciona
- [ ] WhatsApp abre

### 3. Barbeiros
```
URL: http://localhost:8000/admin-painel/barbers/
```
- [ ] Lista de barbeiros carrega
- [ ] Modal de criar abre
- [ ] Criar barbeiro funciona
- [ ] Editar barbeiro funciona
- [ ] Toggle ativo/inativo funciona

### 4. Serviços
```
URL: http://localhost:8000/admin-painel/services/
```
- [ ] Lista de serviços carrega
- [ ] Filtros funcionam
- [ ] CRUD completo funciona

### 5. Cupons
```
URL: http://localhost:8000/admin-painel/coupons/
```
- [ ] Lista de cupons carrega
- [ ] Criar cupom funciona
- [ ] Copiar código funciona
- [ ] Status atualiza corretamente

### 6. Usuários
```
URL: http://localhost:8000/admin-painel/users/
```
- [ ] Lista de usuários carrega
- [ ] Tornar admin funciona
- [ ] Filtros funcionam

### 7. Logs de Auditoria
```
URL: http://localhost:8000/admin-painel/audit-logs/
```
- [ ] Logs aparecem
- [ ] Filtros funcionam
- [ ] Detalhes expandem
- [ ] Exportar CSV funciona

### 8. Lista de Espera
```
URL: http://localhost:8000/admin-painel/waiting-list/
```
- [ ] Lista carrega
- [ ] Notificar WhatsApp funciona
- [ ] Atualizar status funciona

### 9. Relatórios
```
URL: http://localhost:8000/admin-painel/reports/
```
- [ ] Métricas carregam
- [ ] Gráficos aparecem
- [ ] Filtro de período funciona

### 10. Performance
```
URL: http://localhost:8000/admin-painel/performance/
```
- [ ] Métricas do sistema aparecem
- [ ] Auto-refresh funciona

---

## 🔧 Comandos Úteis

### Gerenciar Usuários
```bash
# Listar todos os usuários
python manage.py shell
>>> from users.models import User
>>> User.objects.all().values('id', 'name', 'email', 'is_staff')

# Tornar usuário admin
>>> user = User.objects.get(email='email@exemplo.com')
>>> user.is_staff = True
>>> user.save()

# Remover permissão admin
>>> user.is_staff = False
>>> user.save()
```

### Ver Logs de Auditoria
```bash
python manage.py shell
>>> from core.models import AuditLog
>>> logs = AuditLog.objects.all()[:10]
>>> for log in logs:
...     print(f"{log.user.name if log.user else 'Sistema'} - {log.action} em {log.table_name}")
```

### Limpar Logs Antigos (Manutenção)
```bash
python manage.py shell
>>> from core.models import AuditLog
>>> from datetime import datetime, timedelta
>>> # Deletar logs com mais de 90 dias
>>> old_date = datetime.now() - timedelta(days=90)
>>> AuditLog.objects.filter(created_at__lt=old_date).delete()
```

### Popular Banco de Dados (Teste)
```bash
# Use os scripts existentes
python populate_db.py
python populate_services.py
```

---

## 🎯 URLs Principais (Bookmark)

Salve estes links no seu navegador:

```
Dashboard:       http://localhost:8000/admin-painel/dashboard/
Agendamentos:    http://localhost:8000/admin-painel/appointments/
Barbeiros:       http://localhost:8000/admin-painel/barbers/
Serviços:        http://localhost:8000/admin-painel/services/
Cupons:          http://localhost:8000/admin-painel/coupons/
Usuários:        http://localhost:8000/admin-painel/users/
Logs:            http://localhost:8000/admin-painel/audit-logs/
Lista Espera:    http://localhost:8000/admin-painel/waiting-list/
Relatórios:      http://localhost:8000/admin-painel/reports/
Performance:     http://localhost:8000/admin-painel/performance/
```

---

## 💾 Backup de Dados

Sempre faça backup antes de mudanças grandes:

```bash
# Backup do banco SQLite
copy db.sqlite3 db.sqlite3.backup

# Ou usar dumpdata
python manage.py dumpdata > backup.json
```

---

## 🎉 Você Está Pronto!

Execute estes 3 comandos e comece a usar:

```bash
.\venv\Scripts\activate
python manage.py runserver
# Acesse: http://localhost:8000/admin-painel/dashboard/
```

**BOA SORTE COM SEU PAINEL ADMIN!** 🚀

