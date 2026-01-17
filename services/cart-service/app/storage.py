"""
Cart storage implementation
Uses in-memory storage (dict) for local development
In production: Replace with Redis, DynamoDB, or other persistent storage
"""
from typing import List, Dict
from .models import CartItem


class CartStorage:
    """
    In-memory cart storage
    Thread-safe for single instance
    
    In production, replace with:
    - Redis (for session-based carts)
    - DynamoDB (for persistent carts)
    - PostgreSQL/MySQL (for relational storage)
    """
    
    def __init__(self):
        # Structure: {user_id: {product_id: CartItem}}
        self._carts: Dict[str, Dict[str, CartItem]] = {}
    
    def get_cart(self, user_id: str) -> List[CartItem]:
        """Get all items in user's cart"""
        if user_id not in self._carts:
            return []
        
        return list(self._carts[user_id].values())
    
    def add_item(
        self,
        user_id: str,
        product_id: str,
        product_name: str,
        price: float,
        quantity: int = 1
    ) -> None:
        """
        Add item to cart
        If item already exists, increase quantity
        """
        if user_id not in self._carts:
            self._carts[user_id] = {}
        
        if product_id in self._carts[user_id]:
            # Item already in cart, increase quantity
            self._carts[user_id][product_id].quantity += quantity
        else:
            # New item
            self._carts[user_id][product_id] = CartItem(
                product_id=product_id,
                product_name=product_name,
                price=price,
                quantity=quantity
            )
    
    def update_quantity(
        self,
        user_id: str,
        product_id: str,
        quantity: int
    ) -> None:
        """Update quantity of an item in cart"""
        if user_id not in self._carts or product_id not in self._carts[user_id]:
            raise ValueError(f"Product {product_id} not found in cart")
        
        self._carts[user_id][product_id].quantity = quantity
    
    def remove_item(self, user_id: str, product_id: str) -> None:
        """Remove item from cart"""
        if user_id not in self._carts or product_id not in self._carts[user_id]:
            raise ValueError(f"Product {product_id} not found in cart")
        
        del self._carts[user_id][product_id]
        
        # Clean up empty cart
        if not self._carts[user_id]:
            del self._carts[user_id]
    
    def clear_cart(self, user_id: str) -> None:
        """Clear all items from cart"""
        if user_id in self._carts:
            del self._carts[user_id]
    
    def get_item_count(self, user_id: str) -> int:
        """Get total number of items in cart"""
        if user_id not in self._carts:
            return 0
        
        return sum(item.quantity for item in self._carts[user_id].values())