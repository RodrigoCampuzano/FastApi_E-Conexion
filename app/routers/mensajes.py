from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Mensajes import Mensajes
from app.schemas.mensajes import MensajesCreate, MensajesResponse, MensajeUpdate, MensajesResponseUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=MensajesResponse)
def create_mensaje(mensaje: MensajesCreate, db: Session = Depends(get_db)):
    db_mensaje = Mensajes(
        id_usuario_mensaje=mensaje.id_usuario_mensaje,
        contenido=mensaje.contenido,
        fecha=mensaje.fecha
    )
    db.add(db_mensaje)
    db.commit()
    db.refresh(db_mensaje)
    return db_mensaje

@router.get("/{mensaje_id}", response_model=MensajesResponse)
def read_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    mensaje = db.query(Mensajes).filter(Mensajes.id_mensajes == mensaje_id).first()
    if mensaje is None:
        raise HTTPException(status_code=404, detail='Mensaje no encontrado')
    return mensaje

@router.delete("/{mensaje_id}", response_model=MensajesResponse)
def delete_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    mensaje = db.query(Mensajes).filter(Mensajes.id_mensajes == mensaje_id).first()
    if mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    db.delete(mensaje)
    db.commit()
    return mensaje

@router.put("/{mensaje_id}", response_model=MensajesResponseUpdate)
def update_mensaje(mensaje_id: int, mensaje_update: MensajeUpdate, db: Session = Depends(get_db)):
    mensaje = db.query(Mensajes).filter(Mensajes.id_mensajes == mensaje_id).first()
    if mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    mensaje.contenido = mensaje_update.contenido
    db.commit()
    db.refresh(mensaje)
    return mensaje



@router.get("/", response_model=List[MensajesResponse])
def read_all_chats(db: Session = Depends(get_db)):
    chats = db.query(Mensajes).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found")
    return chats