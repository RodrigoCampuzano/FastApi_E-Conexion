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

@router.get("/mensajes/{mensaje_id}", response_model=List[MensajesResponse])
def read_mensajes_by_user(mensaje_id: int, db: Session = Depends(get_db)):
    # Buscar el mensaje específico por su ID
    mensaje = db.query(Mensajes).filter(Mensajes.id_mensajes == mensaje_id).first()
    
    if mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    # Obtener todos los mensajes que pertenecen al mismo usuario (id_mensajes_usuario)
    mensajes_relacionados = (
        db.query(Mensajes)
        .filter(Mensajes.id_mensajes_usuario == mensaje.id_mensajes_usuario)
        .all()
    )
    if not mensajes_relacionados:
        raise HTTPException(status_code=404, detail="No se encontraron mensajes relacionados")
    
    return mensajes_relacionados

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