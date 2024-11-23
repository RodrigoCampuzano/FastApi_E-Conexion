from pydantic import BaseModel
from datetime import datetime

class UsuarioHasChatBase(BaseModel):
    usuario_idusuario: int
    chat_idchat: int
    
class UsuarioHasChatResponse(UsuarioHasChatBase):
    usuario_idusuario: int
    
    class Config:
        from_attributes  =True
        
class UsuarioHasChatCreate(UsuarioHasChatBase):
    pass

class UsuarioHasChatUpdate(BaseModel):
    usuario_idusuario: int
    chat_idchat: int

class UsuarioHasChatResponseUpdate(UsuarioHasChatUpdate):
    usuario_idusuario: int
    
    class Config:
        from_attributes  =True


