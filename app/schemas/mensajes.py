from pydantic import BaseModel
from datetime import datetime

class MensajesBase(BaseModel):
    id_usuario_mensaje: int
    contenido: str
    fecha: datetime
    
class MensajesResponse(MensajesBase):
    id_mensaje: int
    
    class Config:
        from_attributes  =True 
            
class MensajesCreate(MensajesBase):
    pass

class MensajeUpdate(BaseModel):
    contenido: str

class MensajesResponseUpdate(MensajeUpdate):
    id_mensaje: int
    
    class Config:
        from_attributes  =True 

