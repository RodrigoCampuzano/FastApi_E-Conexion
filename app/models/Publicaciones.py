
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Publicaciones(Base):
    __tablename__ = "publicaciones"
    __table_args__= {"schema": "e_conexion"}

    id_publicaciones = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_publicaciones_usuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario", ondelete="CASCADE"), nullable=True)
    imagen = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=False)
    fecha = Column(DateTime)
    titulo = Column(String(255), nullable=False)
    
    usuario = relationship("Usuario", back_populates="publicaciones")