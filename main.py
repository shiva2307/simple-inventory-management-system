from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Productc
from db import session, engine
from sqlalchemy.orm import Session
import datbase_models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# In-memory products (used by the API)
Products = [
    Productc(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Productc(id=2, name="Smartphone", description="A latest model smartphone", price=699.99, quantity=25),
    Productc(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
    Productc(id=4, name="Monitor", description="4K UHD monitor", price=399.99, quantity=8),
    Productc(id=5, name="Keyboard", description="Mechanical keyboard", price=89.99, quantity=30),
]

# Create tables
datbase_models.Base.metadata.create_all(bind=engine)


# Seed the database once (defensive: skip existing IDs)
def init_db():
    db = session()
    try:
        for prod in Products:
            # Skip seeding if the product already exists
            exists = db.query(datbase_models.Product).filter(datbase_models.Product.id == prod.id).first()
            if exists:
                continue
            payload = prod.model_dump() if callable(getattr(prod, "model_dump", None)) else prod.dict()
            db_product = datbase_models.Product(**payload)
            db.add(db_product)
        db.commit()
    finally:
        db.close()


init_db()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def get_products(db:Session=Depends(get_db)):
    db_products = db.query(datbase_models.Product).all()
    return db_products


@app.get("/products/{id}")
def get_product(id: int,db:Session=Depends(get_db)):
    db_product = db.query(datbase_models.Product).filter(datbase_models.Product.id == id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}


@app.post("/products")
def create_product(product: Productc, db:Session=Depends(get_db)):
    db.add(datbase_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, updated_product: Productc, db:Session=Depends(get_db)):
    db_product = db.query(datbase_models.Product).filter(datbase_models.Product.id == id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return updated_product
    return {"error": "Product not found"}
    


@app.delete("/products/{id}")
def delete_product(id: int,db:Session=Depends(get_db)):
    db_product=db.query(datbase_models.Product).filter(datbase_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}  
    return {"error": "Product not found"}
