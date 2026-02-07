from app.core.database import SessionLocal
from app.db.models.product import Product

db = SessionLocal()

products = [
    Product(name="Laptop", description="Powerful laptop", price=1200, stock=5),
    Product(name="Phone", description="Smartphone", price=600, stock=10),
    Product(name="Headphones", description="Noise cancelling", price=150, stock=20),
]

db.add_all(products)
db.commit()
db.close()

print("Products seeded")
