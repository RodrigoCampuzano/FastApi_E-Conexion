from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Usuario_has_chat import ForoListaUsuario
from app.schemas.usuario_has_chat import UsuarioHasChatCreate, UsuarioHasChatResponse, UsuarioHasChatUpdate, UsuarioHasChatResponseUpdate
from typing import List

router = APIRouter()

# Ruta para crear un nuevo foro (relación usuario-chat)
@router.post("/", response_model=UsuarioHasChatResponse)
def create_forousuario(forousuario: UsuarioHasChatCreate, db: Session = Depends(get_db)):
    db_forousuario = ForoListaUsuario(
        usuario_idusuario=forousuario.id_usuario,
        chat_idchat=forousuario.id_lista_foro,  
        contenido=forousuario.contenido,
        fecha=forousuario.fecha
    )
    db.add(db_forousuario)
    db.commit()
    db.refresh(db_forousuario)
    return UsuarioHasChatResponse.from_orm(db_forousuario)

# Ruta para obtener un foro por ID
@router.get("/{forousuario_id}", response_model=UsuarioHasChatResponse)
def read_forousuarioid(forousuario_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(ForoListaUsuario).filter(ForoListaUsuario.id_lista_foro == forousuario_id).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    return UsuarioHasChatResponse.from_orm(forousuario)

# Ruta para eliminar un foro por ID
@router.delete("/{forousuario_id}", response_model=UsuarioHasChatResponse)
def delete_forousuario(forousuario_id: int, db: Session = Depends(get_db)):
    forousuario = db.query(ForoListaUsuario).filter(ForoListaUsuario.id_lista_foro == forousuario_id).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    db.delete(forousuario)
    db.commit()
    return UsuarioHasChatResponse.from_orm(forousuario)

# Ruta para actualizar el contenido de un foro
@router.put("/{forousuario_id}", response_model=UsuarioHasChatResponseUpdate)
def update_forousuario(forousuario_id: int, forousuario_update: UsuarioHasChatUpdate, db: Session = Depends(get_db)):
    forousuario = db.query(ForoListaUsuario).filter(ForoListaUsuario.id_lista_foro == forousuario_id).first()
    if forousuario is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    forousuario.contenido = forousuario_update.contenido
    db.commit()
    db.refresh(forousuario)
    return UsuarioHasChatResponseUpdate.from_orm(forousuario)

# Ruta para obtener todos los foros de usuarios
@router.get("/", response_model=List[UsuarioHasChatResponse])
def read_all_foros(db: Session = Depends(get_db)):
    foros = db.query(ForoListaUsuario).all()
    if not foros:
        raise HTTPException(status_code=404, detail="No se encontraron foros")
    return [UsuarioHasChatResponse.from_orm(foro) for foro in foros]
