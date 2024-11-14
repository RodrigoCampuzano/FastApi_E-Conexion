from pydantic import BaseModel
from datetime import datetime

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
    imagen: str
    descripcion: str
    titulo: str
    
class PublicacionesCreate(PublicacionesBase):
    pass
    
class PublicacionesResponseUpdate(PublicacionesUpdate):
    id_publicaciones: int
    
    class Config:
        from_attributes = True