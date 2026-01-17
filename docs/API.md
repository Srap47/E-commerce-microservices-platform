# E-Commerce API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Products

#### Get All Products
```http
GET /products
```

Response:
```json
{
  "products": [
    {
      "id": 1,
      "name": "Laptop",
      "description": "High-performance laptop",
      "price": 1299.99,
      "stock": 10,
      "category": "Electronics",
      "rating": 4.5,
      "reviews_count": 120
    }
  ]
}
```

#### Get Product by ID
```http
GET /products/{product_id}
```

#### Search Products
```http
GET /products/search?q=laptop
```

#### Get Recommended Products
```http
GET /products/recommended
```

### Cart

#### Get Cart
```http
GET /cart/{user_id}
```

#### Add to Cart
```http
POST /cart/{user_id}/items
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2,
  "price": 1299.99
}
```

#### Remove from Cart
```http
DELETE /cart/{user_id}/items/{product_id}
```

#### Update Cart Item
```http
PUT /cart/{user_id}/items/{product_id}
Content-Type: application/json

{
  "quantity": 5
}
```

### Authentication

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

Response:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## Error Responses

```json
{
  "detail": "Product not found",
  "status": 404,
  "timestamp": "2024-01-16T10:00:00Z"
}
```

## Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Missing or invalid token
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
