"""
JWT token generation and verification
"""
import jwt
from datetime import datetime, timedelta
import os


# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24  # Token valid for 24 hours


def create_access_token(user_id: str, email: str, name: str) -> str:
    """
    Create a JWT access token
    
    Args:
        user_id: Unique user identifier
        email: User email
        name: User display name
    
    Returns:
        JWT token string
    """
    # Calculate expiration time
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    # Create payload
    payload = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    # Generate token
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dictionary
    
    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")


def decode_token_without_verification(token: str) -> dict:
    """
    Decode token without verification (for debugging only)
    DO NOT USE IN PRODUCTION for authentication
    """
    return jwt.decode(token, options={"verify_signature": False})