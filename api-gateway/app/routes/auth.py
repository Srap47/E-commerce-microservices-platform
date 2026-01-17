# Auth routes
from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login(credentials: dict):
    # Proxy to auth service
    return {"token": "sample_token"}