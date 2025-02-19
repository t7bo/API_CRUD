from fastapi import FastAPI
from routes import router
from database import create_db

# Création de l'application FastAPI
app = FastAPI()

# Lancer la création de la base de données
create_db()

# Inclure les routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)