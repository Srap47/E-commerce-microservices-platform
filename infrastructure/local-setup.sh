#!/bin/bash

# Local Development Setup Script

set -e

echo "🚀 Setting up E-Commerce Microservices Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Service URLs
PRODUCT_SERVICE_URL=http://product-service:8001
CART_SERVICE_URL=http://cart-service:8002
AUTH_SERVICE_URL=http://auth-service:8003
API_GATEWAY_URL=http://localhost:8000

# Auth
JWT_SECRET_KEY=your-secret-key-change-this

# Database
POSTGRES_USER=ecommerce
POSTGRES_PASSWORD=ecommerce_password
POSTGRES_DB=ecommerce_db

# Environment
ENVIRONMENT=development
EOF
fi

# Build and start containers
echo "🐳 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

echo "✅ Setup complete!"
echo ""
echo "Services are running at:"
echo "  - API Gateway: http://localhost:8000"
echo "  - Product Service: http://localhost:8001"
echo "  - Cart Service: http://localhost:8002"
echo "  - Auth Service: http://localhost:8003"
echo "  - Frontend: http://localhost:3000"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"
