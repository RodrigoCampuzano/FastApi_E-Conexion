from pydantic import BaseModel
from datetime import datetime

class ChatBase(BaseModel):
    id_mensaje: int
    id_chat_usuario: int
    fecha: datetime

class ChatResponse(ChatBase): 
    id_chat: int
    
    class Config:
        from_attributes  = True
    
class ChatCreate(ChatBase):
    pass

class ChatUpdate(BaseModel):
    id_mensaje: int
    id_chat_usuario: int
    fecha: datetime
    
class ChatResponseUpdate(ChatUpdate): 
    id_chat: int
    
    class Config:
        from_attributes  = True


