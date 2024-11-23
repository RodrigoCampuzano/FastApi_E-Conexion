from pydantic import BaseModel

class ListaContactoBase(BaseModel):
    id_usuario: int
    usuario_correo: str
    
class ListaContactoResponse(ListaContactoBase):
    idlista: int
    
    class Config:
        from_attributes  =True
        
class ListaContactoCreate(ListaContactoBase):
    pass

class ListaContactoUpdate(BaseModel):
    id_usuario: int
    usuario_correo: str

class ListaContactoResponseUpdate(ListaContactoUpdate):
    idlista: int
    
    class Config:
        from_attributes  =True

