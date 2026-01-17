"""
Data models for Cart Service
"""
from pydantic import BaseModel, Field
from typing import List


class CartItem(BaseModel):
    """Individual item in shopping cart"""
    product_id: str
    product_name: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "prod_001",
                "product_name": "Wireless Headphones",
                "price": 199.99,
                "quantity": 2
            }
        }


class CartResponse(BaseModel):
    """Complete cart response"""
    user_id: str
    items: List[CartItem]
    total_items: int
    total_price: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "items": [
                    {
                        "product_id": "prod_001",
                        "product_name": "Wireless Headphones",
                        "price": 199.99,
                        "quantity": 2
                    }
                ],
                "total_items": 2,
                "total_price": 399.98
            }
        }


class AddToCartRequest(BaseModel):
    """Request to add item to cart"""
    product_id: str
    product_name: str
    price: float = Field(gt=0)
    quantity: int = Field(default=1, gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "prod_001",
                "product_name": "Wireless Headphones",
                "price": 199.99,
                "quantity": 1
            }
        }