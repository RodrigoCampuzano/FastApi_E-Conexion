from pydantic import BaseModel
from datetime import datetime

class UsuarioHasChatBase(BaseModel):
    id_lista_foro: int
    id_usuario: int
    contenido: str
    fecha: datetime
    
class UsuarioHasChatResponse(UsuarioHasChatBase):
    id_lista_foro: int
    
    class Config:
        from_attributes  =True
        
class UsuarioHasChatCreate(UsuarioHasChatBase):
    pass

class UsuarioHasChatUpdate(BaseModel):
    contenido: str

class UsuarioHasChatResponseUpdate(UsuarioHasChatUpdate):
    id_lista_foro: int
    
    class Config:
        from_attributes  =True


