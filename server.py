from fastapi import FastAPI
from githubAgent.api_routes import router as api_routes

app = FastAPI()

@app.get("/")
def home():
    return {"Connected successfully"}

app.include_router(api_routes, prefix="/api")