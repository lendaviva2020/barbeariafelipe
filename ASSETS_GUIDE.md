# GUIA DE ASSETS - React para Django

## 📁 ESTRUTURA DE PASTAS

```
static/
├── images/
│   ├── corte-classico.jpg
│   ├── corte-barba.jpg
│   ├── barba-completa.jpg
│   ├── bigode.jpg
│   ├── hero-background.jpg
│   ├── favicon.svg
│   └── logo.png
├── css/
│   ├── design-system.css  ✅ COMPLETO
│   ├── styles.css          ✅ COMPLETO
│   ├── booking.css         ✅ COMPLETO
│   └── admin.css           ✅ COMPLETO
└── js/
    ├── app.js              ✅ COMPLETO
    ├── auth.js             ✅ COMPLETO
    ├── booking.js          ✅ COMPLETO
    └── admin.js            ✅ COMPLETO
```

## 🖼️ IMAGENS NECESSÁRIAS

### 1. Serviços (4 imagens):
- `corte-classico.jpg` - Corte clássico masculino
- `corte-barba.jpg` - Corte + barba
- `barba-completa.jpg` - Barba completa
- `bigode.jpg` - Bigode estilizado

**Tamanho recomendado:** 400x400px ou 800x800px
**Formato:** JPG ou WebP
**Qualidade:** 85%

### 2. Hero/Background:
- `hero-background.jpg` - Imagem de fundo da seção hero
**Tamanho:** 1920x1080px
**Formato:** JPG
**Qualidade:** 80%

### 3. Logo/Branding:
- `logo.png` - Logo da barbearia (transparente)
**Tamanho:** 512x512px
**Formato:** PNG com transparência

- `favicon.svg` - Ícone do site
**Tamanho:** 32x32px ou SVG
**Formato:** SVG ou ICO

## 🎨 PLACEHOLDERS ATUAIS

Todas as imagens estão usando placeholders `via.placeholder.com`:
```html
<!-- Exemplo atual -->
<img src="https://via.placeholder.com/400x400/2C1810/C9A961?text=Corte+Classico">
```

## 🔄 COMO SUBSTITUIR

### Opção 1: Usar imagens do React original
```bash
# Copiar imagens do projeto React para Django
cp francisco-barber-suite/src/assets/*.jpg static/images/
cp francisco-barber-suite/src/assets/*.png static/images/
```

### Opção 2: Baixar imagens profissionais
Fontes recomendadas:
- [Unsplash](https://unsplash.com) - gratuitas, alta qualidade
- [Pexels](https://pexels.com) - gratuitas
- [Freepik](https://freepik.com) - gratuitas e premium

Buscar por:
- "barber shop"
- "men haircut"
- "beard grooming"
- "barbershop interior"

### Opção 3: Criar placeholders melhorados
Usar ferramentas online:
- [Placeholder.com](https://placeholder.com)
- [Lorem Picsum](https://picsum.photos)
- [DummyImage](https://dummyimage.com)

## 🖌️ ÍCONES

Usando **Lucide Icons** via CDN (já implementado):
```html
<script src="https://unpkg.com/lucide@latest"></script>
```

Sem necessidade de copiar assets de ícones!

## 📋 CHECKLIST DE ASSETS

### Críticos (necessários para funcionamento):
- [ ] favicon.svg ou favicon.ico
- [ ] logo.png (para header)

### Importantes (melhoram a experiência):
- [ ] corte-classico.jpg
- [ ] corte-barba.jpg
- [ ] barba-completa.jpg
- [ ] bigode.jpg

### Opcionais (podem usar placeholders):
- [ ] hero-background.jpg
- [ ] team photos (fotos dos barbeiros)
- [ ] gallery images (galeria)

## 🚀 PRIORIDADE DE IMPLEMENTAÇÃO

1. **Favicon** - Para branding básico
2. **Logo** - Para header/footer
3. **Imagens de serviços** - Para home e página de serviços
4. **Hero background** - Para impacto visual
5. **Gallery** - Para completude

## 💡 DICA

O projeto **JÁ FUNCIONA** com placeholders!
Você pode:
1. Testar tudo primeiro
2. Adicionar imagens reais depois
3. Ou usar os placeholders permanentemente para demo

## 📝 NOTA

Todos os templates já estão configurados com:
- `onerror` fallback para placeholders
- `loading="lazy"` para performance
- Alt texts descritivos para SEO
- Responsive images

**Status:** 🟡 Opcional - projeto funcional sem assets

