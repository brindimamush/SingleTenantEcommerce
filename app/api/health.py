from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.db.models.product import Product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
def health_check():
    return {
        "status": "ok"
    }

@router.get("/products-test")
def products_test(db: Session = Depends(get_db)):
    return db.query(Product).all()