# 🔧 Como Configurar Variáveis de Ambiente

## ❌ Problema Identificado

O diagnóstico mostrou que todas as variáveis estão faltando:
- ❌ SUPABASE_URL
- ❌ SUPABASE_ANON_KEY  
- ❌ DATABASE_URL

## ✅ Solução Rápida

### Opção 1: Usar Script Automático (Recomendado)

```bash
python configure_supabase.py
```

O script vai pedir a senha do banco e configurar tudo automaticamente.

### Opção 2: Criar .env Manualmente

Crie um arquivo `.env` na raiz do projeto com:

```env
# Django Settings
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app

# Supabase Database
DATABASE_URL=postgresql://postgres:[SUA_SENHA]@db.[SEU_PROJETO].supabase.co:5432/postgres

# Supabase API (opcional - para uso futuro)
SUPABASE_URL=https://[SEU_PROJETO].supabase.co
SUPABASE_ANON_KEY=sua-chave-anon-aqui
```

### Onde Obter as Credenciais:

1. **Acesse:** https://app.supabase.com
2. **Vá em:** Settings → Database
3. **Copie:** Connection string (URI)
4. **Ou vá em:** Settings → API
   - **URL:** Project URL
   - **Anon Key:** anon/public key

## 📝 Exemplo Completo

```env
SECRET_KEY=django-insecure-sua-chave-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Substitua pelos seus valores reais:
DATABASE_URL=postgresql://postgres:minhasenha123@db.abcdefghijklmnop.supabase.co:5432/postgres
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## ✅ Depois de Configurar

Execute novamente o diagnóstico:

```bash
python manage.py diagnostico_supabase
```

Todas as variáveis devem aparecer como ✅ configuradas!

