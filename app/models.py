from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel

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