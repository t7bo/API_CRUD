from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Product, ProductCreate
from app.database import SessionLocal
from typing import List

product_router = APIRouter()

# Route pour afficher tous les produits existants
@product_router.get("/products", response_model=List[Product])
def get_products():
    with SessionLocal() as session:
        return session.query(Product).all()

# Route pour obtenir les informations d'un produit par son ID
@product_router.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    with SessionLocal() as session:
        product = session.query(Product).filter(Product.ProductID == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

# Route pour créer un produit
@product_router.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    new_product = Product(**product.dict())
    with SessionLocal() as session:
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
    return new_product

# Route pour mettre à jour un produit existant
@product_router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate):
    with SessionLocal() as session:
        existing_product = session.query(Product).filter(Product.ProductID == product_id).first()
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Mise à jour des informations
        existing_product.Name = product.Name
        existing_product.Price = product.Price
        session.commit()
        session.refresh(existing_product)  # Rafraîchit l'instance pour obtenir les nouvelles valeurs
    return existing_product

# Route pour supprimer un produit
@product_router.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    with SessionLocal() as session:
        product = session.query(Product).filter(Product.ProductID == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        session.delete(product)
        session.commit()
    return product