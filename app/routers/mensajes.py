from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Mensajes import Mensajes
from app.schemas.mensajes import MensajesCreate, MensajesResponse, MensajeUpdate, MensajesResponseUpdate
from typing import List

router = APIRouter()

# Ruta para crear un mensaje
@router.post("/", response_model=MensajesResponse)
def create_mensaje(mensaje: MensajesCreate, db: Session = Depends(get_db)):
    db_mensaje = Mensajes(
        id_chat=mensaje.id_chat,
        fecha=mensaje.fecha,
        estatus=mensaje.estatus,
        mensaje=mensaje.mensaje,
        id_emisor=mensaje.id_emisor
    )
    db.add(db_mensaje)
    db.commit()
    db.refresh(db_mensaje)
    return MensajesResponse.from_orm(db_mensaje)

# Ruta para obtener un mensaje por su ID
@router.get("/{mensaje_id}", response_model=MensajesResponse)
def read_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    mensaje = db.query(Mensajes).filter(Mensajes.id_mensaje == mensaje_id).first()
    if mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return mensaje

# Ruta para obtener mensajes por ID de usuario
@router.get("/mensajes/{mensaje_id}", response_model=List[MensajesResponse])
def read_mensajes_by_user(mensaje_id: int, db: Session = Depends(get_db)):
    mensajes_relacionados = (
        db.query(Mensajes)
        .filter(Mensajes.id_emisor == mensaje_id)
        .all()
    )
    if not mensajes_relacionados:
        raise HTTPException(status_code=404, detail="No se encontraron mensajes relacionados")
    
    return mensajes_relacionados

# Ruta para eliminar un mensaje por su ID
@router.delete("/{mensaje_id}", response_model=MensajesResponse)
def delete_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    mensaje = db.query(Mensajes).filter(Mensajes.id_mensaje == mensaje_id).first()
    if mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    db.delete(mensaje)
    db.commit()
    return mensaje

# Ruta para actualizar un mensaje por su ID
@router.put("/{mensaje_id}", response_model=MensajesResponseUpdate)
def update_mensaje(mensaje_id: int, mensaje_update: MensajeUpdate, db: Session = Depends(get_db)):
    mensaje = db.query(Mensajes).filter(Mensajes.id_mensaje == mensaje_id).first()
    if mensaje is None:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    mensaje.mensaje = mensaje_update.mensaje  
    db.commit()
    db.refresh(mensaje)
    return MensajesResponseUpdate.from_orm(mensaje)

# Ruta para obtener todos los mensajes
@router.get("/", response_model=List[MensajesResponse])
def read_all_mensajes(db: Session = Depends(get_db)):
    mensajes = db.query(Mensajes).all()
    if not mensajes:
        raise HTTPException(status_code=404, detail="No se encontraron mensajes")
    return mensajes
