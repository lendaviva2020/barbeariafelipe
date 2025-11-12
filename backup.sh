#!/bin/bash

# Script de backup automático
# Uso: ./backup.sh
# Cron: 0 3 * * * /home/barbearia/app/backup.sh

set -e

# Configurações
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/barbearia/backups"
DB_NAME="barbearia_prod"
DB_USER="barbearia_user"
RETENTION_DAYS=30

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🔄 Iniciando backup...${NC}"

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# 1. Backup do banco de dados
echo -e "${YELLOW}📊 Backup do banco de dados...${NC}"
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Banco de dados: OK${NC}"
else
    echo -e "${RED}❌ Erro no backup do banco${NC}"
    exit 1
fi

# 2. Backup dos arquivos de media
echo -e "${YELLOW}📁 Backup de arquivos...${NC}"
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/barbearia/app/media

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Arquivos: OK${NC}"
else
    echo -e "${RED}❌ Erro no backup de arquivos${NC}"
fi

# 3. Backup das configurações
echo -e "${YELLOW}⚙️  Backup de configurações...${NC}"
cp /home/barbearia/app/.env $BACKUP_DIR/env_$DATE.bak

# 4. Remover backups antigos
echo -e "${YELLOW}🧹 Limpando backups antigos (>${RETENTION_DAYS} dias)...${NC}"
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete

# 5. Listar backups
echo -e "${YELLOW}📋 Backups disponíveis:${NC}"
ls -lh $BACKUP_DIR | tail -10

# 6. Tamanho total
TOTAL_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
echo -e "${GREEN}✅ Backup concluído!${NC}"
echo -e "${GREEN}💾 Tamanho total: $TOTAL_SIZE${NC}"

# 7. Enviar notificação (opcional)
# curl -X POST https://api.telegram.org/botTOKEN/sendMessage \
#     -d chat_id=YOUR_CHAT_ID \
#     -d text="✅ Backup barbearia concluído: $DATE"

