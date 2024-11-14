import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class ForoListaUsuario(Base):
    __tablename__ = "foro_lista_usuario"
    __table_args__= {"schema": "e_conexion"}

    id_lista_foro = Column(Integer, ForeignKey("e_conexion.foro.id_foro"), primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), index=True)
    contenido = Column(String(500), nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
