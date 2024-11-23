from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.dependencies import get_db
from app.models.usuario_has_chat import ForoListaUsuario
from app.schemas.usuario_has_chat import UsuarioHasChatCreate, UsuarioHasChatResponse, UsuarioHasChatUpdate

router = APIRouter()

# Crear relación usuario-chat
@router.post("/", response_model=UsuarioHasChatResponse)
def create_forousuario(forousuario: UsuarioHasChatCreate, db: Session = Depends(get_db)):
    db_forousuario = ForoListaUsuario(
        usuario_idusuario=forousuario.usuario_idusuario,
        chat_idchat=forousuario.chat_idchat
    )
    db.add(db_forousuario)
    db.commit()
    db.refresh(db_forousuario)
    return UsuarioHasChatResponse.from_orm(db_forousuario)

# Obtener relación por IDs
@router.get("/{usuario_id}/{chat_id}", response_model=UsuarioHasChatResponse)
def read_forousuario(usuario_id: int, chat_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(ForoListaUsuario).filter(
        ForoListaUsuario.usuario_idusuario == usuario_id,
        ForoListaUsuario.chat_idchat == chat_id
    ).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Relación usuario-chat no encontrada")
    return UsuarioHasChatResponse.from_orm(forousuario)

# Eliminar relación por IDs
@router.delete("/{usuario_id}/{chat_id}", response_model=UsuarioHasChatResponse)
def delete_forousuario(usuario_id: int, chat_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(ForoListaUsuario).filter(
        ForoListaUsuario.usuario_idusuario == usuario_id,
        ForoListaUsuario.chat_idchat == chat_id
    ).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Relación usuario-chat no encontrada")
    db.delete(forousuario)
    db.commit()
    return UsuarioHasChatResponse.from_orm(forousuario)

# Actualizar relación usuario-chat
@router.put("/{usuario_id}/{chat_id}", response_model=UsuarioHasChatResponse)
def update_forousuario(usuario_id: int, chat_id: int, forousuario_update: UsuarioHasChatUpdate, db: Session = Depends(get_db)):
    forousuario = db.query(ForoListaUsuario).filter(
        ForoListaUsuario.usuario_idusuario == usuario_id,
        ForoListaUsuario.chat_idchat == chat_id
    ).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Relación usuario-chat no encontrada")
    forousuario.usuario_idusuario = forousuario_update.usuario_idusuario
    forousuario.chat_idchat = forousuario_update.chat_idchat
    db.commit()
    db.refresh(forousuario)
    return UsuarioHasChatResponse.from_orm(forousuario)

# Obtener todas las relaciones usuario-chat
@router.get("/", response_model=List[UsuarioHasChatResponse])
def read_all_forousuarios(db: Session = Depends(get_db)):
    foros = db.query(ForoListaUsuario).all()
    return [UsuarioHasChatResponse.from_orm(foro) for foro in foros]
