# Dans app/models.py
from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    ProductID: int = Field(default=None, primary_key=True)
    Name: str
    ProductNumber: str
    StandardCost: int
    ListPrice: int

class ProductCreate(SQLModel):
    Name: str
    ProductNumber: str
    StandardCost: int
    ListPrice: int
