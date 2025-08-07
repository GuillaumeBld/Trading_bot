#!/bin/bash

# ChatGPT Micro-Cap Trading Bot - Hostinger Quick Deployment Script
# This script automates the deployment process on Hostinger VPS

set -e  # Exit on any error

echo "🚀 ChatGPT Micro-Cap Trading Bot - Hostinger Deployment"
echo "======================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Check for required commands
check_requirements() {
    print_status "Checking system requirements..."
    
    commands=("curl" "git" "docker" "docker-compose")
    missing_commands=()
    
    for cmd in "${commands[@]}"; do
        if ! command -v $cmd &> /dev/null; then
            missing_commands+=($cmd)
        fi
    done
    
    if [ ${#missing_commands[@]} -ne 0 ]; then
        print_error "Missing required commands: ${missing_commands[*]}"
        print_status "Installing missing dependencies..."
        install_dependencies
    else
        print_success "All requirements satisfied"
    fi
}

# Install system dependencies
install_dependencies() {
    print_status "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    
    # Install Docker if not present
    if ! command -v docker &> /dev/null; then
        print_status "Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
    fi
    
    # Install Docker Compose if not present
    if ! command -v docker-compose &> /dev/null; then
        print_status "Installing Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    # Install other dependencies
    sudo apt install -y git python3 python3-pip nginx certbot python3-certbot-nginx
    
    print_success "Dependencies installed successfully"
}

# Clone repository
clone_repository() {
    print_status "Setting up project directory..."
    
    PROJECT_DIR="/var/www/chatgpt-microcap-experiment"
    
    if [ -d "$PROJECT_DIR" ]; then
        print_warning "Project directory already exists. Updating..."
        cd $PROJECT_DIR
        git pull origin main
    else
        print_status "Cloning repository..."
        sudo mkdir -p /var/www
        cd /var/www
        
        # Replace with actual repository URL
        git clone https://github.com/your-username/chatgpt-microcap-experiment.git
        
        # Set proper ownership
        sudo chown -R $USER:$USER $PROJECT_DIR
    fi
    
    cd $PROJECT_DIR
    print_success "Repository setup complete"
}

# Configure environment
configure_environment() {
    print_status "Configuring environment variables..."
    
    cd n8n-integration
    
    if [ ! -f docker/.env ]; then
        cp docker/env.example docker/.env
        print_warning "Environment file created. Please edit docker/.env with your settings:"
        print_status "Required variables:"
        echo "  - OPENAI_API_KEY"
        echo "  - POSTGRES_PASSWORD"
        echo "  - N8N_BASIC_AUTH_PASSWORD"
        echo "  - JWT_SECRET_KEY"
        echo "  - WEBHOOK_SECRET"
        echo "  - API_KEY"
        
        # Generate secure passwords
        POSTGRES_PASSWORD=$(openssl rand -base64 16)
        N8N_PASSWORD=$(openssl rand -base64 12)
        JWT_SECRET=$(openssl rand -base64 32)
        WEBHOOK_SECRET=$(openssl rand -base64 16)
        API_KEY=$(openssl rand -base64 24)
        
        # Update .env file with generated values
        sed -i "s/your-secure-db-password-here/$POSTGRES_PASSWORD/g" docker/.env
        sed -i "s/your-secure-n8n-password-here/$N8N_PASSWORD/g" docker/.env
        sed -i "s/your-super-secret-jwt-key-for-api-auth/$JWT_SECRET/g" docker/.env
        sed -i "s/your-webhook-secret-for-signature-verification/$WEBHOOK_SECRET/g" docker/.env
        sed -i "s/your-api-key-for-external-services/$API_KEY/g" docker/.env
        
        print_success "Environment configured with generated passwords"
        print_warning "IMPORTANT: Please add your API keys to docker/.env:"
        echo "  - OPENAI_API_KEY=your-openai-key"
        echo "  - ANTHROPIC_API_KEY=your-anthropic-key (optional)"
        
        read -p "Press Enter after you've added your API keys to continue..."
    else
        print_success "Environment file already exists"
    fi
}

# Deploy services
deploy_services() {
    print_status "Deploying Docker services..."
    
    cd n8n-integration
    
    # Pull latest images
    docker-compose -f docker/docker-compose.yml pull
    
    # Start services
    docker-compose -f docker/docker-compose.yml up -d
    
    print_status "Waiting for services to start..."
    sleep 30
    
    # Check service status
    if docker-compose -f docker/docker-compose.yml ps | grep -q "Up"; then
        print_success "Services deployed successfully"
    else
        print_error "Some services failed to start"
        docker-compose -f docker/docker-compose.yml logs
        exit 1
    fi
}

# Configure Nginx
configure_nginx() {
    print_status "Configuring Nginx reverse proxy..."
    
    read -p "Enter your domain name (or press Enter to skip): " DOMAIN_NAME
    
    if [ -z "$DOMAIN_NAME" ]; then
        print_warning "Skipping Nginx configuration"
        return
    fi
    
    # Create Nginx configuration
    sudo tee /etc/nginx/sites-available/trading-bot > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;

    # Trading Dashboard
    location / {
        proxy_pass http://localhost:8502;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # n8n Workflows
    location /n8n/ {
        proxy_pass http://localhost:5678/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # API Endpoints
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    # Enable site
    sudo ln -sf /etc/nginx/sites-available/trading-bot /etc/nginx/sites-enabled/
    sudo nginx -t
    
    if [ $? -eq 0 ]; then
        sudo systemctl restart nginx
        print_success "Nginx configured successfully"
        
        # Setup SSL
        read -p "Setup SSL certificate? (y/n): " SETUP_SSL
        if [[ $SETUP_SSL =~ ^[Yy]$ ]]; then
            setup_ssl "$DOMAIN_NAME"
        fi
    else
        print_error "Nginx configuration failed"
    fi
}

# Setup SSL certificate
setup_ssl() {
    local domain=$1
    print_status "Setting up SSL certificate for $domain..."
    
    sudo certbot --nginx -d $domain -d www.$domain --non-interactive --agree-tos --email admin@$domain
    
    if [ $? -eq 0 ]; then
        print_success "SSL certificate installed successfully"
        
        # Setup auto-renewal
        (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
        print_success "SSL auto-renewal configured"
    else
        print_error "SSL certificate installation failed"
    fi
}

# Configure firewall
configure_firewall() {
    print_status "Configuring firewall..."
    
    sudo ufw --force enable
    sudo ufw allow ssh
    sudo ufw allow http
    sudo ufw allow https
    
    # Allow direct access to services if needed
    read -p "Allow direct access to trading dashboard (port 8502)? (y/n): " ALLOW_8502
    if [[ $ALLOW_8502 =~ ^[Yy]$ ]]; then
        sudo ufw allow 8502
    fi
    
    read -p "Allow direct access to n8n (port 5678)? (y/n): " ALLOW_5678
    if [[ $ALLOW_5678 =~ ^[Yy]$ ]]; then
        sudo ufw allow 5678
    fi
    
    print_success "Firewall configured"
}

# Test deployment
test_deployment() {
    print_status "Testing deployment..."
    
    # Test API health
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "API health check passed"
    else
        print_error "API health check failed"
    fi
    
    # Test dashboard
    if curl -s http://localhost:8502 > /dev/null; then
        print_success "Dashboard accessible"
    else
        print_error "Dashboard not accessible"
    fi
    
    # Test n8n
    if curl -s http://localhost:5678 > /dev/null; then
        print_success "n8n accessible"
    else
        print_error "n8n not accessible"
    fi
    
    # Show service status
    print_status "Service status:"
    docker-compose -f n8n-integration/docker/docker-compose.yml ps
}

# Setup monitoring
setup_monitoring() {
    print_status "Setting up monitoring..."
    
    # Create monitoring script
    cat > /home/$USER/monitor-trading-bot.sh << 'EOF'
#!/bin/bash
# Trading Bot Monitoring Script

LOG_FILE="/var/log/trading-bot-monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Check Docker containers
if ! docker-compose -f /var/www/chatgpt-microcap-experiment/n8n-integration/docker/docker-compose.yml ps | grep -q "Up"; then
    echo "$DATE - WARNING: Some containers are down" >> $LOG_FILE
    # Restart services
    cd /var/www/chatgpt-microcap-experiment/n8n-integration
    docker-compose -f docker/docker-compose.yml restart
fi

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$DATE - WARNING: Disk usage is ${DISK_USAGE}%" >> $LOG_FILE
fi

# Check memory usage
MEM_USAGE=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
if (( $(echo "$MEM_USAGE > 90" | bc -l) )); then
    echo "$DATE - WARNING: Memory usage is ${MEM_USAGE}%" >> $LOG_FILE
fi

echo "$DATE - Health check completed" >> $LOG_FILE
EOF

    chmod +x /home/$USER/monitor-trading-bot.sh
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "*/5 * * * * /home/$USER/monitor-trading-bot.sh") | crontab -
    
    print_success "Monitoring script installed"
}

# Create backup script
create_backup_script() {
    print_status "Creating backup script..."
    
    cat > /home/$USER/backup-trading-bot.sh << 'EOF'
#!/bin/bash
# Trading Bot Backup Script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/trading-bot"
PROJECT_DIR="/var/www/chatgpt-microcap-experiment"

# Create backup directory
sudo mkdir -p $BACKUP_DIR

# Backup database
cd $PROJECT_DIR/n8n-integration
docker-compose exec -T postgres pg_dump -U postgres trading_bot > $BACKUP_DIR/db_$DATE.sql

# Backup configuration
cp docker/.env $BACKUP_DIR/env_$DATE.backup

# Backup workflows
cp -r workflows/ $BACKUP_DIR/workflows_$DATE/

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.backup" -mtime +7 -delete
find $BACKUP_DIR -name "workflows_*" -mtime +7 -exec rm -rf {} +

echo "Backup completed: $DATE"
EOF

    chmod +x /home/$USER/backup-trading-bot.sh
    
    # Add to crontab for daily backups
    (crontab -l 2>/dev/null; echo "0 2 * * * /home/$USER/backup-trading-bot.sh") | crontab -
    
    print_success "Backup script installed"
}

# Main deployment function
main() {
    print_status "Starting Hostinger deployment..."
    
    # Check requirements
    check_requirements
    
    # Clone repository
    clone_repository
    
    # Configure environment
    configure_environment
    
    # Deploy services
    deploy_services
    
    # Configure Nginx
    configure_nginx
    
    # Configure firewall
    configure_firewall
    
    # Test deployment
    test_deployment
    
    # Setup monitoring
    setup_monitoring
    
    # Create backup script
    create_backup_script
    
    print_success "Deployment completed successfully!"
    echo ""
    print_status "Access your services:"
    echo "  - Trading Dashboard: http://$(curl -s ifconfig.me):8502"
    echo "  - n8n Workflows: http://$(curl -s ifconfig.me):5678"
    echo "  - API Documentation: http://$(curl -s ifconfig.me):8000/docs"
    echo ""
    print_status "Default credentials:"
    echo "  - n8n: admin / (check docker/.env for password)"
    echo "  - API: Bearer token (check docker/.env for API_KEY)"
    echo ""
    print_warning "Important next steps:"
    echo "  1. Change all default passwords"
    echo "  2. Configure your trading API keys"
    echo "  3. Set up your notification channels"
    echo "  4. Test all functionality before live trading"
    echo ""
    print_success "Happy trading! 🚀"
}

# Run main function
main "$@"