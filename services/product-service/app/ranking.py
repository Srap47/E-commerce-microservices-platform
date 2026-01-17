"""
Product Ranking Algorithm
Implements sophisticated multi-factor ranking for e-commerce products
"""
import math
from datetime import datetime, timedelta
from typing import List
from .models import Product


class ProductRanker:
    """
    Intelligent product ranking system
    
    Ranking Factors:
    1. Popularity (30%) - Direct popularity score
    2. Price Score (20%) - Inverse price normalization (cheaper = better value)
    3. Rating (25%) - Customer satisfaction
    4. Sales Velocity (15%) - Recent sales performance
    5. Recency (10%) - Boost for newer products
    """
    
    def __init__(self):
        # Configurable weights for different ranking factors
        self.weights = {
            'popularity': 0.30,
            'price': 0.20,
            'rating': 0.25,
            'sales': 0.15,
            'recency': 0.10
        }
        
        # Reference values for normalization
        self.avg_price = 500.0  # Reference price for normalization
        self.recency_window_days = 30  # Products within 30 days get recency boost
    
    def calculate_score(self, product: Product) -> float:
        """
        Calculate comprehensive ranking score for a product
        
        Returns a score between 0 and 100
        """
        # 1. Popularity Score (0-100, already normalized)
        popularity_score = product.popularity
        
        # 2. Price Score (inverse - cheaper products score higher)
        # Using logarithmic scale to handle wide price ranges
        price_score = self._calculate_price_score(product.price)
        
        # 3. Rating Score (0-5 scale, normalize to 0-100)
        rating_score = (product.rating / 5.0) * 100
        
        # 4. Sales Velocity Score
        # Use logarithmic scale to handle outliers
        sales_score = self._calculate_sales_score(product.sales_count)
        
        # 5. Recency Score (boost for new products)
        recency_score = self._calculate_recency_score(product.created_at)
        
        # Calculate weighted average
        total_score = (
            popularity_score * self.weights['popularity'] +
            price_score * self.weights['price'] +
            rating_score * self.weights['rating'] +
            sales_score * self.weights['sales'] +
            recency_score * self.weights['recency']
        )
        
        # Apply stock penalty (out of stock products ranked lower)
        if product.stock == 0:
            total_score *= 0.5
        elif product.stock < 5:
            total_score *= 0.8
        
        return round(total_score, 2)
    
    def _calculate_price_score(self, price: float) -> float:
        """
        Calculate price score using inverse logarithmic normalization
        Lower prices get higher scores (better value)
        """
        if price <= 0:
            return 0
        
        # Logarithmic normalization relative to average price
        # Products at avg_price get score of 50
        # Cheaper products score higher, expensive products score lower
        ratio = self.avg_price / price
        
        if ratio >= 1:
            # Product is cheaper than average
            score = 50 + (50 * (1 - math.exp(-ratio + 1)))
        else:
            # Product is more expensive than average
            score = 50 * math.exp(-1 / ratio + 1)
        
        return min(100, max(0, score))
    
    def _calculate_sales_score(self, sales_count: int) -> float:
        """
        Calculate sales score using logarithmic scale
        Handles wide range of sales numbers gracefully
        """
        if sales_count <= 0:
            return 0
        
        # Logarithmic scale: log10(sales + 1) normalized
        # 10 sales = ~25, 100 sales = ~50, 1000 sales = ~75, 10000 sales = ~100
        score = (math.log10(sales_count + 1) / 4) * 100
        
        return min(100, max(0, score))
    
    def _calculate_recency_score(self, created_at: datetime) -> float:
        """
        Calculate recency boost for new products
        Products added within the recency window get a boost
        """
        days_since_creation = (datetime.now() - created_at).days
        
        if days_since_creation < 0:
            # Future date (data error), no boost
            return 0
        
        if days_since_creation >= self.recency_window_days:
            # Older products get baseline score
            return 50
        
        # Linear decay from 100 to 50 over the recency window
        boost = 100 - ((days_since_creation / self.recency_window_days) * 50)
        
        return max(50, boost)
    
    def rank_products(self, products: List[Product]) -> List[Product]:
        """
        Rank a list of products by calculated scores
        Returns products sorted by ranking score (highest first)
        """
        # Calculate scores for all products
        scored_products = [
            (product, self.calculate_score(product))
            for product in products
        ]
        
        # Sort by score (descending)
        scored_products.sort(key=lambda x: x[1], reverse=True)
        
        # Return sorted products
        return [product for product, score in scored_products]
    
    def explain_ranking(self, product: Product) -> dict:
        """
        Explain the ranking score breakdown for a product
        Useful for debugging and transparency
        """
        popularity_score = product.popularity
        price_score = self._calculate_price_score(product.price)
        rating_score = (product.rating / 5.0) * 100
        sales_score = self._calculate_sales_score(product.sales_count)
        recency_score = self._calculate_recency_score(product.created_at)
        
        return {
            'product_id': product.id,
            'product_name': product.name,
            'final_score': self.calculate_score(product),
            'breakdown': {
                'popularity': {
                    'score': popularity_score,
                    'weight': self.weights['popularity'],
                    'contribution': popularity_score * self.weights['popularity']
                },
                'price': {
                    'score': price_score,
                    'weight': self.weights['price'],
                    'contribution': price_score * self.weights['price']
                },
                'rating': {
                    'score': rating_score,
                    'weight': self.weights['rating'],
                    'contribution': rating_score * self.weights['rating']
                },
                'sales': {
                    'score': sales_score,
                    'weight': self.weights['sales'],
                    'contribution': sales_score * self.weights['sales']
                },
                'recency': {
                    'score': recency_score,
                    'weight': self.weights['recency'],
                    'contribution': recency_score * self.weights['recency']
                }
            },
            'stock_status': 'in_stock' if product.stock > 0 else 'out_of_stock'
        }