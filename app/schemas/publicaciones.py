from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PublicacionesBase(BaseModel):
    id_publicaciones_usuario: int
    imagen: str
    descripcion: str
    fecha: datetime
    titulo: str

class PublicacionesResponse(PublicacionesBase):
    id_publicaciones: int
    
    class Config:
        from_attributes = True
    
class PublicacionesUpdate(BaseModel):
    imagen: Optional[str] = None
    descripcion: Optional[str]= None
    titulo: Optional[str] = None
    
class PublicacionesCreate(PublicacionesBase):
    pass
    
class PublicacionesResponseUpdate(PublicacionesUpdate):
    id_publicaciones: int
    
    class Config:
        from_attributes = True
        
class PublicacionesResponseconUsuario(PublicacionesBase):
    id_publicaciones: int
    nombre_usuario: str
    
    class Config:
        from_attributes = True