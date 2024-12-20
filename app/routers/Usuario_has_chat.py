from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.dependencies import get_db
from app.db.auth import verify_token
from app.models.Usuario_has_chat import UsuarioHasChat
from app.schemas.usuario_has_chat import UsuarioHasChatCreate, UsuarioHasChatResponse, UsuarioHasChatUpdate

router = APIRouter()

# Crear relación usuario-chat
@router.post("/", response_model=UsuarioHasChatResponse )
def create_forousuario(forousuario: UsuarioHasChatCreate, db: Session = Depends(get_db)):
    db_forousuario = UsuarioHasChat(
        usuario_idusuario=forousuario.usuario_idusuario,
        chat_idchat=forousuario.chat_idchat
    )
    db.add(db_forousuario)
    db.commit()
    db.refresh(db_forousuario)
    return db_forousuario

# Obtener relación por IDs
@router.get("/by_usuario/{usuario_id}", response_model=List[UsuarioHasChatResponse])
def read_forousuario(usuario_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(UsuarioHasChat).filter(UsuarioHasChat.usuario_idusuario == usuario_id).all()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Relación usuario-chat no encontrada")
    return forousuario

@router.get("/by_chat/{chat_id}", response_model=List[UsuarioHasChatResponse] )
def read_forochat(chat_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(UsuarioHasChat).filter(UsuarioHasChat.chat_idchat == chat_id).all()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Relación usuario-chat no encontrada")
    return forousuario

# Eliminar relación por usuario_id
@router.delete("/{usuario_id}/{chat_id}", response_model=UsuarioHasChatResponse)
def delete_forousuario(usuario_id: int, chat_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(UsuarioHasChat).filter(
        UsuarioHasChat.usuario_idusuario == usuario_id,
        UsuarioHasChat.chat_idchat == chat_id
    ).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Relación usuario-chat no encontrada")
    db.delete(forousuario)
    db.commit()
    return forousuario

# Actualizar relación usuario-chat
@router.put("/{usuario_id}", response_model=UsuarioHasChatResponse )
def update_forousuario(usuario_id: int, forousuario_update: UsuarioHasChatUpdate, db: Session = Depends(get_db)):
    forousuario = db.query(UsuarioHasChat).filter(UsuarioHasChat.usuario_idusuario == usuario_id).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Relación usuario-chat no encontrada")
    forousuario.usuario_idusuario = forousuario_update.usuario_idusuario
    forousuario.chat_idchat = forousuario_update.chat_idchat
    db.commit()
    db.refresh(forousuario)
    return forousuario

# Obtener todas las relaciones por usuario_id
@router.get("/", response_model=List[UsuarioHasChatResponse])
def read_all_forousuarios(db: Session = Depends(get_db)):
    chats = db.query(UsuarioHasChat).all()
    return chats
