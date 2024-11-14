import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Chat(Base):
    __tablename__ = "chat"
    __table_args__= {"schema": "e_conexion"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_chat = Column(Integer, nullable=True)
    id_mensaje = Column(Integer, ForeignKey("e_conexion.mensajes.id_mensaje"), nullable=True)
    id_chat_usuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), nullable=True, index=True)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)


