from pydantic import BaseModel
from typing import Optional, List

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    category: str
    rating: float = 0.0
    reviews_count: int = 0

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    category: str
    rating: float
    reviews_count: int

    class Config:
        from_attributes = True
