from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Foro import Foro
from app.schemas.foro import ForoCreate, ForoResponse, ForoUpdate, ForoResponseUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=ForoResponse)
def create_foro(foro: ForoCreate, db: Session = Depends(get_db)):
    db_foro = Foro(
        id_lista_foro=foro.id_lista_foro,
        nombre_foro=foro.nombre_foro,
        descripcion=foro.descripcion
    )
    db.add(db_foro)
    db.commit()
    db.refresh(db_foro)
    return db_foro

@router.get("/{foro_id}", response_model=ForoResponse)
def read_foroid(foro_id: int, db: Session = Depends(get_db)):
    foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if foro is None:
        raise HTTPException(status_code=404, detail='Foro no encontrado')
    return foro

@router.delete("/{foro_id}", response_model=ForoResponse)
def delete_foro(foro_id: int, db: Session = Depends(get_db)):
    foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if foro is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    db.delete(foro)
    db.commit()
    return foro

@router.put("/{foro_id}", response_model=ForoResponseUpdate)
def update_foro(foro_id: int, foro_update: ForoUpdate, db: Session = Depends(get_db)):
    foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if foro is None:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    foro.nombre_foro = foro_update.nombre_foro
    foro.descripcion = foro_update.descripcion
    db.refresh(foro)
    return foro



@router.get("/", response_model=List[ForoResponse])
def read_all_chats(db: Session = Depends(get_db)):
    chats = db.query(Foro).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found")
    return chats