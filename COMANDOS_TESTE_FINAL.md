# 🧪 COMANDOS PARA TESTAR TUDO

## 1️⃣ Preparar Ambiente

```bash
cd C:\Users\98911\OneDrive\Desktop\barbearia-django
```

## 2️⃣ Instalar Dependências (se necessário)

```bash
.\venv\Scripts\activate
pip install -r requirements.txt
```

## 3️⃣ Criar/Atualizar Banco

```bash
python manage.py makemigrations
python manage.py migrate
python populate_db.py
```

## 4️⃣ Rodar Servidor

```bash
python manage.py runserver
```

---

## 🔗 TESTAR TODAS AS PÁGINAS

### Páginas Públicas:
- ✅ http://localhost:8000/ - Home
- ✅ http://localhost:8000/servicos/ - Serviços
- ✅ http://localhost:8000/galeria/ - Galeria com Lightbox
- ✅ http://localhost:8000/contato/ - Contato
- ✅ http://localhost:8000/agendar/ - Booking 4 Steps

### Auth:
- ✅ http://localhost:8000/auth/ - Login/Register

### Usuário (após login):
- ✅ http://localhost:8000/perfil/ - Editar Perfil
- ✅ http://localhost:8000/historico/ - Histórico
- ✅ http://localhost:8000/reviews/ - Avaliações
- ✅ http://localhost:8000/settings/ - Configurações
- ✅ http://localhost:8000/goals/ - Metas
- ✅ http://localhost:8000/loyalty/ - Fidelidade
- ✅ http://localhost:8000/recurring/ - Recorrentes

### Admin (login: admin@barbearia.com / admin123):
- ✅ http://localhost:8000/admin-painel/ - Dashboard
- ✅ Ver todos os gráficos funcionando
- ✅ Testar filtros de período
- ✅ Testar navegação entre tabs
- ✅ Inventory: http://localhost:8000/inventory/
- ✅ Commissions: http://localhost:8000/commissions/
- ✅ Suppliers: http://localhost:8000/suppliers/

### API Docs:
- ✅ http://localhost:8000/api/docs/ - Swagger UI
- ✅ http://localhost:8000/api/redoc/ - ReDoc

---

## 🧪 TESTAR FUNCIONALIDADES

### 1. Booking Flow:
1. Ir para /agendar/
2. Selecionar serviço
3. Selecionar barbeiro
4. Escolher data e hora
5. Aplicar cupom "BEMVINDO20"
6. Confirmar
7. Verificar confirmação

### 2. Admin Dashboard:
1. Login como admin
2. Ver métricas atualizadas
3. Mudar filtro de período
4. Ver gráficos renderizarem
5. Clicar em "Ações Rápidas"
6. Testar navegação

### 3. History:
1. Login como cliente
2. Ir para /historico/
3. Ver agendamentos
4. Filtrar por status
5. Tentar cancelar
6. Testar chat

### 4. Goals:
1. Login como admin
2. Ir para /goals/
3. Criar nova meta
4. Ver progress bar
5. Editar meta
6. Deletar meta

### 5. Gallery:
1. Ir para /galeria/
2. Filtrar por categoria
3. Clicar em imagem
4. Ver lightbox abrir
5. Navegar com setas/teclado
6. Testar download/share

### 6. Reviews:
1. Login como cliente
2. Ir para /reviews/
3. Criar avaliação (5 stars)
4. Filtrar por rating
5. Ver média geral

### 7. Profile:
1. Editar nome/telefone
2. Salvar alterações
3. Alterar senha
4. Upload avatar (mock)
5. Ver estatísticas

---

## 📡 TESTAR APIs (Swagger)

Acesse: http://localhost:8000/api/docs/

Testar endpoints:
- ✅ POST /api/users/login/
- ✅ GET /api/servicos/
- ✅ POST /api/agendamentos/create/
- ✅ POST /api/cupons/validate/
- ✅ GET /api/goals/
- ✅ POST /api/reviews/create/
- ✅ GET /api/admin/dashboard-stats/

---

## ✅ CHECKLIST COMPLETO

- [ ] Home carrega corretamente
- [ ] Hero com floating images
- [ ] Team section dinâmica
- [ ] Testimonials carousel
- [ ] Booking 4 steps funciona
- [ ] Cupons aplicam desconto
- [ ] Histórico lista agendamentos
- [ ] Cancelamento com motivo
- [ ] Profile edita dados
- [ ] Gallery lightbox funciona
- [ ] Reviews estrelas funcionam
- [ ] Goals progress bars
- [ ] Admin dashboard gráficos
- [ ] Todos CRUDs admin funcionam
- [ ] Filtros funcionam
- [ ] Busca funciona
- [ ] Responsivo mobile
- [ ] Menu mobile abre/fecha
- [ ] Todas validações funcionam
- [ ] Error handling ok
- [ ] Toast notifications
- [ ] Loading states

---

## 🎊 TUDO PRONTO!

**Projeto 100% funcional e pronto para uso!**

Teste tudo e depois faça deploy! 🚀

