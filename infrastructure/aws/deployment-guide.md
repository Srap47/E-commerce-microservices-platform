# AWS Deployment Guide

## Prerequisites
- AWS Account
- AWS CLI configured with credentials
- Terraform installed
- Docker installed

## Deployment Steps

### 1. Set Up Infrastructure

```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the configuration
terraform apply
```

### 2. Build and Push Docker Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repositories
aws ecr create-repository --repository-name ecommerce-product-service
aws ecr create-repository --repository-name ecommerce-cart-service
aws ecr create-repository --repository-name ecommerce-auth-service
aws ecr create-repository --repository-name ecommerce-api-gateway
aws ecr create-repository --repository-name ecommerce-frontend

# Build and push images
docker build -t ecommerce-product-service services/product-service/
docker tag ecommerce-product-service:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ecommerce-product-service:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ecommerce-product-service:latest

# Repeat for other services...
```

### 3. Deploy to ECS

```bash
# Update ECS service with new task definition
aws ecs update-service --cluster ecommerce-cluster --service product-service --force-new-deployment
```

### 4. Monitor Deployment

```bash
# Check service status
aws ecs describe-services --cluster ecommerce-cluster --services product-service

# View logs
aws logs tail /ecs/ecommerce-product-service --follow
```

## Environment Variables

Create a `.env` file in the root directory:

```
PRODUCT_SERVICE_URL=http://product-service:8001
CART_SERVICE_URL=http://cart-service:8002
AUTH_SERVICE_URL=http://auth-service:8003
JWT_SECRET_KEY=your-secret-key
```

## Cleanup

```bash
# Destroy all infrastructure
terraform destroy
```

## Troubleshooting

- Check CloudWatch logs for service errors
- Verify security group ingress/egress rules
- Ensure IAM roles have necessary permissions
