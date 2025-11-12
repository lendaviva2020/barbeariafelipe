#!/bin/bash

# Script de deploy para produção
# Uso: ./deploy.sh

set -e

echo "🚀 Iniciando deploy..."

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Pull do código
echo -e "${YELLOW}📥 Atualizando código...${NC}"
git pull origin master

# 2. Ativar ambiente virtual
echo -e "${YELLOW}🐍 Ativando ambiente virtual...${NC}"
source venv/bin/activate

# 3. Instalar/atualizar dependências
echo -e "${YELLOW}📦 Instalando dependências...${NC}"
pip install -r requirements.txt --upgrade --quiet

# 4. Aplicar migrações
echo -e "${YELLOW}🗄️  Aplicando migrações...${NC}"
python manage.py migrate --noinput

# 5. Coletar arquivos estáticos
echo -e "${YELLOW}📁 Coletando arquivos estáticos...${NC}"
python manage.py collectstatic --noinput --clear

# 6. Compilar mensagens (i18n)
if [ -d "locale" ]; then
    echo -e "${YELLOW}🌐 Compilando traduções...${NC}"
    python manage.py compilemessages
fi

# 7. Verificar deployment
echo -e "${YELLOW}✅ Verificando configuração...${NC}"
python manage.py check --deploy

# 8. Reiniciar serviços
echo -e "${YELLOW}🔄 Reiniciando serviços...${NC}"

if command -v supervisorctl &> /dev/null; then
    sudo supervisorctl restart barbearia
    sudo supervisorctl restart barbearia-celery
    sudo supervisorctl restart barbearia-celery-beat
    echo -e "${GREEN}✅ Supervisor reiniciado${NC}"
fi

if command -v systemctl &> /dev/null; then
    sudo systemctl restart nginx
    echo -e "${GREEN}✅ Nginx reiniciado${NC}"
fi

# 9. Limpar cache
echo -e "${YELLOW}🧹 Limpando cache...${NC}"
python manage.py clearsessions

# 10. Verificar status
echo -e "${YELLOW}📊 Verificando status...${NC}"
if command -v supervisorctl &> /dev/null; then
    sudo supervisorctl status
fi

echo -e "${GREEN}🎉 Deploy concluído com sucesso!${NC}"
echo -e "${GREEN}🌐 Acesse: https://seu-dominio.com${NC}"

