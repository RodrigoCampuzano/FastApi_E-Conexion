from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db, get_current_user
from app.models.Usuarios import Usuario
from app.models.Foro import Foro
from app.schemas.foro import ForoCreate, ForoResponse, ForoUpdate, ForoResponseUpdate
from typing import List

router = APIRouter()

# Ruta para crear un foro
@router.post("/", response_model=ForoResponse)
def create_foro(foro: ForoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_foro = Foro(
        id_chat=foro.id_chat,  
        nombre_foro=foro.nombre_foro,
        descripcion=foro.descripcion,
        id_usuario=foro.id_usuario
    )
    db.add(db_foro)
    db.commit()
    db.refresh(db_foro)  
    return db_foro

# Ruta para leer un foro por su ID
@router.get("chat/{chat_id}", response_model=ForoResponse)
def read_foro_chatid(chat_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    foro = db.query(Foro).filter(Foro.id_chat == chat_id).first()
    if foro is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    return foro

# Ruta para eliminar un foro por su ID
@router.delete("/{foro_id}", response_model=ForoResponse)
def delete_foro(foro_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if foro is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    db.delete(foro)
    db.commit()
    return foro

# Ruta para actualizar un foro por su ID
@router.put("/{foro_id}", response_model=ForoResponseUpdate)
def update_foro(foro_id: int, foro_update: ForoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if foro is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    foro.nombre_foro = foro_update.nombre_foro
    foro.descripcion = foro_update.descripcion
    db.commit()  
    db.refresh(foro)  
    return foro

# Ruta para obtener todos los foros
@router.get("/", response_model=List[ForoResponse])
def read_all_foros(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    foros = db.query(Foro).all()
    if not foros:
        raise HTTPException(status_code=404, detail="No foros encontrados")
    return foros


@router.get("foro/{foro_id}", response_model=ForoResponse)
def read_foroid(foro_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    forochat = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if forochat is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    return forochat
