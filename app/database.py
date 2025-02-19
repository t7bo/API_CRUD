from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connexion à la base de données avec Microsoft ODBC Driver 18
DATABASE_URL = "mssql+pyodbc://jvcb:cbjv592023!@adventureworks-server-hdf.database.windows.net/adventureworks?driver=ODBC+Driver+18+for+SQL+Server"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour créer la base de données
def create_db():
    from models import SQLModel
    SQLModel.metadata.create_all(bind=engine)
