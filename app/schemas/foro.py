from pydantic import BaseModel

class ForoBase(BaseModel):
    id_chat: int
    nombre_foro: str
    descripcion: str
    id_usuario: int

class ForoResponse(ForoBase):
    id_foro: int
    
    class Config:
        from_attributes  =True
        
class ForoCreate(ForoBase):
    pass

class ForoUpdate(BaseModel):
    nombre_foro: str
    descripcion: str

class ForoResponseUpdate(ForoUpdate):
    id_foro: int
    
    class Config:
        from_attributes  =True

