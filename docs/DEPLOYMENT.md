# Deployment Guide

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd ecommerce-microservices

# Run setup script
bash infrastructure/local-setup.sh

# Or manually start with Docker Compose
docker-compose up -d
```

### Access Services
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- Product Service: http://localhost:8001
- Cart Service: http://localhost:8002
- Auth Service: http://localhost:8003

## Docker Deployment

### Build Images
```bash
docker-compose build
```

### Run Containers
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f [service-name]
```

### Stop Services
```bash
docker-compose down
```

## AWS Deployment

See [AWS Deployment Guide](../infrastructure/aws/deployment-guide.md)

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (EKS, GKE, or local)
- kubectl configured
- Docker images pushed to registry

### Deploy

```bash
# Create namespace
kubectl create namespace ecommerce

# Apply configurations
kubectl apply -f k8s/ -n ecommerce

# Check deployment status
kubectl get pods -n ecommerce
```

## Environment Configuration

Create `.env` file:

```env
# Service Configuration
PRODUCT_SERVICE_URL=http://product-service:8001
CART_SERVICE_URL=http://cart-service:8002
AUTH_SERVICE_URL=http://auth-service:8003

# Security
JWT_SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@db:5432/ecommerce

# Environment
ENVIRONMENT=production
LOG_LEVEL=info
```

## Monitoring

### Logs
```bash
# Docker
docker-compose logs -f

# Kubernetes
kubectl logs -f deployment/api-gateway -n ecommerce
```

### Health Checks
```bash
curl http://localhost:8000/health
```

## Scaling

### Docker Compose
```bash
docker-compose up -d --scale product-service=3
```

### Kubernetes
```bash
kubectl scale deployment product-service --replicas=3 -n ecommerce
```

## Rollback

### Docker
```bash
docker-compose down
docker-compose up -d
```

### Kubernetes
```bash
kubectl rollout history deployment/api-gateway -n ecommerce
kubectl rollout undo deployment/api-gateway -n ecommerce
```
