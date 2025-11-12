# 🎨 Biblioteca de Componentes UI - Django

Sistema completo de componentes reutilizáveis em Django equivalentes aos componentes React/Radix UI.

## 📋 Índice

- [Instalação](#instalação)
- [Componentes Disponíveis](#componentes-disponíveis)
- [Exemplos de Uso](#exemplos-de-uso)
- [Template Tags](#template-tags)
- [JavaScript](#javascript)

---

## ⚙️ Instalação

### 1. Incluir CSS e JavaScript no Base Template

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/components.css' %}">
    <script src="{% static 'js/ui-core.js' %}" defer></script>
    <script src="{% static 'js/components/accordion.js' %}" defer></script>
    <script src="{% static 'js/components/tabs.js' %}" defer></script>
    <script src="{% static 'js/components/dialog.js' %}" defer></script>
    <script src="{% static 'js/components/dropdown.js' %}" defer></script>
    <script src="{% static 'js/components/carousel.js' %}" defer></script>
    <script src="{% static 'js/components/popover.js' %}" defer></script>
    <script src="{% static 'js/components/tooltip.js' %}" defer></script>
    <script src="{% static 'js/components/slider.js' %}" defer></script>
    <script src="{% static 'js/components/switch.js' %}" defer></script>
    <script src="{% static 'js/components/command.js' %}" defer></script>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

### 2. Carregar Template Tags

```django
{% load ui_components %}
```

---

## 📦 Componentes Disponíveis

### Formulário (11 componentes)
- ✅ Input - Campo de texto
- ✅ Textarea - Área de texto
- ✅ Select - Seletor dropdown
- ✅ Checkbox - Caixa de seleção
- ✅ Radio Group - Grupo de rádios
- ✅ Switch - Toggle switch
- ✅ Slider - Controle deslizante
- ✅ Calendar - Seletor de data
- ✅ Date Range Picker - Intervalo de datas
- ✅ Input OTP - Input de código
- ✅ Form Field - Campo completo com label/erro

### Layout (6 componentes)
- ✅ Card - Card com header/footer
- ✅ Accordion - Accordion expansível
- ✅ Tabs - Sistema de abas
- ✅ Table - Tabela estilizada
- ✅ Separator - Linha separadora
- ✅ Scroll Area - Área com scroll customizado

### Navegação (7 componentes)
- ✅ Breadcrumb - Breadcrumb
- ✅ Pagination - Paginação
- ✅ Navigation Menu - Menu de navegação
- ✅ Menubar - Barra de menu
- ✅ Command - Command palette
- ✅ Dropdown Menu - Menu dropdown
- ✅ Context Menu - Menu de contexto

### Feedback (5 componentes)
- ✅ Alert - Alerta inline
- ✅ Toast - Notificação toast
- ✅ Progress - Barra de progresso
- ✅ Skeleton - Loading skeleton
- ✅ Badge - Badge/tag

### Overlay (7 componentes)
- ✅ Dialog - Modal dialog
- ✅ Alert Dialog - Dialog de confirmação
- ✅ Sheet - Drawer lateral
- ✅ Drawer - Drawer mobile
- ✅ Popover - Popover
- ✅ Tooltip - Tooltip
- ✅ Hover Card - Card em hover

### Visuais (4 componentes)
- ✅ Button - Botão com variantes
- ✅ Avatar - Avatar de usuário
- ✅ Carousel - Carrossel de imagens
- ✅ Chart - Gráficos

### Interativos (3 componentes)
- ✅ Toggle - Toggle button
- ✅ Toggle Group - Grupo de toggles
- ✅ Resizable - Painéis redimensionáveis

**Total: 43 componentes** ✅

---

## 💡 Exemplos de Uso

### Button

```django
{% include 'components/ui/button.html' with variant="default" size="lg" text="Clique Aqui" %}

{# Ou usando template tag #}
{% ui_button text="Salvar" variant="primary" size="default" %}
```

Variantes: `default`, `destructive`, `outline`, `secondary`, `ghost`, `link`, `premium`

Tamanhos: `sm`, `default`, `lg`, `xl`, `icon`

### Card

```django
{% include 'components/ui/card.html' with title="Título do Card" description="Descrição" %}
    <p>Conteúdo do card aqui</p>
    <div class="card-footer">
        {% ui_button text="Ação" %}
    </div>
{% endinclude %}
```

### Input

```django
{% include 'components/ui/input.html' with type="email" name="email" placeholder="seu@email.com" required=True %}
```

### Alert

```django
{% ui_alert title="Atenção!" description="Dados salvos com sucesso" variant="default" %}
```

Variantes: `default`, `destructive`

### Badge

```django
{% ui_badge text="Novo" variant="default" %}
{% ui_badge text="Erro" variant="destructive" %}
```

### Accordion

```django
{% with items=accordion_data %}
{% include 'components/ui/accordion.html' with items=items %}
{% endwith %}
```

```python
# Na view:
accordion_data = [
    {'title': 'Item 1', 'content': '<p>Conteúdo 1</p>'},
    {'title': 'Item 2', 'content': '<p>Conteúdo 2</p>'},
]
```

### Tabs

```django
{% with tabs=tab_data %}
{% include 'components/ui/tabs.html' with tabs=tabs default_tab="tab1" %}
{% endwith %}
```

```python
# Na view:
tab_data = [
    {'id': 'tab1', 'label': 'Tab 1', 'content': '<p>Content 1</p>'},
    {'id': 'tab2', 'label': 'Tab 2', 'content': '<p>Content 2</p>'},
]
```

### Table

```django
{% with headers=headers rows=rows %}
{% include 'components/ui/table.html' with headers=headers rows=rows caption="Lista de Usuários" %}
{% endwith %}
```

```python
# Na view:
headers = ['Nome', 'Email', 'Ações']
rows = [
    [
        {'value': 'João Silva'},
        {'value': 'joao@email.com'},
        {'value': '<button class="btn btn-sm">Editar</button>'}
    ],
]
```

### Dialog/Modal

```django
{# Definir modal #}
{% include 'components/ui/dialog.html' with id="confirmDialog" title="Confirmar Ação" description="Tem certeza?" %}
    <p>Conteúdo do modal</p>
    <div class="dialog-footer">
        <button class="btn btn-outline" onclick="UI.overlay.close(document.getElementById('confirmDialog'))">Cancelar</button>
        <button class="btn btn-default">Confirmar</button>
    </div>
{% endinclude %}

{# Abrir modal #}
<button class="btn btn-default" onclick="UI.overlay.open(document.getElementById('confirmDialog'))">
    Abrir Modal
</button>
```

### Toast (via JavaScript)

```javascript
// Success
UI.toast.success('Sucesso!', 'Dados salvos com sucesso');

// Error
UI.toast.error('Erro!', 'Não foi possível salvar');

// Info
UI.toast.info('Informação', 'Dados atualizados');

// Custom
UI.toast.show({
    title: 'Título',
    description: 'Descrição',
    variant: 'default',
    duration: 5000
});
```

### Progress

```django
{% ui_progress value=75 max=100 %}
```

### Skeleton Loading

```django
{% ui_skeleton width="200px" height="20px" %}
{% ui_skeleton width="100%" height="40px" rounded="lg" %}
```

### Avatar

```django
{% ui_avatar src="/static/img/user.jpg" name="João Silva" %}
{% ui_avatar name="Maria Santos" fallback="MS" %}
```

### Pagination

```django
{% include 'components/ui/pagination.html' with page_obj=page_obj url_pattern="?page=" %}
```

### Breadcrumb

```django
{% with items=breadcrumb_items %}
{% include 'components/ui/breadcrumb.html' with items=items %}
{% endwith %}
```

```python
# Na view:
breadcrumb_items = [
    {'url': '/', 'label': 'Home'},
    {'url': '/produtos/', 'label': 'Produtos'},
    {'label': 'Detalhes'}  # último sem URL
]
```

---

## 🏷️ Template Tags

### ui_button

```django
{% ui_button text="Salvar" variant="primary" size="lg" %}
```

### ui_badge

```django
{% ui_badge text="Novo" variant="default" %}
```

### ui_alert

```django
{% ui_alert title="Atenção" description="Mensagem importante" variant="destructive" %}
```

### ui_progress

```django
{% ui_progress value=50 max=100 %}
```

### ui_skeleton

```django
{% ui_skeleton width="100%" height="20px" %}
```

### ui_separator

```django
{% ui_separator orientation="horizontal" %}
```

### ui_avatar

```django
{% ui_avatar src="/img/avatar.jpg" name="João" %}
```

### ui_icon

```django
{% ui_icon "check" size="5" %}
{% ui_icon "x" size="4" %}
{% ui_icon "chevron-down" %}
```

---

## ⚡ JavaScript API

### UI.toast

```javascript
UI.toast.success('Título', 'Descrição');
UI.toast.error('Título', 'Descrição');
UI.toast.info('Título', 'Descrição');
```

### UI.overlay

```javascript
// Abrir overlay
UI.overlay.open(document.getElementById('myDialog'));

// Fechar overlay
UI.overlay.close(document.getElementById('myDialog'));

// Fechar último
UI.overlay.closeLast();
```

### UI.animate

```javascript
// Fade in
await UI.animate.fadeIn(element, 300);

// Fade out
await UI.animate.fadeOut(element, 300);

// Slide down
await UI.animate.slideDown(element, 300);

// Slide up
await UI.animate.slideUp(element, 300);
```

### UI.api

```javascript
// GET
const data = await UI.api.get('/api/endpoint/');

// POST
const result = await UI.api.post('/api/endpoint/', {key: 'value'});

// PUT
await UI.api.put('/api/endpoint/1/', {key: 'new value'});

// DELETE
await UI.api.delete('/api/endpoint/1/');
```

### UI.utils

```javascript
// Debounce
const debouncedFn = UI.utils.debounce(() => {
    console.log('Executado após delay');
}, 300);

// CSRF Token
const token = UI.utils.getCsrfToken();

// Gerar ID único
const id = UI.utils.generateId('my-component');

// Sanitizar HTML
const safe = UI.utils.escapeHtml('<script>alert("xss")</script>');
```

### UI.events

```javascript
// Escutar evento
UI.events.on('custom:event', (data) => {
    console.log('Evento disparado:', data);
});

// Emitir evento
UI.events.emit('custom:event', {key: 'value'});

// Remover listener
UI.events.off('custom:event');
```

### UI.theme

```javascript
// Obter tema atual
const theme = UI.theme.get(); // 'light' ou 'dark'

// Definir tema
UI.theme.set('dark');

// Toggle tema
UI.theme.toggle();
```

---

## 🎯 Variantes de Cores

### Button/Badge/Alert
- `default` - Cor primária
- `destructive` - Vermelho (ações destrutivas)
- `outline` - Apenas borda
- `secondary` - Cor secundária
- `ghost` - Transparente
- `link` - Estilo de link
- `premium` - Gradiente dourado

### Tamanhos
- `sm` - Pequeno
- `default` - Padrão
- `lg` - Grande
- `xl` - Extra grande
- `icon` - Tamanho de ícone

---

## 🎨 Customização

### Sobrescrever Estilos

```css
/* Customizar cores primárias */
:root {
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
}

/* Customizar raio de borda */
:root {
    --radius: 0.75rem;
}
```

### Adicionar Classes Personalizadas

```django
{% include 'components/ui/button.html' with class="my-custom-class" %}
```

---

## 🚀 Boas Práticas

### 1. Sempre Usar Componentes

```django
{# ❌ Evite HTML direto #}
<button class="bg-blue-500 text-white px-4 py-2 rounded">Botão</button>

{# ✅ Use componentes #}
{% include 'components/ui/button.html' with text="Botão" variant="default" %}
```

### 2. Aproveitar Template Tags

```django
{# ✅ Mais limpo #}
{% ui_button text="Salvar" variant="primary" %}

{# ❌ Mais verboso #}
{% include 'components/ui/button.html' with text="Salvar" variant="primary" %}
```

### 3. Validação de Formulários

```javascript
const validation = UI.form.validate(input, {
    required: true,
    minLength: 3,
    maxLength: 100,
    email: true
});

if (!validation.valid) {
    UI.form.showErrors(input, validation.errors);
}
```

### 4. Gerenciar Estado

```javascript
// Salvar estado
UI.state.set('user', {name: 'João', email: 'joao@email.com'});

// Obter estado
const user = UI.state.get('user');

// Escutar mudanças
UI.state.subscribe('user', (newUser) => {
    console.log('Usuário atualizado:', newUser);
});
```

---

## 🎓 Exemplos Completos

### Formulário de Login

```django
{% load ui_components %}

<form method="post" class="space-y-4">
    {% csrf_token %}
    
    <div>
        {% include 'components/ui/label.html' with for="email" text="Email" required=True %}
        {% include 'components/ui/input.html' with type="email" name="email" placeholder="seu@email.com" required=True %}
    </div>
    
    <div>
        {% include 'components/ui/label.html' with for="password" text="Senha" required=True %}
        {% include 'components/ui/input.html' with type="password" name="password" required=True %}
    </div>
    
    {% include 'components/ui/button.html' with type="submit" text="Entrar" variant="default" class="w-full" %}
</form>
```

### Dashboard com Cards

```django
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    {% include 'components/ui/card.html' with title="Total de Usuários" %}
        <p class="text-3xl font-bold">{{ total_users }}</p>
    {% endinclude %}
    
    {% include 'components/ui/card.html' with title="Vendas Hoje" %}
        <p class="text-3xl font-bold">R$ {{ sales_today }}</p>
    {% endinclude %}
    
    {% include 'components/ui/card.html' with title="Pedidos" %}
        <p class="text-3xl font-bold">{{ total_orders }}</p>
    {% endinclude %}
</div>
```

### Lista com Tabela e Paginação

```django
{% include 'components/ui/table.html' with headers=headers rows=rows caption="Lista de Clientes" %}

<div class="mt-4">
    {% include 'components/ui/pagination.html' with page_obj=page_obj url_pattern="?page=" %}
</div>
```

### Modal de Confirmação

```django
{# Definir modal #}
{% include 'components/ui/alert_dialog.html' with id="deleteDialog" title="Confirmar Exclusão" description="Esta ação não pode ser desfeita" action_variant="destructive" action_text="Excluir" action_onclick="deleteItem()" %}

{# Botão para abrir #}
<button class="btn btn-destructive" onclick="UI.overlay.open(document.getElementById('deleteDialog'))">
    Excluir Item
</button>
```

---

## 📱 Responsividade

Todos os componentes são responsivos por padrão usando Tailwind CSS:

```django
{# Grid responsivo #}
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {% ui_card title="Card 1" %}
    {% ui_card title="Card 2" %}
    {% ui_card title="Card 3" %}
</div>
```

---

## 🔧 Troubleshooting

### Componentes não aparecem estilizados

**Problema**: Estilos não carregam

**Solução**:
1. Verificar se `components.css` está incluído
2. Executar `python manage.py collectstatic`
3. Verificar console do navegador

### JavaScript não funciona

**Problema**: Componentes interativos não respondem

**Solução**:
1. Verificar se `ui-core.js` está carregado primeiro
2. Carregar scripts com `defer`
3. Verificar console para erros

### Template tags não encontradas

**Problema**: `{% load ui_components %}` dá erro

**Solução**:
1. Verificar se `core/templatetags/__init__.py` existe
2. Reiniciar servidor Django
3. Verificar INSTALLED_APPS inclui 'core'

---

## 📞 Suporte

Para mais informações:
- Documentação completa em cada arquivo de componente
- Exemplos em `templates/components/showcase.html`
- JavaScript em `static/js/ui-core.js` e `static/js/components/`

---

**✨ Sistema completo de componentes UI pronto para uso!** 🚀

