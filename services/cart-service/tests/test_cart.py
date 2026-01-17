import pytest
from app.storage import (
    get_cart,
    add_to_cart,
    remove_from_cart,
    update_cart_item,
    clear_cart,
    get_cart_count
)

def test_get_cart():
    cart = get_cart("user123")
    assert cart.user_id == "user123"
    assert len(cart.items) == 0

def test_add_to_cart():
    cart = add_to_cart("user123", 1, 2, 29.99)
    assert len(cart.items) == 1
    assert cart.items[0].product_id == 1
    assert cart.items[0].quantity == 2

def test_add_same_product_twice():
    add_to_cart("user456", 1, 2, 29.99)
    cart = add_to_cart("user456", 1, 3, 29.99)
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 5

def test_remove_from_cart():
    add_to_cart("user789", 1, 2, 29.99)
    cart = remove_from_cart("user789", 1)
    assert len(cart.items) == 0

def test_update_cart_item():
    add_to_cart("user111", 1, 2, 29.99)
    cart = update_cart_item("user111", 1, 5)
    assert cart.items[0].quantity == 5

def test_clear_cart():
    add_to_cart("user222", 1, 2, 29.99)
    add_to_cart("user222", 2, 3, 49.99)
    cart = clear_cart("user222")
    assert len(cart.items) == 0
    assert cart.total_price == 0.0

def test_get_cart_count():
    add_to_cart("user333", 1, 2, 29.99)
    add_to_cart("user333", 2, 3, 49.99)
    count = get_cart_count("user333")
    assert count == 5
