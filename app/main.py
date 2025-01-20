from fastapi import FastAPI
from app.models import Product
from app.routes import product_router
from app.database import create_db

app = FastAPI()

# Inclus les routes
app.include_router(product_router)

# Crée la base de données
create_db()