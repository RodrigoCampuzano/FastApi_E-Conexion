from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Eventos import Eventos
from app.schemas.eventos import EventoCreate, EventoResponse, EventoUpdate, EventoResponseUpdate

router = APIRouter()

@router.post("/", response_model=EventoResponse)
def create_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    db_evento = Eventos(
        id_evento_usuario=evento.id_evento_usuario,
        id_organizador=evento.id_organizador,
        id_donacion=evento.id_donacion,
        descripcion=evento.descripcion,
        fecha_creacion=evento.fecha_creacion,
        fecha_termino=evento.fecha_termino,
        estatus=evento.estatus,
        nombre=evento.nombre,
        ubicacion=evento.ubicacion,
        estatus_donacion=evento.estatus_donacion,
        estatus_donador=evento.estatus_donador
    )
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

@router.get("/{evento_id}", response_model=EventoResponse)
def read_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Eventos).filter(Eventos.id_eventos == evento_id).first()
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

@router.delete("/{evento_id}", response_model=EventoResponse)
def delete_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Eventos).filter(Eventos.id_eventos == evento_id).first()
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    db.delete(evento)
    db.commit()
    return evento

@router.put("/{evento_id}", response_model=EventoResponseUpdate)
def update_evento(evento_id: int, evento_update: EventoUpdate, db: Session = Depends(get_db)):
    evento = db.query(Eventos).filter(Eventos.id_eventos == evento_id).first()
    
    # Si el evento no existe, lanzamos un error
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    # Para depuración, muestra los valores actuales antes de actualizar
    print(f"Evento antes de actualización: {evento}")
    
    # Solo actualizamos los campos que son distintos de None
    if evento_update.id_donacion is not None:
        evento.id_donacion = evento_update.id_donacion
    if evento_update.descripcion is not None:
        evento.descripcion = evento_update.descripcion
    if evento_update.fecha_termino is not None:
        evento.fecha_termino = evento_update.fecha_termino
    if evento_update.estatus is not None:
        evento.estatus = evento_update.estatus
    if evento_update.nombre is not None:
        evento.nombre = evento_update.nombre
    if evento_update.ubicacion is not None:
        evento.ubicacion = evento_update.ubicacion
    if evento_update.estatus_donacion is not None:
        evento.estatus_donacion = evento_update.estatus_donacion
    if evento_update.estatus_donador is not None:
        evento.estatus_donador = evento_update.estatus_donador
    
    # Para depuración, muestra los valores después de actualización
    print(f"Evento después de actualización: {evento}")
    
    db.commit()  # Asegúrate de hacer commit después de la actualización
    db.refresh(evento)  # Refrescar el objeto con los nuevos datos
    return evento
