from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos desde el archivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarar la base
Base = declarative_base()

# Verificar la conexión
try:
    # Intentar conectar a la base de datos
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)
