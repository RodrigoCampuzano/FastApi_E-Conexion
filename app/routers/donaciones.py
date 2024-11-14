from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Donaciones import Donaciones 
from app.schemas.donaciones import DonacionesCreate, DonacionesResponse, DonacionesUpdate, DonacionesResponseUpdate

router = APIRouter()

@router.post("/", response_model=DonacionesResponse)
def create_donaciones(donaciones: DonacionesCreate, db: Session = Depends(get_db)):
    db_donaciones = Donaciones(
        id_donacion_usuario=donaciones.id_donacion_usuario,
        cantidad=donaciones.cantidad,
        fecha=donaciones.fecha,
        tipo_donacion=donaciones.tipo_donacion,
        estatus=donaciones.estatus
    )
    db.add(db_donaciones)
    db.commit()
    db.refresh(db_donaciones)
    return db_donaciones

@router.get("/{donaciones_id}", response_model=DonacionesResponse)
def read_donacionesid(donaciones_id: int, db : Session = Depends(get_db)):
    donaciones = db.query(Donaciones).filter(Donaciones.id_donaciones == donaciones_id).first()
    if donaciones is None:
        raise HTTPException(status_code=404, detail='foro no encontrado')
    return donaciones

@router.delete("/{donaciones_id}", response_model=DonacionesResponse)
def delete_donaciones(donaciones_id: int, db: Session = Depends(get_db)):
    donaciones = db.query(Donaciones).filter(Donaciones.id_donaciones == donaciones_id).first()
    if donaciones is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(donaciones)
    db.commit()
    return donaciones

@router.put("/{donaciones_id}", response_model=DonacionesResponseUpdate)
def update_donaciones(donaciones_id: int, donaciones_update: DonacionesUpdate, db: Session = Depends(get_db)):
    donaciones = db.query(Donaciones).filter(Donaciones.id_donaciones == donaciones_id).first()
    if donaciones is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    donaciones.cantidad=donaciones_update.cantidad
    donaciones.tipo_donacion=donaciones_update.tipo_donacion
    donaciones.estatus=donaciones_update.estatus
    db.refresh(donaciones)
    return donaciones