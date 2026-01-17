from fastapi import FastAPI

app = FastAPI(title="Auth Service", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Auth Service is running"}

@app.post("/login")
async def login(credentials: dict):
    return {"token": "sample_token"}

@app.post("/register")
async def register(user: dict):
    return {"message": "User registered"}