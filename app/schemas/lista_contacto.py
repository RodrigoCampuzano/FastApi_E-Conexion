from pydantic import BaseModel

class ListaContactoBase(BaseModel):
    id_usuario: int
    id_usuario_lista: int
    
class ListaContactoResponse(ListaContactoBase):
    id_lista: int
    
    class Config:
        from_attributes  =True
        
class ListaContactoCreate(ListaContactoBase):
    pass

class ListaContactoUpdate(BaseModel):
    id_usuario: int
    id_usuario_lista: int

class ListaContactoResponseUpdate(ListaContactoUpdate):
    id_lista: int
    
    class Config:
        from_attributes  =True

