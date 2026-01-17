"""
In-memory cart storage
"""

from typing import Dict, List, Optional
from .models import Cart, CartItem

# In-memory storage for carts
CARTS: Dict[str, Cart] = {}

def get_cart(user_id: str) -> Optional[Cart]:
    """Get cart for a user"""
    if user_id not in CARTS:
        CARTS[user_id] = Cart(user_id=user_id, items=[], total_price=0.0)
    return CARTS[user_id]

def add_to_cart(user_id: str, product_id: int, quantity: int, price: float) -> Cart:
    """Add item to cart"""
    cart = get_cart(user_id)
    
    # Check if item already exists
    existing_item = None
    for item in cart.items:
        if item.product_id == product_id:
            existing_item = item
            break
    
    if existing_item:
        existing_item.quantity += quantity
    else:
        cart.items.append(CartItem(product_id=product_id, quantity=quantity, price=price))
    
    update_cart_total(cart)
    return cart

def remove_from_cart(user_id: str, product_id: int) -> Cart:
    """Remove item from cart"""
    cart = get_cart(user_id)
    cart.items = [item for item in cart.items if item.product_id != product_id]
    update_cart_total(cart)
    return cart

def update_cart_item(user_id: str, product_id: int, quantity: int) -> Cart:
    """Update quantity of an item in cart"""
    cart = get_cart(user_id)
    
    for item in cart.items:
        if item.product_id == product_id:
            if quantity <= 0:
                cart.items.remove(item)
            else:
                item.quantity = quantity
            break
    
    update_cart_total(cart)
    return cart

def clear_cart(user_id: str) -> Cart:
    """Clear entire cart"""
    cart = get_cart(user_id)
    cart.items = []
    cart.total_price = 0.0
    return cart

def update_cart_total(cart: Cart) -> None:
    """Update total price of cart"""
    cart.total_price = sum(item.price * item.quantity for item in cart.items)

def get_cart_count(user_id: str) -> int:
    """Get total item count in cart"""
    cart = get_cart(user_id)
    return sum(item.quantity for item in cart.items)
