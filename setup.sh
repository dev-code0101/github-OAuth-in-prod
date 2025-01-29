#!/bin/bash

set -e  # Exit immediately if any command fails

echo "🔧 Setting up FastAPI application..."

# Update and install required packages
sudo apt update && sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx

# Create application directory
APP_DIR="/home/$USER/fastapi-app"
mkdir -p $APP_DIR
cd $APP_DIR

# Clone repository
if [ ! -d "$APP_DIR/.git" ]; then
    git clone https://github.com/yourusername/yourrepo.git .
else
    echo "✅ Repository already cloned."
fi

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set up PostgreSQL database
sudo -u postgres psql <<EOF
CREATE DATABASE fastapi_db;
CREATE USER fastapi_user WITH PASSWORD 'securepassword';
ALTER ROLE fastapi_user SET client_encoding TO 'utf8';
ALTER ROLE fastapi_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE fastapi_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
EOF

# Run Alembic migrations
export DATABASE_URL="postgresql+asyncpg://fastapi_user:securepassword@localhost/fastapi_db"
alembic upgrade head

# Set up systemd service
echo "🚀 Setting up FastAPI service..."

sudo tee /etc/systemd/system/fastapi.service > /dev/null <<EOL
[Unit]
Description=FastAPI OAuth App
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable & start service
sudo systemctl daemon-reload
sudo systemctl enable fastapi.service
sudo systemctl start fastapi.service

# Configure Nginx
echo "🌍 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/fastapi > /dev/null <<EOL
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    error_log /var/log/nginx/fastapi_error.log;
    access_log /var/log/nginx/fastapi_access.log;
}
EOL

# Enable the Nginx site configuration and test the Nginx setup
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
sudo nginx -t

# Restart Nginx to apply changes
sudo systemctl restart nginx

# Open necessary firewall ports (if applicable)
echo "🔒 Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

# Final message
echo "✅ FastAPI application setup is complete!"
echo "🌐 You can now access your app at http://yourdomain.com"

       

alembic init alembic
alembic revision --autogenerate -m "Initial migration"