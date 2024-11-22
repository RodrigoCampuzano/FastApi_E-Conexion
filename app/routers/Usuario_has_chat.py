from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Usuario_has_chat import ForoListaUsuario
from app.schemas.usuario_has_chat import ForoUsuarioCreate, ForoUsuarioResponse, ForoUsuarioUpdate, ForoUsuarioResponseUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=ForoUsuarioResponse)
def create_forousuario(forolistausuario: ForoUsuarioCreate, db: Session = Depends(get_db)):
    db_forousuario = ForoListaUsuario(
        id_lista_foro=forolistausuario.id_lista_foro,
        id_usuario=forolistausuario.id_usuario,
        contenido=forolistausuario.contenido,
        fecha=forolistausuario.fecha
    )
    db.add(db_forousuario)
    db.commit()
    db.refresh(db_forousuario)
    return db_forousuario

@router.get("/{forousuario_id}", response_model=ForoUsuarioResponse)
def read_forousuarioid(forousuario_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(ForoListaUsuario).filter(ForoListaUsuario.id_lista_foro == forousuario_id).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail='Foro no encontrado')
    return forousuario

@router.delete("/{forousuario_id}", response_model=ForoUsuarioResponse)
def delete_forousuario(forousuario_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(ForoListaUsuario).filter(ForoListaUsuario.id_lista_foro == forousuario_id).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    db.delete(forousuario)
    db.commit()
    return forousuario

@router.put("/{forousuario_id}", response_model=ForoUsuarioResponseUpdate)
def update_forousuario(forousuario_id: int, forousuario_update: ForoUsuarioUpdate, db: Session = Depends(get_db)):
    forolistausuario = db.query(ForoListaUsuario).filter(ForoListaUsuario.id_lista_foro == forousuario_id).first()
    if forolistausuario is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    forolistausuario.contenido= forousuario_update.contenido
    db.refresh(forolistausuario)
    return forolistausuario



@router.get("/", response_model=List[ForoUsuarioResponse])
def read_all_chats(db: Session = Depends(get_db)):
    chats = db.query(ForoListaUsuario).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found")
    return chats