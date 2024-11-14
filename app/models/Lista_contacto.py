import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
  
class ListaContacto(Base):
    __tablename__ = "lista_contacto"
    __table_args__= {"schema": "e_conexion"}

    id_lista = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), nullable=True)
    id_usuario_lista = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), nullable=True)


