from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.database import Base

class Foro(Base):
    __tablename__ = "foro"
    __table_args__= {"schema": "e_conexion"}

    id_foro = Column(Integer, primary_key=True, index=True)
    id_chat = Column(Integer, ForeignKey("e_conexion.chat.id_chat"), primary_key=True)
    nombre_foro = Column(String(255), nullable=True)
    descripcion = Column(String(255), nullable=False)
    id_usuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), nullable=False)


