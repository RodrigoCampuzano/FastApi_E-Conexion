from pydantic import BaseModel
from datetime import datetime

class MensajesBase(BaseModel):
    id_chat: int 
    fecha: datetime
    estatus: str 
    mensaje: str 
    id_emisor: int 
    
class MensajesResponse(MensajesBase):
    id_mensaje: int
    
    class Config:
        from_attributes  =True 
            
class MensajesCreate(MensajesBase):
    pass

class MensajeUpdate(BaseModel):
    mensaje: str

class MensajesResponseUpdate(MensajeUpdate):
    id_mensaje: int
    
    class Config:
        from_attributes  =True 

