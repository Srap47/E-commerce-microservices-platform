from pydantic import BaseModel
from typing import List, Optional

class CartItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []
    total_price: float = 0.0

class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int
    price: float

class RemoveFromCartRequest(BaseModel):
    product_id: int

class UpdateCartItemRequest(BaseModel):
    product_id: int
    quantity: int

class CartResponse(BaseModel):
    user_id: str
    items: List[CartItem]
    total_price: float
    item_count: int

    class Config:
        from_attributes = True
