from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.chat import ChatResponse, ChatCreate, ChatUpdate, ChatResponseUpdate
from app.models.Chat import Chat 

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = Chat(
        id_mensaje=chat.id_mensaje,
        id_chat_Usuario=chat.id_chat_usuario,
        fecha=chat.fecha
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.get("/{chat_id}", response_model=ChatResponse)
def read_chatid(chat_id: int, db : Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id_chat == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail='foro no encontrado')
    return chat

@router.delete("/{chat_id}", response_model=ChatResponse)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(chat)
    db.commit()
    return chat

@router.put("/{chat_id}", response_model=ChatResponseUpdate)
def update_evento(chat_id: int, chat_update: ChatUpdate, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id_chat == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    chat.id_mensaje=chat_update.id_mensaje,
    chat.id_chat_usuario=chat_update.id_chat_usuario,
    chat.fecha=chat_update.fecha
    chat.id_chat_usuario=chat_update.id_chat_usuario
    db.refresh(chat)
    return chat
