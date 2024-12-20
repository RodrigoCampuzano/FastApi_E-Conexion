from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.database import Base
from sqlalchemy.orm import relationship
  
class ListaContacto(Base):
    __tablename__ = "lista_contacto"
    __table_args__= {"schema": "e_conexion"}

    idlista = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, nullable=True)
    usuario_correo = Column(String(255), ForeignKey("e_conexion.usuarios.correo_usuario"), nullable=True)

    usuario = relationship("Usuario", back_populates="lista")
