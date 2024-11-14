from pydantic import BaseModel
from datetime import datetime

class DonacionesBase(BaseModel):
    id_donacion_usuario: int
    cantidad: int
    fecha: datetime
    tipo_donacion: str
    estatus: str
    
class DonacionesResponse(DonacionesBase):
    id_donaciones: int
    
    class Config:
        from_attributes = True
        
class DonacionesCreate(DonacionesBase):
    pass

class DonacionesUpdate(BaseModel):
    cantidad: int
    tipo_donacion: str
    estatus: str

class DonacionesResponseUpdate(DonacionesUpdate):
    id_donaciones: int
    
    class Config:
        from_attributes = True


