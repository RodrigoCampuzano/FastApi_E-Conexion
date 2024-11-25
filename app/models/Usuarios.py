from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "e_conexion"}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(255), nullable=True)
    apellidos_usuario = Column(String(255), nullable=True)
    correo_usuario = Column(String(255), nullable=False)
    contrasena_usuario = Column(String(255), nullable=True, unique=False)
    telefono_usuario = Column(String(25), nullable=True)
    tipo_usuario = Column(String(255), nullable=True)
    imagen_usuario = Column(String(255), nullable=False)
    estatus = Column(String(100), nullable=True)
    descripcion = Column(String(600), nullable=False)

    publicaciones = relationship("Publicaciones", back_populates="usuario")
    lista = relationship("ListaContacto", back_populates="usuario")
    eventos = relationship("Eventos", foreign_keys="[Eventos.id_evento_usuario]", back_populates="usuario")
    eventos_as_organizer = relationship("Eventos", foreign_keys="[Eventos.id_organizador]", back_populates="organizador")
