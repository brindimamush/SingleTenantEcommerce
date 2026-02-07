from fastapi import FastAPI
from app.core.config import settings
from app.api.health import router as health_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "Telegram E-Commerce API running"}
