# Product routes
from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def get_products():
    # Proxy to product service
    return {"products": []}