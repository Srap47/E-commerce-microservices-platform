# Cart routes
from fastapi import APIRouter

router = APIRouter()

@router.get("/cart")
async def get_cart():
    # Proxy to cart service
    return {"cart": []}