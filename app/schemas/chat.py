from pydantic import BaseModel

class ChatBase(BaseModel):
    ultimo_msj: str
    grupal: bool

class ChatResponse(ChatBase): 
    id_chat: int
    
    class Config:
        from_attributes  = True
    
class ChatCreate(ChatBase):
    pass

class ChatUpdate(BaseModel):
    ultimo_msj: str
    grupal: bool
    
class ChatResponseUpdate(ChatUpdate): 
    id_chat: int
    
    class Config:
        from_attributes  = True


