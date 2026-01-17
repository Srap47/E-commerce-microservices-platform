"""
Product Ranking Service
Handles product listing with intelligent ranking algorithm
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

from .models import Product, ProductResponse
from .ranking import ProductRanker
from .data import get_products_data

app = FastAPI(
    title="Product Ranking Service",
    description="E-commerce product service with intelligent ranking",
    version="1.0.0"
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ranker and load data
ranker = ProductRanker()
products_db = get_products_data()


@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "product-ranking"}


@app.get("/products", response_model=List[ProductResponse])
def get_products(
    sort_by: Optional[str] = "ranking",
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None
):
    """
    Get all products with ranking applied
    
    Query Parameters:
    - sort_by: ranking (default), price, popularity, rating
    - min_price: Filter by minimum price
    - max_price: Filter by maximum price
    - min_rating: Filter by minimum rating
    """
    # Apply filters
    filtered_products = products_db.copy()
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p.price >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p.price <= max_price]
    
    if min_rating is not None:
        filtered_products = [p for p in filtered_products if p.rating >= min_rating]
    
    # Apply ranking
    if sort_by == "ranking":
        ranked_products = ranker.rank_products(filtered_products)
    elif sort_by == "price":
        ranked_products = sorted(filtered_products, key=lambda x: x.price)
    elif sort_by == "popularity":
        ranked_products = sorted(filtered_products, key=lambda x: x.popularity, reverse=True)
    elif sort_by == "rating":
        ranked_products = sorted(filtered_products, key=lambda x: x.rating, reverse=True)
    else:
        ranked_products = ranker.rank_products(filtered_products)
    
    # Convert to response format with ranking scores
    response = []
    for idx, product in enumerate(ranked_products):
        score = ranker.calculate_score(product) if sort_by == "ranking" else None
        response.append(
            ProductResponse(
                **product.dict(),
                rank=idx + 1,
                ranking_score=score
            )
        )
    
    return response


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    """Get a specific product by ID"""
    product = next((p for p in products_db if p.id == product_id), None)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Calculate ranking score for this product
    score = ranker.calculate_score(product)
    
    return ProductResponse(
        **product.dict(),
        rank=None,  # Single product doesn't have a rank
        ranking_score=score
    )


@app.get("/products/search/{query}")
def search_products(query: str):
    """Search products by name or description"""
    query_lower = query.lower()
    results = [
        p for p in products_db 
        if query_lower in p.name.lower() or 
           (p.description and query_lower in p.description.lower())
    ]
    
    # Rank the search results
    ranked_results = ranker.rank_products(results)
    
    response = []
    for idx, product in enumerate(ranked_results):
        score = ranker.calculate_score(product)
        response.append(
            ProductResponse(
                **product.dict(),
                rank=idx + 1,
                ranking_score=score
            )
        )
    
    return response


# Lambda handler for AWS deployment
def lambda_handler(event, context):
    """
    AWS Lambda handler
    This allows the same code to run as a Lambda function
    """
    from mangum import Mangum
    handler = Mangum(app)
    return handler(event, context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)