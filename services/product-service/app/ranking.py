"""
Product ranking and recommendation engine
"""

from typing import List
from .data import get_all_products

def rank_products_by_rating(products: List[dict]) -> List[dict]:
    """Rank products by rating in descending order"""
    return sorted(products, key=lambda x: x["rating"], reverse=True)

def rank_products_by_popularity(products: List[dict]) -> List[dict]:
    """Rank products by reviews count (popularity) in descending order"""
    return sorted(products, key=lambda x: x["reviews_count"], reverse=True)

def rank_products_by_price_low_to_high(products: List[dict]) -> List[dict]:
    """Rank products by price from low to high"""
    return sorted(products, key=lambda x: x["price"])

def rank_products_by_price_high_to_low(products: List[dict]) -> List[dict]:
    """Rank products by price from high to low"""
    return sorted(products, key=lambda x: x["price"], reverse=True)

def filter_by_category(products: List[dict], category: str) -> List[dict]:
    """Filter products by category"""
    return [p for p in products if p["category"].lower() == category.lower()]

def filter_in_stock(products: List[dict]) -> List[dict]:
    """Filter only in-stock products"""
    return [p for p in products if p["stock"] > 0]

def get_recommended_products(limit: int = 5) -> List[dict]:
    """Get top recommended products based on rating and reviews"""
    products = get_all_products()
    products_in_stock = filter_in_stock(products)
    ranked = rank_products_by_rating(products_in_stock)
    return ranked[:limit]

def search_products(query: str) -> List[dict]:
    """Search products by name or description"""
    products = get_all_products()
    query_lower = query.lower()
    return [p for p in products if query_lower in p["name"].lower() or query_lower in p["description"].lower()]
