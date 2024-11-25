import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Eventos(Base):
    __tablename__ = "eventos"
    __table_args__= {"schema": "e_conexion"}

    id_eventos = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_evento_usuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), nullable=True, index=True)
    id_organizador = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), nullable=True, index=True)
    id_donacion = Column(Integer, ForeignKey("e_conexion.donaciones.id_donaciones"), index=True, nullable=True)
    descripcion = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime, nullable=True)
    fecha_termino = Column(DateTime)
    estatus = Column(String(45), nullable=True)
    nombre = Column(String(100), nullable=True)
    ubicacion = Column(String(500), nullable=True)
    estatus_donacion = Column(String(100), nullable=True)
    estatus_donador = Column(String(100), nullable=True)
    
    usuario = relationship("Usuario", back_populates="eventos")
