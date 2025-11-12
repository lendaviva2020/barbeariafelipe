#!/bin/bash

# ========================================
# SCRIPT DE DEPLOY AUTOMATIZADO
# Barbearia Django - Sistema Completo
# ========================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Verificar se está no diretório correto
if [ ! -f "manage.py" ]; then
    print_error "Erro: manage.py não encontrado. Execute este script no diretório raiz do projeto."
    exit 1
fi

# Menu principal
print_header "🚀 DEPLOY AUTOMATIZADO - BARBEARIA DJANGO"

echo "Escolha o tipo de deploy:"
echo ""
echo "1) Deploy Local (Desenvolvimento)"
echo "2) Deploy com Docker"
echo "3) Deploy em VPS (Ubuntu)"
echo "4) Apenas verificações (check)"
echo "5) Sair"
echo ""
read -p "Opção: " deploy_option

case $deploy_option in
    1)
        print_header "📦 DEPLOY LOCAL"
        
        # Verificar Python
        print_info "Verificando Python..."
        if ! command -v python &> /dev/null; then
            print_error "Python não encontrado!"
            exit 1
        fi
        print_success "Python encontrado: $(python --version)"
        
        # Verificar ambiente virtual
        if [ ! -d "venv" ]; then
            print_warning "Ambiente virtual não encontrado. Criando..."
            python -m venv venv
            print_success "Ambiente virtual criado"
        fi
        
        # Ativar ambiente virtual
        print_info "Ativando ambiente virtual..."
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
        print_success "Ambiente virtual ativado"
        
        # Instalar dependências
        print_info "Instalando dependências..."
        pip install -r requirements.txt --quiet
        print_success "Dependências instaladas"
        
        # Executar migrations
        print_info "Executando migrations..."
        python manage.py migrate
        print_success "Migrations executadas"
        
        # Coletar static files
        print_info "Coletando arquivos estáticos..."
        python manage.py collectstatic --noinput
        print_success "Arquivos estáticos coletados"
        
        # Verificar sistema
        print_info "Verificando sistema..."
        python manage.py check
        print_success "Sistema verificado"
        
        # Perguntar se quer criar superusuário
        read -p "Criar superusuário? (s/n): " create_super
        if [ "$create_super" = "s" ]; then
            python manage.py createsuperuser
        fi
        
        # Iniciar servidor
        print_success "Deploy local concluído!"
        print_info "Iniciando servidor de desenvolvimento..."
        echo ""
        print_warning "ATENÇÃO: Este servidor NÃO deve ser usado em produção!"
        echo ""
        print_info "Acesse: http://localhost:8000"
        print_info "Admin: http://localhost:8000/admin/"
        print_info "Health: http://localhost:8000/health/"
        echo ""
        python manage.py runserver 0.0.0.0:8000
        ;;
        
    2)
        print_header "🐳 DEPLOY COM DOCKER"
        
        # Verificar Docker
        print_info "Verificando Docker..."
        if ! command -v docker &> /dev/null; then
            print_error "Docker não encontrado! Instale: https://www.docker.com/get-started"
            exit 1
        fi
        print_success "Docker encontrado: $(docker --version)"
        
        # Verificar Docker Compose
        print_info "Verificando Docker Compose..."
        if ! command -v docker-compose &> /dev/null; then
            print_error "Docker Compose não encontrado!"
            exit 1
        fi
        print_success "Docker Compose encontrado: $(docker-compose --version)"
        
        # Verificar se .env existe
        if [ ! -f ".env" ]; then
            print_warning "Arquivo .env não encontrado!"
            print_info "Copiando .env.example para .env..."
            cp .env.example .env
            print_warning "Configure o arquivo .env antes de continuar!"
            exit 1
        fi
        
        # Build da imagem
        print_info "Building Docker image..."
        docker build -t barbearia-django .
        print_success "Imagem Docker criada"
        
        # Parar containers antigos
        print_info "Parando containers antigos..."
        docker-compose -f docker-compose.prod.yml down
        
        # Iniciar containers
        print_info "Iniciando containers..."
        docker-compose -f docker-compose.prod.yml up -d
        print_success "Containers iniciados"
        
        # Aguardar banco de dados
        print_info "Aguardando banco de dados..."
        sleep 10
        
        # Executar migrations
        print_info "Executando migrations..."
        docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate
        print_success "Migrations executadas"
        
        # Coletar static files
        print_info "Coletando arquivos estáticos..."
        docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
        print_success "Arquivos estáticos coletados"
        
        # Verificar sistema
        print_info "Verificando sistema..."
        docker-compose -f docker-compose.prod.yml exec -T web python manage.py check
        print_success "Sistema verificado"
        
        # Perguntar se quer criar superusuário
        read -p "Criar superusuário? (s/n): " create_super
        if [ "$create_super" = "s" ]; then
            docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
        fi
        
        # Mostrar status
        print_success "Deploy Docker concluído!"
        echo ""
        print_info "Containers em execução:"
        docker-compose -f docker-compose.prod.yml ps
        echo ""
        print_info "Acesse: http://localhost:8000"
        print_info "Admin: http://localhost:8000/admin/"
        print_info "Health: http://localhost:8000/health/"
        echo ""
        print_info "Ver logs: docker-compose -f docker-compose.prod.yml logs -f"
        print_info "Parar: docker-compose -f docker-compose.prod.yml down"
        ;;
        
    3)
        print_header "🖥️  DEPLOY EM VPS"
        
        print_warning "Este script irá configurar o servidor VPS."
        print_warning "Certifique-se de:"
        echo "  - Ter acesso SSH ao servidor"
        echo "  - O servidor estar rodando Ubuntu 20.04+"
        echo "  - Ter permissões sudo"
        echo ""
        read -p "Continuar? (s/n): " continue_vps
        
        if [ "$continue_vps" != "s" ]; then
            print_info "Deploy cancelado."
            exit 0
        fi
        
        # Solicitar informações do servidor
        read -p "IP ou domínio do servidor: " server_host
        read -p "Usuário SSH: " server_user
        read -p "Domínio do site (ex: meusite.com): " domain_name
        
        print_info "Conectando ao servidor..."
        
        # Criar script de setup remoto
        cat > /tmp/remote_setup.sh << 'EOFREMOTE'
#!/bin/bash
set -e

# Atualizar sistema
echo "Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências
echo "Instalando dependências..."
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git

# Configurar PostgreSQL
echo "Configurando PostgreSQL..."
sudo -u postgres psql << EOF
CREATE DATABASE barbearia;
CREATE USER barbearia_user WITH PASSWORD 'senha_segura_123';
ALTER ROLE barbearia_user SET client_encoding TO 'utf8';
ALTER ROLE barbearia_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE barbearia_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE barbearia TO barbearia_user;
EOF

echo "Setup inicial concluído!"
EOFREMOTE
        
        # Copiar e executar script no servidor
        scp /tmp/remote_setup.sh $server_user@$server_host:/tmp/
        ssh $server_user@$server_host 'bash /tmp/remote_setup.sh'
        
        # Copiar projeto para servidor
        print_info "Copiando projeto para servidor..."
        rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' --exclude '.git' \
            ./ $server_user@$server_host:~/barbearia-django/
        
        # Configurar projeto no servidor
        ssh $server_user@$server_host << 'EOFSSH'
cd ~/barbearia-django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configurar .env
cat > .env << EOF
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=False
ALLOWED_HOSTS=$domain_name,www.$domain_name
DATABASE_URL=postgresql://barbearia_user:senha_segura_123@localhost/barbearia
REDIS_URL=redis://localhost:6379/0
EOF

# Executar migrations
python manage.py migrate
python manage.py collectstatic --noinput

# Configurar Gunicorn
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << EOFSERVICE
[Unit]
Description=Gunicorn daemon for Barbearia Django
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/home/$USER/barbearia-django
Environment="PATH=/home/$USER/barbearia-django/venv/bin"
EnvironmentFile=/home/$USER/barbearia-django/.env
ExecStart=/home/$USER/barbearia-django/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          barbearia.wsgi:application

[Install]
WantedBy=multi-user.target
EOFSERVICE

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Configurar Nginx
sudo tee /etc/nginx/sites-available/barbearia > /dev/null << EOFNGINX
server {
    listen 80;
    server_name $domain_name www.$domain_name;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/$USER/barbearia-django/staticfiles/;
    }

    location /media/ {
        alias /home/$USER/barbearia-django/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOFNGINX

sudo ln -sf /etc/nginx/sites-available/barbearia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'

echo "Deploy VPS concluído!"
EOFSSH
        
        print_success "Deploy VPS concluído!"
        echo ""
        print_info "Próximos passos:"
        echo "  1. Configure DNS para apontar para $server_host"
        echo "  2. Instale SSL: sudo certbot --nginx -d $domain_name"
        echo "  3. Acesse: http://$domain_name"
        echo "  4. Crie superusuário: ssh $server_user@$server_host 'cd ~/barbearia-django && source venv/bin/activate && python manage.py createsuperuser'"
        ;;
        
    4)
        print_header "🔍 VERIFICAÇÕES DO SISTEMA"
        
        print_info "Executando verificações..."
        echo ""
        
        # Check básico
        python manage.py check
        echo ""
        
        # Check de deploy
        print_info "Verificações para produção:"
        python manage.py check --deploy
        echo ""
        
        # Verificar migrations
        print_info "Verificando migrations pendentes:"
        python manage.py showmigrations | grep "\[ \]" && print_warning "Migrations pendentes encontradas!" || print_success "Todas migrations aplicadas"
        echo ""
        
        # Testar collectstatic
        print_info "Testando collectstatic (dry-run):"
        python manage.py collectstatic --noinput --dry-run
        echo ""
        
        print_success "Verificações concluídas!"
        ;;
        
    5)
        print_info "Saindo..."
        exit 0
        ;;
        
    *)
        print_error "Opção inválida!"
        exit 1
        ;;
esac

print_header "✅ CONCLUÍDO"
print_success "Deploy finalizado com sucesso!"
echo ""
print_info "Documentação completa: GUIA_DEPLOY_COMPLETO.md"
print_info "Suporte: TROUBLESHOOTING.md"
echo ""

