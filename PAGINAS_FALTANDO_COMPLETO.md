# 📋 TODAS AS PÁGINAS E CÓDIGOS QUE FALTAM EXTRAIR DO REACT

**Data:** Novembro 2025  
**Status:** EM EXTRAÇÃO

---

## 🔴 PRIORIDADE CRÍTICA (15 PÁGINAS)

### 1. **History.tsx → historico.html** ✅ (EM PROGRESSO)
- **Linhas:** 553
- **Componentes:**
  - HistorySkeleton
  - EmptyHistoryState
  - StatusBadge (Pendente, Confirmado, Completado, Cancelado)
  - AppointmentCard
  - CancelDialog
  - ChatDialog
- **Funcionalidades:**
  - Filtros por status (tabs)
  - Listagem paginada
  - Cancelamento com motivo
  - Chat de suporte
  - Verificação de prazo (2h antes)
  - Display de desconto
  - Foto de referência
- **APIs necessárias:** ✅ Já tem GET, precisa POST cancel
- **CSS:** ✅ Criado (history.css)
- **JS:** ❌ Precisa criar (history.js)

### 2. **Goals.tsx → goals.html**
- **Linhas:** 556
- **Componentes:**
  - GoalsSkeleton
  - EmptyGoalsState
  - GoalFormDialog
  - GoalCard
- **Funcionalidades:**
  - CRUD completo de metas
  - Metas por barbeiro ou gerais
  - 3 tipos: revenue, appointments, customer_satisfaction
  - Progress bar
  - Status (ativa, completa, expirada, cancelada)
  - Período customizável
- **APIs necessárias:** ❌ GET /api/goals/, POST /api/goals/, PUT, DELETE
- **CSS:** ❌ Precisa criar (goals.css)
- **JS:** ❌ Precisa criar (goals.js)

### 3. **Gallery.tsx → galeria.html** ✅ (BÁSICA JÁ EXISTE)
- **Linhas:** 447
- **Componentes:**
  - GallerySkeleton
  - GalleryItem
  - Lightbox (modal de visualização)
- **Funcionalidades:**
  - Grid Masonry responsivo
  - Filtros por categoria
  - Lightbox com navegação (Esc, arrows)
  - Compartilhamento
  - Download de imagens
  - Lazy loading
  - Featured badges
- **APIs necessárias:** ✅ Pode usar static files
- **CSS:** ❌ Precisa expandir (gallery.css completo com lightbox)
- **JS:** ❌ Precisa criar (gallery.js com lightbox)

### 4. **Coupons.tsx (ADMIN) → admin/coupons.html**
- **Linhas:** 595
- **Componentes:**
  - CouponsSkeleton
  - EmptyCouponsState
  - CouponFormDialog
  - CouponCard
  - CouponStatus
- **Funcionalidades:**
  - CRUD completo admin
  - Validação de código
  - 2 tipos: percentage, fixed
  - Limite de uso
  - Data de expiração
  - Status (ativo, expirado, limite atingido)
  - Copy código
  - Delete confirmation
- **APIs necessárias:** ✅ JÁ TEM (cupons/ urls criadas)
- **CSS:** ❌ Precisa criar (admin-coupons.css)
- **JS:** ❌ Precisa criar (admin-coupons.js)

### 5. **Admin/Appointments.tsx → admin/appointments.html**
- **Linhas:** ~800 (estimado)
- **Componentes:**
  - AppointmentsList
  - AppointmentDetails
  - StatusUpdateDialog
  - FiltersAdvanced
- **Funcionalidades:**
  - Lista TODOS agendamentos
  - Filtros avançados (data, status, barbeiro)
  - Busca por nome/telefone
  - Atualizar status
  - Visualizar detalhes completos
  - Exportar relatório
- **APIs necessárias:** ✅ Parcial (tem GET, precisa PATCH)
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 6. **Admin/Barbers.tsx → admin/barbers.html**
- **Linhas:** ~600 (estimado)
- **Componentes:**
  - BarbersList
  - BarberFormDialog
  - BarberCard
  - WorkingHoursEditor
- **Funcionalidades:**
  - CRUD barbeiros
  - Upload foto
  - Horários de trabalho (JSON editor)
  - Dias de folga
  - Especialidades
  - Status ativo/inativo
  - Estatísticas por barbeiro
- **APIs necessárias:** ❌ Tem GET, falta POST/PUT/DELETE
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 7. **Admin/Services.tsx → admin/services.html**
- **Linhas:** ~500 (estimado)
- **Componentes:**
  - ServicesList
  - ServiceFormDialog
  - ServiceCard
- **Funcionalidades:**
  - CRUD serviços
  - Upload imagem
  - Categorias
  - Preço e duração
  - Status ativo/inativo
  - Ordem de exibição
- **APIs necessárias:** ✅ JÁ TEM (servicos/admin/)
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 8. **Admin/Users.tsx → admin/users.html**
- **Linhas:** ~700 (estimado)
- **Componentes:**
  - UsersList
  - UserDetails
  - RoleEditor
  - ActivityLog
- **Funcionalidades:**
  - Lista todos usuários
  - Filtros (admin, barbeiro, cliente)
  - Ver detalhes
  - Editar roles
  - Desativar conta
  - Ver histórico
- **APIs necessárias:** ❌ GET /api/admin/users/, PATCH
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 9. **Admin/Reports.tsx → admin/reports.html**
- **Linhas:** ~900 (estimado)
- **Componentes:**
  - RevenueChart
  - TopServicesChart
  - BarbersPerformanceChart
  - PeriodSelector
  - ExportButtons
- **Funcionalidades:**
  - Múltiplos gráficos
  - Período customizável
  - Export PDF
  - Export Excel
  - Print
  - Comparação períodos
- **APIs necessárias:** ❌ GET /api/admin/reports/{type}/, POST /export-pdf/
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 10. **Profile.tsx → perfil.html** ✅ (BÁSICA JÁ EXISTE)
- **Linhas:** ~600 (estimado)
- **Componentes:**
  - ProfileHeader
  - EditProfileForm
  - PasswordChangeForm
  - AvatarUpload
  - DeleteAccountDialog
- **Funcionalidades:**
  - Visualizar perfil
  - Editar dados
  - Upload foto
  - Alterar senha
  - Deletar conta
- **APIs necessárias:** ❌ PATCH /api/users/me/, POST /upload-avatar/
- **CSS:** ❌ Precisa criar (profile.css completo)
- **JS:** ❌ Precisa criar (profile.js completo)

### 11. **Reviews.tsx → reviews.html**
- **Linhas:** ~500 (estimado)
- **Componentes:**
  - ReviewsList
  - ReviewForm
  - RatingStars
  - ReviewCard
- **Funcionalidades:**
  - Criar avaliação (rating 1-5)
  - Comentário
  - Ver avaliações públicas
  - Filtrar por nota
  - Aprovar (admin)
- **APIs necessárias:** ❌ GET /api/reviews/, POST
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 12. **Settings.tsx → settings.html**
- **Linhas:** ~400 (estimado)
- **Componentes:**
  - SettingsTabs
  - NotificationSettings
  - PrivacySettings
  - PreferencesSettings
- **Funcionalidades:**
  - Notificações (email, WhatsApp)
  - Privacidade
  - Tema (dark mode)
  - Idioma
- **APIs necessárias:** ❌ PATCH /api/users/settings/
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 13. **Inventory.tsx → inventory.html**
- **Linhas:** ~700 (estimado)
- **Componentes:**
  - ProductsList
  - ProductFormDialog
  - LowStockAlert
  - StockHistory
- **Funcionalidades:**
  - CRUD produtos
  - Controle de estoque
  - Alertas de estoque baixo
  - Histórico de movimentação
  - Categorias
- **APIs necessárias:** ❌ GET /api/products/, POST, PUT, DELETE
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 14. **Commissions.tsx → commissions.html**
- **Linhas:** ~600 (estimado)
- **Componentes:**
  - CommissionsList
  - CommissionCard
  - MonthSelector
  - PaymentDialog
- **Funcionalidades:**
  - Ver comissões (barbeiro)
  - Cálculo automático
  - Status (pendente, pago)
  - Relatório mensal
  - Marcar como pago (admin)
- **APIs necessárias:** ❌ GET /api/commissions/, POST /mark-paid/
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

### 15. **Suppliers.tsx → suppliers.html**
- **Linhas:** ~500 (estimado)
- **Componentes:**
  - SuppliersList
  - SupplierFormDialog
  - SupplierCard
- **Funcionalidades:**
  - CRUD fornecedores
  - CNPJ
  - Contatos
  - Termos de pagamento
  - Notas
- **APIs necessárias:** ❌ GET /api/suppliers/, POST, PUT, DELETE
- **CSS:** ❌ Precisa criar
- **JS:** ❌ Precisa criar

---

## 🟡 PRIORIDADE MÉDIA (5 PÁGINAS)

### 16. **Loyalty.tsx → loyalty.html**
- Programa de fidelidade
- Pontos e tiers
- Resgates
- Histórico

### 17. **RecurringAppointments.tsx → recurring.html**
- Agendamentos recorrentes
- Frequência (semanal, quinzenal, mensal)
- Gerenciar recorrências

### 18. **WaitingList.tsx → waiting-list.html**
- Lista de espera
- Notificações de vaga
- Admin manage

### 19. **AuditLogs.tsx → admin/audit-logs.html**
- Logs de auditoria
- Quem fez o quê e quando
- Filtros avançados

### 20. **Performance.tsx → admin/performance.html**
- Métricas de performance
- Tempo de resposta
- Uptime
- Estatísticas avançadas

---

## 🟢 PRIORIDADE BAIXA (10 COMPONENTES)

### Componentes Reutilizáveis Faltantes:

21. **ChatDialog** - Chat de suporte completo
22. **ImageCropper** - Crop de imagens no upload
23. **PDFViewer** - Visualizador de PDF embutido
24. **CalendarView** - Calendário visual para agendamentos
25. **NotificationsPanel** - Painel de notificações
26. **SearchBar** - Busca global avançada
27. **BulkActions** - Ações em massa (admin)
28. **ExportWizard** - Wizard de exportação
29. **OnboardingTour** - Tutorial guiado
30. **HelpCenter** - Central de ajuda

---

## 📊 RESUMO ESTATÍSTICO

### Páginas por Status:
- ✅ **Completas:** 2 (Home, Booking)
- 🔄 **Em Progresso:** 1 (History)
- ❌ **Faltando:** 27 páginas

### Total de Código Estimado:
- **React:** ~15.000 linhas
- **Para Extrair:** ~13.000 linhas
- **Progresso:** ~13% completo

### Arquivos por Criar:
- **Templates HTML:** 25
- **CSS:** 25
- **JavaScript:** 25
- **APIs/Views:** ~40 endpoints
- **Serializers:** ~15

---

## ⏱️ TEMPO ESTIMADO

### Por Prioridade:
- 🔴 **Crítica (15 páginas):** 20-30 horas
- 🟡 **Média (5 páginas):** 8-12 horas
- 🟢 **Baixa (10 componentes):** 10-15 horas

### Total: **38-57 horas de desenvolvimento**

---

## 🎯 PLANO DE AÇÃO RECOMENDADO

### Fase 1 (AGORA): Páginas Críticas Principais (8h)
1. ✅ History (em progresso)
2. Goals
3. Gallery (lightbox)
4. Coupons Admin

### Fase 2: Admin CRUD (12h)
5. Admin/Appointments
6. Admin/Barbers
7. Admin/Services
8. Admin/Users

### Fase 3: Usuário Avançado (8h)
9. Profile completo
10. Reviews
11. Settings
12. Reports

### Fase 4: Funcionalidades Avançadas (12h)
13. Inventory
14. Commissions
15. Suppliers
16. Loyalty

### Fase 5: Refinamento (10h)
17-30. Componentes extras e polish

---

## 🔥 COMEÇANDO AGORA

**Primeira página:** History.tsx (em progresso)

**Status:**
- ✅ Template HTML - CRIADO
- ✅ CSS - CRIADO (history.css)
- ❌ JavaScript - EM CRIAÇÃO
- ✅ API - JÁ EXISTE

**Próximas 3:**
- Goals.tsx
- Gallery.tsx (lightbox)
- Coupons Admin

