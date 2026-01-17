"""
Data models for Product Service
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Product(BaseModel):
    """Core product model"""
    id: str
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Product price in USD")
    popularity: int = Field(ge=0, le=100, description="Popularity score 0-100")
    rating: float = Field(ge=0, le=5, description="Average rating 0-5")
    sales_count: int = Field(ge=0, description="Total number of sales")
    stock: int = Field(ge=0, description="Available stock")
    category: str
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "prod_001",
                "name": "Wireless Headphones",
                "description": "High-quality noise-cancelling headphones",
                "price": 199.99,
                "popularity": 85,
                "rating": 4.5,
                "sales_count": 1250,
                "stock": 45,
                "category": "Electronics",
                "image_url": "https://example.com/headphones.jpg"
            }
        }


class ProductResponse(Product):
    """Product response with ranking information"""
    rank: Optional[int] = Field(None, description="Product rank in the list")
    ranking_score: Optional[float] = Field(None, description="Calculated ranking score")