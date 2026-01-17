from fastapi import FastAPI

app = FastAPI(title="API Gateway", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "API Gateway is running"}

# Routes will be added here