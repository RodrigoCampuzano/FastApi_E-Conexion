import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Foro(Base):
    __tablename__ = "foro"
    __table_args__= {"schema": "e_conexion"}

    id_foro = Column(Integer, primary_key=True, index=True)
    id_lista_foro = Column(Integer, ForeignKey("e_conexion.foro_lista_usuario.id_lista_foro"), primary_key=True)
    nombre_foro = Column(String(255), nullable=True)
    descripcion = Column(String(255), nullable=False)


