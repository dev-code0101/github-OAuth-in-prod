#!/bin/bash

set -e  # Exit immediately if any command fails

APP_DIR="/home/$USER/fastapi-app"

echo "🚀 Deploying FastAPI application..."

cd $APP_DIR

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run database migrations
export DATABASE_URL="postgresql+asyncpg://fastapi_user:securepassword@localhost/fastapi_db"
alembic upgrade head

# Restart the FastAPI service
sudo systemctl restart fastapi.service

echo "✅ Deployment complete!"

