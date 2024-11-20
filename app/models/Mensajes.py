import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Mensajes(Base):
    __tablename__ = "mensajes"
    __table_args__= {"schema": "e_conexion"}

    id_mensaje = Column(Integer, primary_key=True, index=True)
    id_usuario_mensaje = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), unique=True)
    contenido = Column(String, nullable=True)
    fecha = Column(DateTime)