import pytest
from app.ranking import (
    rank_products_by_rating,
    rank_products_by_popularity,
    rank_products_by_price_low_to_high,
    filter_by_category,
    filter_in_stock,
    search_products
)

# Sample test data
test_products = [
    {"id": 1, "name": "Laptop", "price": 1299.99, "stock": 10, "rating": 4.5, "reviews_count": 120, "category": "Electronics"},
    {"id": 2, "name": "Mouse", "price": 29.99, "stock": 50, "rating": 4.2, "reviews_count": 340, "category": "Accessories"},
    {"id": 3, "name": "Cable", "price": 12.99, "stock": 0, "rating": 4.0, "reviews_count": 450, "category": "Cables"},
]

def test_rank_products_by_rating():
    ranked = rank_products_by_rating(test_products)
    assert ranked[0]["rating"] == 4.5
    assert ranked[-1]["rating"] == 4.0

def test_rank_products_by_popularity():
    ranked = rank_products_by_popularity(test_products)
    assert ranked[0]["reviews_count"] == 450
    assert ranked[-1]["reviews_count"] == 120

def test_rank_products_by_price_low_to_high():
    ranked = rank_products_by_price_low_to_high(test_products)
    assert ranked[0]["price"] == 12.99
    assert ranked[-1]["price"] == 1299.99

def test_filter_by_category():
    filtered = filter_by_category(test_products, "Electronics")
    assert len(filtered) == 1
    assert filtered[0]["name"] == "Laptop"

def test_filter_in_stock():
    filtered = filter_in_stock(test_products)
    assert len(filtered) == 2
    assert all(p["stock"] > 0 for p in filtered)

def test_search_products():
    results = search_products("Laptop")
    assert len(results) == 1
    assert results[0]["name"] == "Laptop"
