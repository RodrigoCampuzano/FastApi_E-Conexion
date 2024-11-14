
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__= {"schema": "e_conexion"}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(255), nullable=True)
    apellidos_usuario = Column(String(255), nullable=True)
    correo_usuario = Column(String(255), nullable=True)
    contraseña_usuario = Column(String(255), nullable=True, unique=True)
    telefono_usuario = Column(String(25), nullable=True)
    tipo_usuario = Column(String(255), nullable=True)
    imagen_usuario = Column(String(255), nullable=True)
    estatus = Column(String(100), nullable=True)
