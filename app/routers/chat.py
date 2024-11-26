from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db, get_current_user
from app.models.Usuarios import Usuario
from app.schemas.chat import ChatResponse, ChatCreate, ChatUpdate, ChatResponseUpdate
from app.models.Chat import Chat
from typing import List


router = APIRouter()

# Ruta para crear un chat
@router.post("/", response_model=ChatResponse)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = Chat(
        ultimo_msj=chat.ultimo_msj,
        grupal=chat.grupal
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)  
    return db_chat


# Ruta para leer un chat por su ID
@router.get("/{chat_id}", response_model=ChatResponse)
def read_chatid(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id_chat == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat no encontrado")
    return chat


# Ruta para eliminar un chat por su ID
@router.delete("/{chat_id}", response_model=ChatResponse)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id_chat == chat_id).first()  # Usar id_chat para la búsqueda
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat no encontrado")
    
    db.delete(chat)
    db.commit()
    return chat


# Ruta para actualizar un chat por su ID
@router.put("/{chat_id}", response_model=ChatResponseUpdate)
def update_chat(chat_id: int, chat_update: ChatUpdate, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id_chat == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat no encontrado")
    
    chat.ultimo_msj = chat_update.ultimo_msj  
    db.commit()  
    db.refresh(chat)  
    return chat


# Ruta para obtener todos los chats
@router.get("/", response_model=List[ChatResponse])
def read_all_chats(db: Session = Depends(get_db)):
    chats = db.query(Chat).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats encontrados")
    return chats
