from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product, ProductCreate, ProductUpdate
from database import SessionLocal
from datetime import datetime, timedelta
from typing import List
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# Dépendance pour récupérer la session SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour récupérer tous les produits
@router.get("/products", response_model=List[Product])
def get_products():
    with SessionLocal() as session:
        products = session.query(Product).all()
    return products

# Route pour récupérer un produit par son ID
@router.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    with SessionLocal() as session:
        product = session.query(Product).filter(Product.ProductID == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

# Route pour créer un nouveau produit
@router.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    new_product = Product(
        Name=product.Name, 
        ProductNumber=product.ProductNumber,  
        StandardCost=0, 
        ListPrice=product.Price,
        SellStartDate=datetime.utcnow()
    )
    
    with SessionLocal() as session:
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
    
    return new_product

# Route pour mettre à jour un produit
@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, session: Session = Depends(get_db)):
    existing_product = session.query(Product).filter(Product.ProductID == product_id).first()
    
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Mise à jour dynamique uniquement des champs non nuls
    for key, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, key, value)
    
    session.commit()
    session.refresh(existing_product)

    return existing_product

# Route pour supprimer un produit
@router.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    with SessionLocal() as session:
        product = session.query(Product).filter(Product.ProductID == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        session.delete(product)
        session.commit()
    
    return product


# OAuth2 pour la gestion des tokens JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour créer un token d'accès JWT
@router.post("/token")
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
    return f"Token : {encoded_jwt}"

# Fonction pour vérifier le token JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
