"""
Authentication Service
Handles user login and JWT token generation
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .models import LoginRequest, LoginResponse, User
from .jwt_handler import create_access_token, verify_token

app = FastAPI(
    title="Authentication Service",
    description="JWT-based authentication service",
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

# Mock user database
# In production: Replace with actual database (PostgreSQL, MongoDB, etc.)
USERS_DB = {
    "demo@example.com": User(
        user_id="user_001",
        email="demo@example.com",
        password="demo123",  # In production: Use hashed passwords (bcrypt)
        name="Demo User"
    ),
    "john@example.com": User(
        user_id="user_002",
        email="john@example.com",
        password="password123",
        name="John Doe"
    ),
    "alice@example.com": User(
        user_id="user_003",
        email="alice@example.com",
        password="secure456",
        name="Alice Smith"
    )
}


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "authentication"}


@app.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """
    Authenticate user and return JWT token
    
    Demo credentials:
    - Email: demo@example.com, Password: demo123
    - Email: john@example.com, Password: password123
    - Email: alice@example.com, Password: secure456
    """
    # Find user
    user = USERS_DB.get(request.email)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Verify password (in production, use bcrypt.checkpw)
    if user.password != request.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    token = create_access_token(
        user_id=user.user_id,
        email=user.email,
        name=user.name
    )
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.user_id,
        email=user.email,
        name=user.name
    )


@app.post("/auth/verify")
def verify_token_endpoint(token: str):
    """
    Verify if a token is valid
    Useful for API Gateway or client-side validation
    """
    try:
        payload = verify_token(token)
        return {
            "valid": True,
            "user_id": payload.get("user_id"),
            "email": payload.get("email")
        }
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )


@app.get("/auth/users")
def list_demo_users():
    """
    List available demo users (for testing purposes)
    Remove this endpoint in production!
    """
    return {
        "demo_users": [
            {
                "email": user.email,
                "password": "***",  # Don't expose passwords in production
                "name": user.name
            }
            for user in USERS_DB.values()
        ],
        "note": "This endpoint is for demo purposes only. Remove in production!"
    }


# Lambda handler for AWS deployment
def lambda_handler(event, context):
    """AWS Lambda handler"""
    from mangum import Mangum
    handler = Mangum(app)
    return handler(event, context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)