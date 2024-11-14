from pydantic import BaseModel
from datetime import datetime

class ForoUsuarioBase(BaseModel):
    id_lista_foro: int
    id_usuario: int
    contenido: str
    fecha: datetime
    
class ForoUsuarioResponse(ForoUsuarioBase):
    id_lista_foro: int
    
    class Config:
        from_attributes  =True
        
class ForoUsuarioCreate(ForoUsuarioBase):
    pass

class ForoUsuarioUpdate(BaseModel):
    contenido: str

class ForoUsuarioResponseUpdate(ForoUsuarioUpdate):
    id_lista_foro: int
    
    class Config:
        from_attributes  =True


