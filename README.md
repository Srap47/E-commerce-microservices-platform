# E-Commerce Microservices Platform 🛍️

A full-stack e-commerce application demonstrating **microservices architecture**, **API Gateway pattern**, **JWT authentication**, and **intelligent product ranking**. Built with **Python FastAPI** backend and **React** frontend.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Authentication Flow](#authentication-flow)
- [Product Ranking Algorithm](#product-ranking-algorithm)
- [Cloud Deployment](#cloud-deployment)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Design Decisions](#design-decisions)

---

## 🎯 Overview

This project implements a simplified e-commerce platform following **microservices architecture** principles:

- **3 Independent Microservices**: Product Ranking, Cart Management, Authentication
- **API Gateway**: Single entry point with request routing and JWT validation
- **JWT Authentication**: Secure, stateless authentication for protected endpoints
- **Intelligent Ranking**: Multi-factor product ranking algorithm
- **Cloud-Ready**: Designed for serverless deployment (AWS Lambda, Azure Functions, GCP Cloud Functions)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (SPA)                     │
│                    http://localhost:3000                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (FastAPI)                     │
│                    http://localhost:8080                     │
│  - Routes requests to microservices                          │
│  - Validates JWT tokens for protected routes                │
│  - Public routes: /products, /auth/login                     │
│  - Protected routes: /cart/*                                 │
└──────────┬─────────────────────┬──────────────┬─────────────┘
           │                     │              │
           ▼                     ▼              ▼
┌──────────────────┐  ┌────────────────┐  ┌──────────────┐
│ Product Service  │  │  Cart Service  │  │ Auth Service │
│   Port: 8001     │  │   Port: 8002   │  │  Port: 8003  │
│                  │  │                │  │              │
│ • GET /products  │  │ • GET /cart    │  │ • POST /login│
│ • GET /{id}      │  │ • POST /add    │  │ • POST       │
│ • Ranking logic  │  │ • PUT /update  │  │   /verify    │
│ • PUBLIC         │  │ • JWT Required │  │ • PUBLIC     │
└──────────────────┘  └────────────────┘  └──────────────┘
```

### Key Architectural Decisions

1. **API Gateway Pattern**: All client requests go through a single gateway
   - Simplifies client-side code
   - Centralized authentication
   - Service discovery abstraction

2. **JWT Authentication**: Stateless token-based auth
   - No session storage required
   - Serverless-friendly
   - Scalable across instances

3. **Microservices Independence**: Each service can be deployed separately
   - Independent scaling
   - Technology flexibility
   - Fault isolation

4. **Intelligent Product Ranking**: Multi-factor algorithm for product sorting
   - Popularity + Price + Rating + Sales + Recency
   - Demonstrates data-aware service capability

---

## ✨ Features

### Implemented

✅ **Product Ranking Service**
- Intelligent multi-factor ranking algorithm
- Query filtering (price range, rating)
- Multiple sort options (ranking, price, popularity, rating)
- 15 sample products with realistic data

✅ **Cart Service** (JWT Protected)
- Add/update/remove items
- Persistent cart per user
- Real-time cart count
- Price calculation

✅ **Authentication Service**
- JWT token generation
- Mock user database (demo credentials)
- Token verification endpoint

✅ **API Gateway**
- Request routing to microservices
- JWT validation middleware
- Public/protected route separation
- Error handling

✅ **React Frontend**
- Product browsing with filters
- User authentication (login/logout)
- Shopping cart management
- Responsive design

✅ **Docker Support**
- Individual Dockerfiles for each service
- Docker Compose for local orchestration
- Production-ready containers

✅ **Cloud Deployment Documentation**
- Terraform templates (AWS-focused)
- Serverless deployment guide
- Environment configuration

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | Python 3.11 + FastAPI | Fast, async API development |
| **Frontend** | React 18 + Vite | Modern SPA framework |
| **Authentication** | JWT (PyJWT) | Stateless auth tokens |
| **API Gateway** | FastAPI + httpx | Request routing & proxy |
| **Containerization** | Docker + Docker Compose | Local development & deployment |
| **IaC** | Terraform | Infrastructure as Code |
| **Testing** | pytest | Python unit tests |

---

## 📦 Prerequisites

### For Local Development

- **Python 3.11+**
- **Node.js 18+** and npm
- **Docker** and Docker Compose (recommended)
- **Git**

### For Cloud Deployment (Optional)

- AWS Account (or GCP/Azure)
- Terraform installed
- AWS CLI configured

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd ecommerce-microservices

# 2. Set environment variables (optional)
export JWT_SECRET="your-super-secret-key-here"

# 3. Start all services
docker-compose up --build

# 4. Access the application
# Frontend: http://localhost:3000
# API Gateway: http://localhost:8080
# Product Service: http://localhost:8001
# Cart Service: http://localhost:8002
# Auth Service: http://localhost:8003
```

### Option 2: Manual Setup

#### Backend Services

```bash
# Product Service
cd services/product-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main

# Cart Service (new terminal)
cd services/cart-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export JWT_SECRET="your-secret-key"
python -m app.main

# Auth Service (new terminal)
cd services/auth-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export JWT_SECRET="your-secret-key"
python -m app.main

# API Gateway (new terminal)
cd api-gateway
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export JWT_SECRET="your-secret-key"
python -m app.main
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Demo Credentials

```
Email: demo@example.com
Password: demo123

Email: john@example.com
Password: password123

Email: alice@example.com
Password: secure456
```

---

## 📚 API Documentation

### Public Endpoints (No Authentication)

#### Products

```bash
# Get all products (ranked)
GET /products
Query Params: ?sort_by=ranking&min_price=100&max_price=500&min_rating=4.0

# Get single product
GET /products/{product_id}

# Search products
GET /products/search/{query}
```

#### Authentication

```bash
# Login
POST /auth/login
Body: {"email": "demo@example.com", "password": "demo123"}
Response: {"access_token": "eyJ...", "user_id": "...", ...}

# Verify token
POST /auth/verify
Body: {"token": "eyJ..."}
```

### Protected Endpoints (JWT Required)

Add header: `Authorization: Bearer <your_jwt_token>`

#### Cart

```bash
# Get cart
GET /cart

# Add to cart
POST /cart/add
Body: {
  "product_id": "prod_001",
  "product_name": "Wireless Headphones",
  "price": 299.99,
  "quantity": 1
}

# Update quantity
PUT /cart/update/{product_id}?quantity=2

# Remove from cart
DELETE /cart/remove/{product_id}

# Clear cart
DELETE /cart/clear

# Get cart count
GET /cart/count
```

### Example Usage with cURL

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123"}' \
  | jq -r '.access_token')

# 2. Get products
curl http://localhost:8080/products

# 3. Add to cart (authenticated)
curl -X POST http://localhost:8080/cart/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "prod_001",
    "product_name": "Wireless Headphones",
    "price": 299.99,
    "quantity": 1
  }'

# 4. Get cart
curl http://localhost:8080/cart \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔐 Authentication Flow

```
┌──────────┐                ┌─────────────┐                ┌──────────┐
│  Client  │                │ API Gateway │                │   Auth   │
│ (React)  │                │             │                │ Service  │
└─────┬────┘                └──────┬──────┘                └─────┬────┘
      │                            │                             │
      │  1. POST /auth/login       │                             │
      │  (email, password)         │                             │
      ├───────────────────────────>│                             │
      │                            │  2. Forward credentials     │
      │                            ├────────────────────────────>│
      │                            │                             │
      │                            │  3. Validate & generate JWT │
      │                            │<────────────────────────────┤
      │  4. Return JWT token       │                             │
      │<───────────────────────────┤                             │
      │                            │                             │
      │  5. Store token (localStorage)                           │
      │                            │                             │
      │  6. POST /cart/add         │                             │
      │  (Authorization: Bearer <JWT>)                           │
      ├───────────────────────────>│                             │
      │                            │  7. Validate JWT            │
      │                            │  (middleware)               │
      │                            │                             │
      │                            │  8. Forward to Cart Service │
      │                            ├────────────────────────────>│
      │                            │                             │
      │  9. Success response       │                             │
      │<───────────────────────────┤                             │
```

---

## 🎯 Product Ranking Algorithm

The Product Ranking Service implements a sophisticated multi-factor scoring system:

### Factors & Weights

```python
weights = {
    'popularity': 0.30,    # 30% - User engagement/views
    'price': 0.20,         # 20% - Value for money (inverse)
    'rating': 0.25,        # 25% - Customer satisfaction
    'sales': 0.15,         # 15% - Sales velocity (log scale)
    'recency': 0.10        # 10% - New product boost
}
```

### Scoring Logic

1. **Popularity Score** (0-100): Direct value
2. **Price Score**: Logarithmic inverse normalization
   - Cheaper products score higher
   - `score = 50 + (50 * (1 - exp(-avg_price/price + 1)))`
3. **Rating Score**: Linear normalization
   - `score = (rating / 5.0) * 100`
4. **Sales Score**: Logarithmic scale
   - `score = (log10(sales + 1) / 4) * 100`
5. **Recency Score**: Time-based decay
   - Products ≤30 days old get boost
   - `score = 100 - (days_since_creation / 30) * 50`

### Additional Modifiers

- **Out of Stock**: score × 0.5
- **Low Stock** (<5 items): score × 0.8

### Example

```
Product: Wireless Headphones
- Popularity: 92/100 → 92 * 0.30 = 27.6
- Price: $299.99 → 65.4 * 0.20 = 13.08
- Rating: 4.7/5.0 → 94 * 0.25 = 23.5
- Sales: 2450 → 83.2 * 0.15 = 12.48
- Recency: 45 days → 75 * 0.10 = 7.5
-----------------------------------------
Final Score: 84.16
```

---

## ☁️ Cloud Deployment

This application is designed for serverless cloud deployment but implemented locally for evaluation.

### AWS Deployment Architecture

```
┌────────────────────────────────────────────────────────────┐
│                      AWS Cloud                              │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Amazon API Gateway                       │  │
│  │  - Single REST API endpoint                           │  │
│  │  - JWT authorizer for protected routes               │  │
│  │  - Request routing                                    │  │
│  └────────┬──────────────────┬──────────────┬───────────┘  │
│           │                  │              │               │
│           ▼                  ▼              ▼               │
│  ┌─────────────────┐  ┌────────────┐  ┌──────────┐        │
│  │ AWS Lambda      │  │ AWS Lambda │  │ AWS Lambda│        │
│  │ (Product        │  │ (Cart      │  │ (Auth     │        │
│  │  Service)       │  │  Service)  │  │  Service) │        │
│  └─────────────────┘  └────────────┘  └──────────┘        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  DynamoDB Tables                     │   │
│  │  - Products (optional - can use static JSON)        │   │
│  │  - Carts                                             │   │
│  │  - Users                                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │      Amazon S3 + CloudFront (Frontend)              │   │
│  │  - Static React SPA hosting                          │   │
│  │  - CDN for global distribution                       │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### Component Mapping

| Local Component | AWS Service | GCP Service | Azure Service |
|----------------|-------------|-------------|---------------|
| FastAPI Apps | Lambda Functions | Cloud Functions | Azure Functions |
| API Gateway | API Gateway | API Gateway | API Management |
| In-memory storage | DynamoDB | Firestore | Cosmos DB |
| React Frontend | S3 + CloudFront | Cloud Storage + CDN | Blob Storage + CDN |
| Environment vars | Lambda Environment | Function Config | App Settings |

### Terraform Deployment

Terraform configuration is provided in `infrastructure/terraform/`:

```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Review deployment plan
terraform plan

# Deploy to AWS
terraform apply

# Outputs will show:
# - API Gateway URL
# - Lambda function ARNs
# - Frontend S3 bucket URL
```

### Environment Variables (Production)

In production, configure these via AWS Systems Manager Parameter Store or Lambda Environment Variables:

```bash
JWT_SECRET=<your-strong-secret-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

---

## 📁 Project Structure

```
ecommerce-microservices/
├── README.md                    # This file
├── ARCHITECTURE.md              # Detailed architecture docs
├── docker-compose.yml           # Docker orchestration
├── .gitignore
│
├── services/
│   ├── product-service/         # Product Ranking Microservice
│   │   ├── app/
│   │   │   ├── main.py         # FastAPI app & endpoints
│   │   │   ├── models.py       # Pydantic models
│   │   │   ├── ranking.py      # Ranking algorithm
│   │   │   └── data.py         # Sample product data
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   ├── cart-service/            # Cart Management Microservice
│   │   ├── app/
│   │   │   ├── main.py         # FastAPI app (JWT protected)
│   │   │   ├── models.py       # Cart models
│   │   │   └── storage.py      # In-memory cart storage
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── README.md
│   │
│   └── auth-service/            # Authentication Microservice
│       ├── app/
│       │   ├── main.py         # FastAPI app
│       │   ├── models.py       # User models
│       │   └── jwt_handler.py  # JWT generation/validation
│       ├── tests/
│       ├── requirements.txt
│       ├── Dockerfile
│       └── README.md
│
├── api-gateway/                 # API Gateway
│   ├── app/
│   │   ├── main.py             # Gateway routing logic
│   │   └── middleware/
│   │       └── auth.py         # JWT validation middleware
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProductList.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   ├── Cart.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Navbar.jsx
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── context/
│   │   │   └── AuthContext.jsx # Auth state management
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── README.md
│
├── infrastructure/              # Cloud Infrastructure
│   ├── terraform/              # IaC templates
│   │   ├── main.tf
│   │   ├── api_gateway.tf
│   │   ├── lambda.tf
│   │   ├── iam.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── aws/
│       └── deployment-guide.md
│
└── docs/
    ├── API.md                  # API documentation
    ├── DEPLOYMENT.md           # Deployment guide
    ├── TESTING.md              # Testing guide
    └── architecture-diagram.png
```

---

## 🧪 Testing

### Backend Tests

```bash
# Product Service
cd services/product-service
pytest tests/ -v

# Cart Service
cd services/cart-service
pytest tests/ -v

# Auth Service
cd services/auth-service
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run test
```

### Integration Tests

```bash
# Start all services
docker-compose up -d

# Run integration tests
python integration_tests/test_e2e.py
```

### Manual Testing with Postman

Import the Postman collection from `docs/postman_collection.json`

---

## 🤔 Design Decisions

### Why Python + FastAPI?

- **Fast**: Async/await support, high performance
- **Type-safe**: Pydantic models for validation
- **Auto-docs**: Built-in OpenAPI/Swagger
- **Lambda-friendly**: Works well in serverless environments

### Why Microservices?

- **Scalability**: Scale services independently
- **Flexibility**: Use different technologies per service
- **Resilience**: Failure isolation
- **Team autonomy**: Different teams can own services

### Why JWT Authentication?

- **Stateless**: No session storage required
- **Serverless-friendly**: No shared state needed
- **Scalable**: Works across multiple instances
- **Standard**: Industry-standard approach

### Why API Gateway?

- **Single entry point**: Simplifies client code
- **Security**: Centralized authentication
- **Routing**: Abstract service locations
- **Monitoring**: Single place to add logging/metrics

### Storage Choices

**Local Development:**
- In-memory Python dictionaries
- Static JSON files
- Fast, simple, no setup required

**Production (Recommended):**
- Products: DynamoDB or PostgreSQL
- Cart: Redis (session-based) or DynamoDB (persistent)
- Users: PostgreSQL or DynamoDB

### Why This Ranking Algorithm?

- **Multi-factor**: Considers multiple aspects (not just price or popularity)
- **Balanced**: Weights reflect e-commerce priorities
- **Recency boost**: Highlights new products
- **Log scaling**: Handles outliers in sales/price
- **Stock awareness**: De-prioritizes out-of-stock items

---

## 🐛 Troubleshooting

### Docker Issues

```bash
# Clean rebuild
docker-compose down -v
docker-compose up --build

# Check logs
docker-compose logs -f [service-name]

# Restart single service
docker-compose restart [service-name]
```

### Port Conflicts

If ports are in use, edit `docker-compose.yml` to use different ports.

### JWT Token Issues

Ensure all services use the same `JWT_SECRET` environment variable.

---

## 📝 License

This project is for educational/demonstration purposes.

---

## 👤 Author

**Sohom Banerjee**
- Email: sohommister@gmail.com
- Assignment for: Take-Home Assignment - E-Commerce Microservices

---

## 🙏 Acknowledgments

Built as a demonstration of:
- Microservices architecture
- API Gateway pattern
- JWT authentication
- Intelligent ranking algorithms
- Cloud-ready design (serverless)
- Docker containerization
- Full-stack development (Python + React)

---

**Note**: This application is implemented locally for evaluation but designed with cloud deployment in mind. All services are stateless and can be deployed as AWS Lambda functions, Azure Functions, or GCP Cloud Functions with minimal modifications.