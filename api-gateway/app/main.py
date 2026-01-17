"""
API Gateway
Single entry point for all microservices
Routes requests and enforces authentication
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import uvicorn
import os

from .middleware.auth import validate_jwt_token

app = FastAPI(
    title="E-Commerce API Gateway",
    description="Unified API Gateway for microservices",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: Specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs (configured via environment variables)
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://localhost:8002")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8003")


@app.get("/")
def root():
    """API Gateway health check"""
    return {
        "service": "api-gateway",
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "product": PRODUCT_SERVICE_URL,
            "cart": CART_SERVICE_URL,
            "auth": AUTH_SERVICE_URL
        }
    }


# ============================================================================
# PRODUCT SERVICE ROUTES (PUBLIC - No Authentication Required)
# ============================================================================

@app.get("/products")
async def get_products(request: Request):
    """
    Get all products (ranked)
    PUBLIC ENDPOINT - No authentication required
    """
    async with httpx.AsyncClient() as client:
        try:
            # Forward query parameters
            params = dict(request.query_params)
            response = await client.get(
                f"{PRODUCT_SERVICE_URL}/products",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Product service error: {str(e)}"
            )


@app.get("/products/{product_id}")
async def get_product(product_id: str):
    """
    Get specific product by ID
    PUBLIC ENDPOINT - No authentication required
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{PRODUCT_SERVICE_URL}/products/{product_id}",
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Product not found")
            raise HTTPException(status_code=500, detail="Product service error")


@app.get("/products/search/{query}")
async def search_products(query: str):
    """
    Search products
    PUBLIC ENDPOINT - No authentication required
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{PRODUCT_SERVICE_URL}/products/search/{query}",
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Product service error")


# ============================================================================
# CART SERVICE ROUTES (PROTECTED - JWT Authentication Required)
# ============================================================================

@app.get("/cart")
async def get_cart(request: Request):
    """
    Get user's cart
    PROTECTED ENDPOINT - Requires JWT authentication
    """
    # Validate JWT and extract user_id
    user_id = await validate_jwt_token(request)
    
    async with httpx.AsyncClient() as client:
        try:
            # Forward request with Authorization header
            auth_header = request.headers.get("authorization")
            headers = {"authorization": auth_header}
            
            response = await client.get(
                f"{CART_SERVICE_URL}/cart",
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Cart service error")


@app.post("/cart/add")
async def add_to_cart(request: Request):
    """
    Add item to cart
    PROTECTED ENDPOINT - Requires JWT authentication
    """
    # Validate JWT
    user_id = await validate_jwt_token(request)
    
    # Get request body
    body = await request.json()
    
    async with httpx.AsyncClient() as client:
        try:
            auth_header = request.headers.get("authorization")
            headers = {"authorization": auth_header}
            
            response = await client.post(
                f"{CART_SERVICE_URL}/cart/add",
                json=body,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Cart service error")
            )


@app.put("/cart/update/{product_id}")
async def update_cart_item(product_id: str, request: Request):
    """
    Update cart item quantity
    PROTECTED ENDPOINT - Requires JWT authentication
    """
    user_id = await validate_jwt_token(request)
    
    params = dict(request.query_params)
    
    async with httpx.AsyncClient() as client:
        try:
            auth_header = request.headers.get("authorization")
            headers = {"authorization": auth_header}
            
            response = await client.put(
                f"{CART_SERVICE_URL}/cart/update/{product_id}",
                params=params,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Cart service error")


@app.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: str, request: Request):
    """
    Remove item from cart
    PROTECTED ENDPOINT - Requires JWT authentication
    """
    user_id = await validate_jwt_token(request)
    
    async with httpx.AsyncClient() as client:
        try:
            auth_header = request.headers.get("authorization")
            headers = {"authorization": auth_header}
            
            response = await client.delete(
                f"{CART_SERVICE_URL}/cart/remove/{product_id}",
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Cart service error")


@app.delete("/cart/clear")
async def clear_cart(request: Request):
    """
    Clear entire cart
    PROTECTED ENDPOINT - Requires JWT authentication
    """
    user_id = await validate_jwt_token(request)
    
    async with httpx.AsyncClient() as client:
        try:
            auth_header = request.headers.get("authorization")
            headers = {"authorization": auth_header}
            
            response = await client.delete(
                f"{CART_SERVICE_URL}/cart/clear",
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Cart service error")


@app.get("/cart/count")
async def get_cart_count(request: Request):
    """
    Get cart item count
    PROTECTED ENDPOINT - Requires JWT authentication
    """
    user_id = await validate_jwt_token(request)
    
    async with httpx.AsyncClient() as client:
        try:
            auth_header = request.headers.get("authorization")
            headers = {"authorization": auth_header}
            
            response = await client.get(
                f"{CART_SERVICE_URL}/cart/count",
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Cart service error")


# ============================================================================
# AUTHENTICATION SERVICE ROUTES (PUBLIC)
# ============================================================================

@app.post("/auth/login")
async def login(request: Request):
    """
    User login
    PUBLIC ENDPOINT - Returns JWT token
    """
    body = await request.json()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/auth/login",
                json=body,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Authentication failed")
            )


@app.post("/auth/verify")
async def verify_token(request: Request):
    """
    Verify JWT token
    PUBLIC ENDPOINT
    """
    body = await request.json()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/auth/verify",
                json=body,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/auth/users")
async def list_demo_users():
    """
    List demo users (for testing)
    Remove in production!
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/auth/users",
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Auth service error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)