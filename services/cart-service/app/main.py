"""
Cart Service
Handles user shopping cart operations
Requires JWT authentication
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
import jwt
import os

from .models import CartItem, CartResponse, AddToCartRequest
from .storage import CartStorage

app = FastAPI(
    title="Cart Service",
    description="E-commerce cart management service (JWT protected)",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize cart storage
cart_storage = CartStorage()

# JWT secret (in production, use environment variable)
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"


def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Verify JWT token and extract user_id
    This function is used as a dependency for protected endpoints
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    
    try:
        # Extract token from "Bearer <token>" format
        if authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
        else:
            token = authorization
        
        # Decode and verify token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: user_id missing"
            )
        
        return user_id
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cart"}


@app.get("/cart", response_model=CartResponse)
def get_cart(user_id: str = Depends(verify_token)):
    """
    Get the current user's cart
    Requires valid JWT token
    """
    cart_items = cart_storage.get_cart(user_id)
    
    # Calculate totals
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.price * item.quantity for item in cart_items)
    
    return CartResponse(
        user_id=user_id,
        items=cart_items,
        total_items=total_items,
        total_price=round(total_price, 2)
    )


@app.post("/cart/add")
def add_to_cart(
    request: AddToCartRequest,
    user_id: str = Depends(verify_token)
):
    """
    Add a product to the user's cart
    Requires valid JWT token
    """
    try:
        cart_storage.add_item(
            user_id=user_id,
            product_id=request.product_id,
            product_name=request.product_name,
            price=request.price,
            quantity=request.quantity
        )
        
        return {
            "message": "Product added to cart successfully",
            "product_id": request.product_id,
            "quantity": request.quantity
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/cart/update/{product_id}")
def update_cart_item(
    product_id: str,
    quantity: int,
    user_id: str = Depends(verify_token)
):
    """
    Update quantity of a product in cart
    Set quantity to 0 to remove item
    """
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    
    try:
        if quantity == 0:
            cart_storage.remove_item(user_id, product_id)
            return {"message": "Product removed from cart"}
        else:
            cart_storage.update_quantity(user_id, product_id, quantity)
            return {"message": "Cart updated successfully"}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/cart/remove/{product_id}")
def remove_from_cart(
    product_id: str,
    user_id: str = Depends(verify_token)
):
    """Remove a product from cart"""
    try:
        cart_storage.remove_item(user_id, product_id)
        return {"message": "Product removed from cart"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/cart/clear")
def clear_cart(user_id: str = Depends(verify_token)):
    """Clear all items from cart"""
    cart_storage.clear_cart(user_id)
    return {"message": "Cart cleared successfully"}


@app.get("/cart/count")
def get_cart_count(user_id: str = Depends(verify_token)):
    """Get total number of items in cart (useful for navbar badge)"""
    cart_items = cart_storage.get_cart(user_id)
    total_items = sum(item.quantity for item in cart_items)
    
    return {"count": total_items}


# Lambda handler for AWS deployment
def lambda_handler(event, context):
    """AWS Lambda handler"""
    from mangum import Mangum
    handler = Mangum(app)
    return handler(event, context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)