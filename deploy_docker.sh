#!/bin/bash

set -e  # Exit immediately if any command fails

echo "🚀 Deploying FastAPI with Docker..."

APP_DIR="/home/$USER/fastapi-app"

cd $APP_DIR

# Pull the latest code
git pull origin main

# Build and restart the containers
docker compose down
docker compose build
docker compose up -d

echo "✅ Deployment complete!"
