from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventoBase(BaseModel):
    id_evento_usuario: int  
    id_organizador: int  
    id_donacion: Optional[int] = None  
    descripcion: str
    fecha_creacion: datetime
    fecha_termino: datetime
    estatus: str
    nombre: str
    ubicacion: str
    estatus_donacion: str
    estatus_donador: Optional[str] = None
    
class EventoResponse(EventoBase):
    id_eventos: int
    
    class Config:
        from_attributes = True

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    id_donacion: Optional[int] = None
    descripcion: str
    fecha_creacion: datetime
    fecha_termino: datetime
    estatus: str
    nombre: str
    ubicacion: str
    estatus_donacion: str
    estatus_donador: str

class EventoResponseUpdate(EventoUpdate):
    id_eventos: int
    
    class Config:
        from_attributes = True
        
# crear lista eventos y llamar id_lista_evento
