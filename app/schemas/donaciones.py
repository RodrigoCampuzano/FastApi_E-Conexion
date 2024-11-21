from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DonacionesBase(BaseModel):
    id_donacion_usuario: int
    cantidad: int
    fecha: datetime
    tipo_donacion: str
    estatus: str
    id_evento: Optional[str] = None
    
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
    id_evento: Optional[str] = None

class DonacionesResponseUpdate(DonacionesUpdate):
    id_donaciones: int
    
    class Config:
        from_attributes = True


