from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.dependencies import get_db, get_current_user
from app.models.Usuarios import Usuario
from app.models.Eventos import Eventos
from app.schemas.eventos import EventoCreate, EventoResponse, EventoUpdate, EventoResponseUpdate
from typing import List
from sqlalchemy import text

router = APIRouter()

@router.post("/", response_model=EventoResponse)
def create_evento(evento: EventoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
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
def read_evento(evento_id: int, db: Session = Depends(get_db),current_user: Usuario = Depends(get_current_user)):
    evento = db.query(Eventos).filter(Eventos.id_eventos == evento_id).first()
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    db.execute(text("SELECT actualizar_estatus_eventos();"))
    db.commit()
    return evento

@router.get("/eventos/{evento_id}", response_model=List[EventoResponse])
def read_eventos_by_user(evento_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    evento = db.query(Eventos).filter(Eventos.id_evento_usuario == evento_id).first()

    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    eventos_relacionados = (
        db.query(Eventos)
        .filter(Eventos.id_evento_usuario == evento.id_evento_usuario)
        .all()
    )

    if not eventos_relacionados:
        raise HTTPException(status_code=404, detail="No se encontraron eventos relacionados")

    return eventos_relacionados

@router.delete("/{evento_id}", response_model=EventoResponse)
def delete_evento(evento_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    evento = db.query(Eventos).filter(Eventos.id_eventos == evento_id).first()
    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    db.execute(text("SELECT actualizar_estatus_eventos();"))
    db.delete(evento)
    db.commit()
    return evento

@router.put("/{evento_id}", response_model=EventoResponseUpdate)
def update_evento(evento_id: int, evento_update: EventoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    evento = db.query(Eventos).filter(Eventos.id_eventos == evento_id).first()

    if evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    print(f"Evento antes de actualización: {evento}")
    if evento_update.id_donacion is not None:
        evento.id_donacion = evento_update.id_donacion
    if evento_update.descripcion is not None:
        evento.descripcion = evento_update.descripcion
    if evento_update.fecha_creacion is not None:
        evento.fecha_creacion = evento_update.fecha_creacion
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
    print(f"Evento después de actualización: {evento}")
    
    
    db.commit()  
    db.refresh(evento)
    return evento


@router.get("/", response_model=List[EventoResponse])
def read_all_eventos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    eventos = db.query(Eventos).options(joinedload(Eventos.usuario),joinedload(Eventos.organizador)).all()

    if not eventos:
        raise HTTPException(status_code=404, detail="No events found")
    db.execute(text("SELECT actualizar_estatus_eventos();"))
    result = [
        {
            "id_eventos": evnt.id_eventos,
            "id_evento_usuario": evnt.id_evento_usuario,
            "id_organizador": evnt.id_organizador,
            "id_donacion": evnt.id_donacion,
            "descripcion": evnt.descripcion,
            "fecha_creacion": evnt.fecha_creacion,
            "fecha_termino": evnt.fecha_termino,
            "estatus": evnt.estatus,
            "nombre": evnt.nombre,
            "ubicacion": evnt.ubicacion,
            "estatus_donacion": evnt.estatus_donacion,
            "estatus_donador": evnt.estatus_donador,
            "nombre_organizador": evnt.organizador.nombre_usuario if evnt.organizador else None,
        }
        for evnt in eventos
    ]

    return result



