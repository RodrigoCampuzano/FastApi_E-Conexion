from sqlalchemy import Column, Integer, ForeignKey

from app.db.database import Base

class UsuarioHasChat(Base):
    __tablename__ = "usuario_has_chat"
    __table_args__= {"schema": "e_conexion"}

    usuario_idusuario = Column(Integer, ForeignKey("e_conexion.usuarios.id_usuario"), primary_key=True, index=True)
    chat_idchat = Column(Integer, ForeignKey("e_conexion.chat.id_chat"), primary_key=True, index=True)