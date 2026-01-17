from fastapi import FastAPI

app = FastAPI(title="Cart Service", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Cart Service is running"}

@app.get("/cart")
async def get_cart():
    return {"cart": []}

@app.post("/cart")
async def add_to_cart(item: dict):
    return {"message": "Item added to cart"}