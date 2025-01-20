# Import des modules nécessaires
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel, Field
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import datetime
from typing import List

# Connexion à la base de données avec Microsoft ODBC Driver 18
# Base de données SQL Server Azure (AdventureWorks)
DATABASE_URL = "mssql+pyodbc://jvcb:cbjv592023!@adventureworks-server-hdf.database.windows.net/adventureworks?driver=ODBC+Driver+18+for+SQL+Server"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création de l'application FastAPI
app = FastAPI()

# Modèle de données pour le produit
class Product(SQLModel, table=True):
    ProductID: int = Field(default=None, primary_key=True)
    Name: str
    ProductNumber: str
    StandardCost: int
    ListPrice: int

# Modèle de données pour l'authentification
class User(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    Name: str
    Price: float

# OAuth2 pour la gestion des tokens JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour créer la base de données
def create_db():
    SQLModel.metadata.create_all(bind=engine)

# Route pour récupérer tous les produits
@app.get("/products", response_model=List[Product])
def get_products():
    with SessionLocal() as session:
        products = session.query(Product).all()  # Récupère tous les produits
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
    new_product = Product(Name=product.Name, Price=product.Price)  # Crée un nouveau produit
    with SessionLocal() as session:
        session.add(new_product)
        session.commit()  # Sauvegarde dans la base de données
        session.refresh(new_product)  # Rafraîchit l'instance pour avoir les données actuelles
    return new_product


# Route pour mettre à jour un produit existant
@app.put("/products/{product_id}", response_model=Product)
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
        payload = jwt.decode(token, "secret", algorithms=["HS256"])  # Vérifie le token
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Route pour générer un token JWT (authentification)
@app.post("/token")
def login_for_access_token(form_data: User):
    # Ici on simule la création du token JWT
    access_token = jwt.encode(
        {"sub": form_data.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        "secret", algorithm="HS256"
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Lancer la création de la base de données
create_db()

# Le code ci-dessus met en place toutes les routes nécessaires à l'API.
# Vous pouvez maintenant tester l'API avec FastAPI en utilisant Swagger UI.
