# 📸 ADICIONAR SUAS IMAGENS REAIS - GUIA RÁPIDO

## ✅ STATUS ATUAL

**POR ENQUANTO:** O sistema está usando **placeholders do Unsplash** (imagens temporárias de alta qualidade)

**AS IMAGENS APARECEM EM:**
- ✅ Página de agendamento
- ✅ Catálogo de serviços
- ✅ Home page
- ✅ Cards de serviços

**TUDO JÁ ESTÁ FUNCIONANDO!** Você pode testar o sistema agora mesmo.

---

## 🎯 PARA USAR SUAS PRÓPRIAS FOTOS:

### PASSO 1: Salvar as Imagens

1. **Abra a pasta:**
   ```
   C:\Users\98911\OneDrive\Desktop\barbearia-django\static\images\services\
   ```

2. **Salve as 5 fotos do chat com estes nomes EXATOS:**

   | Foto do Chat | Nome do Arquivo | Serviço |
   |--------------|----------------|---------|
   | Foto 1 (bigode) | `bigode-professional.jpg` | Bigode Profissional |
   | Foto 2 (perfil corte) | `corte-classico.jpg` | Corte Clássico |
   | Foto 3 (barba/orelha) | `barba-completa.jpg` | Barba Completa |
   | Foto 4 (barbeiro+cliente) | `corte-barba-combo.jpg` | Corte + Barba |
   | Foto 5 (perfil corte) | `corte-premium.jpg` | Corte Premium |

---

### PASSO 2: Executar Script

**No terminal/PowerShell:**
```bash
cd C:\Users\98911\OneDrive\Desktop\barbearia-django
python update_services_images.py
```

**O script vai:**
- ✅ Verificar se as 5 imagens estão salvas
- ✅ Atualizar todos os 10 serviços
- ✅ Confirmar sucesso

---

### PASSO 3: Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

---

### PASSO 4: Recarregar Página

No navegador: **Ctrl+Shift+R**

---

## 🎨 ONDE AS IMAGENS APARECEM:

### 1. Página de Agendamento (`/agendar/`)
```
┌─────────────────────┐
│  [IMAGEM]          │
│                     │
│  Corte Clássico    │
│  R$ 50,00          │
│  45 minutos        │
└─────────────────────┘
```

### 2. Catálogo de Serviços (`/servicos/`)
Grid com todas as imagens em cards elegantes

### 3. Home Page (`/`)
Serviços em destaque com imagens

### 4. Galeria (`/galeria/`)
Portfólio de trabalhos realizados

---

## 📋 CHECKLIST

- [ ] Salvei as 5 fotos em `static/images/services/`
- [ ] Renomeei com os nomes corretos (.jpg)
- [ ] Executei `python update_services_images.py`
- [ ] Executei `python manage.py collectstatic --noinput`
- [ ] Recarreguei a página (Ctrl+Shift+R)
- [ ] As imagens aparecem corretamente!

---

## ⚡ ATALHO RÁPIDO

Se preferir, copie e cole este comando (executa tudo de uma vez):

```bash
cd C:\Users\98911\OneDrive\Desktop\barbearia-django
python update_services_images.py
python manage.py collectstatic --noinput
echo.
echo PRONTO! Recarregue a pagina agora (Ctrl+Shift+R)
```

---

## 🆘 PROBLEMAS?

### "Imagens não aparecem"
- Certifique-se que os nomes estão EXATAMENTE iguais
- Execute collectstatic novamente
- Limpe o cache do navegador (Ctrl+Shift+R)

### "Erro ao executar script"
- Verifique se salvou as imagens na pasta correta
- Os nomes devem ter .jpg no final
- Sem espaços ou caracteres especiais

---

## 💡 DICA

**Por enquanto, use o sistema com as imagens placeholder do Unsplash.**  
Elas são profissionais e ficam ótimas! 

Quando tiver tempo, substitua pelas suas próprias fotos seguindo este guia.

---

## ✅ RESUMO

1. **Agora:** Sistema funcionando com placeholders Unsplash
2. **Depois:** Salve suas 5 fotos
3. **Execute:** `python update_services_images.py`
4. **Colete:** `python manage.py collectstatic --noinput`
5. **Recarregue:** Ctrl+Shift+R

**SIMPLES ASSIM!** 🚀

---

**Dúvidas?** Leia `GUIA_IMAGENS.md` ou `COMO_ADICIONAR_IMAGENS.txt`

