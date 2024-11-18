import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Donaciones(Base):
    __tablename__ = "donaciones"
    __table_args__= {"schema": "e_conexion"}

    id_donaciones = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_donacion_usuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), nullable=True, index=True)
    cantidad = Column(Integer, nullable=True)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    tipo_donacion = Column(String(255), nullable=True)
    estatus = Column(String(255), nullable=True)
    id_evento = Column(Integer, ForeignKey("e_conexion.eventos.id_eventos"), nullable=True)
