# 📸 GUIA DE IMAGENS - BARBEARIA DJANGO

## 📁 Estrutura de Diretórios

As imagens devem ser salvas em:

```
static/images/
├── services/
│   ├── bigode-professional.jpg          (Foto 1 - Bigode)
│   ├── corte-classico.jpg               (Foto 2 - Corte Clássico)
│   ├── barba-completa.jpg               (Foto 3 - Barba Completa)
│   ├── corte-barba-combo.jpg            (Foto 4 - Combo)
│   └── corte-premium.jpg                (Foto 5 - Corte Clássico/Premium)
├── gallery/
│   ├── work-1.jpg                       (Foto 2 - Galeria)
│   ├── work-2.jpg                       (Foto 3 - Galeria)
│   ├── work-3.jpg                       (Foto 4 - Galeria)
│   └── work-4.jpg                       (Foto 5 - Galeria)
├── team/
│   └── barber-action.jpg                (Foto 4 - Barbeiro trabalhando)
└── hero/
    ├── hero-main.jpg                    (Foto 4 - Hero section)
    └── hero-secondary.jpg               (Foto 2 - Secondary hero)
```

---

## 📋 PASSO A PASSO

### 1. Salvar as Imagens

**Manualmente:**
1. Baixe/salve as 5 imagens que você enviou
2. Renomeie conforme a estrutura acima
3. Copie para `static/images/services/`
4. Copie para `static/images/gallery/`

**Estrutura:**
- Foto 1 (bigode) → `bigode-professional.jpg`
- Foto 2 (corte lado) → `corte-classico.jpg`
- Foto 3 (barba/orelha) → `barba-completa.jpg`
- Foto 4 (barbeiro+cliente) → `corte-barba-combo.jpg`
- Foto 5 (perfil corte) → `corte-premium.jpg`

---

## 🔧 DEPOIS DE SALVAR AS IMAGENS, EXECUTE:

```bash
python update_services_images.py
python manage.py collectstatic --noinput
```

---

## 📍 Locais Onde as Imagens Serão Usadas:

### 1. Página de Serviços
- Card de cada serviço mostra sua imagem
- Hover effect com zoom

### 2. Página de Agendamento
- Seleção de serviço mostra imagem
- Preview visual do serviço

### 3. Galeria
- Grid de trabalhos realizados
- Lightbox ao clicar

### 4. Home Page
- Hero section com imagem principal
- Seção de serviços em destaque
- Seção da equipe

### 5. Admin Panel
- Preview ao cadastrar/editar serviços
- Galeria de trabalhos

---

## 📝 Observações:

- Imagens otimizadas automaticamente (max 1920px)
- Formato aceito: JPG, PNG, WebP
- Tamanho recomendado: 1920x1080px
- Peso máximo: 2MB por imagem

---

Salve as imagens na estrutura acima e execute o script de atualização!

