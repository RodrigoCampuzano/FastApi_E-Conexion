from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Chat(Base):
    __tablename__ = "chat"
    __table_args__= {"schema": "e_conexion"}

    id_chat = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ultimo_msj = Column(String(1000), nullable=False)


