# Import des modules nécessaires
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel, Field
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import List


# Connexion à la base de données avec Microsoft ODBC Driver 18
DATABASE_URL = "mssql+pyodbc://jvcb:cbjv592023!@adventureworks-server-hdf.database.windows.net/adventureworks?driver=ODBC+Driver+18+for+SQL+Server"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création de l'application FastAPI
app = FastAPI()

# Dépendance pour récupérer la session SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèle de données pour le produit
class Product(SQLModel, table=True):
    ProductID: int = Field(default=None, primary_key=True)
    Name: str
    ProductNumber: str
    StandardCost: int
    ListPrice: int
    SellStartDate: datetime = Field(default_factory=datetime.utcnow)

# Modèle de données pour l'authentification
class User(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    Name: str
    Price: float
    ProductNumber: str  # Ajout de ProductNumber

class ProductUpdate(BaseModel):
    Name: str = None
    ProductNumber: str = None
    ListPrice: float = None  

# OAuth2 pour la gestion des tokens JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour créer la base de données
def create_db():
    SQLModel.metadata.create_all(bind=engine)

# Route pour récupérer tous les produits
@app.get("/products", response_model=List[Product])
def get_products():
    with SessionLocal() as session:
        products = session.query(Product).all()
    return products

# Route pour récupérer un produit par son ID
@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    with SessionLocal() as session:
        product = session.query(Product).filter(Product.ProductID == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    return product

# Route pour créer un nouveau produit
@app.post("/products", response_model=Product)
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
@app.put("/products/{product_id}", response_model=Product)
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
@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    with SessionLocal() as session:
        product = session.query(Product).filter(Product.ProductID == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        session.delete(product)
        session.commit()
    
    return product

# Fonction pour vérifier le token JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Route pour générer un token JWT (authentification)
@app.post("/token")
def login_for_access_token(form_data: User):
    access_token = jwt.encode(
        {"sub": form_data.username, "exp": datetime.utcnow() + timedelta(hours=1)},
        "secret", algorithm="HS256"
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Lancer la création de la base de données
create_db()