from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base
  
class ListaContacto(Base):
    __tablename__ = "lista_contacto"
    __table_args__= {"schema": "e_conexion"}

    idlista = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, nullable=True)
    usuario_idusuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), nullable=True)


