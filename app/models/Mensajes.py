from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.database import Base

class Mensajes(Base):
    __tablename__ = "mensajes"
    __table_args__= {"schema": "e_conexion"}

    id_mensaje = Column(Integer, primaty_key=True, nullable=True)
    id_chat = Column(Integer, ForeignKey("e_conexion.chat.id_chat"), nullable=True ) 
    fecha = Column(DateTime)
    estatus = Column(String(255), nullable=True)
    mensaje = Column(String(255), nullable=True)
    id_emisor = Column(Integer, nullable=True)