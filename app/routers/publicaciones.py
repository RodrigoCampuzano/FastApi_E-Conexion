from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.dependencies import get_db
from app.models.Publicaciones import Publicaciones
from app.models.Usuarios import Usuario
from app.schemas.publicaciones import PublicacionesCreate, PublicacionesResponse, PublicacionesUpdate, PublicacionesResponseUpdate, PublicacionesResponseconUsuario
from typing import List

router = APIRouter()

@router.post("/", response_model=PublicacionesResponse)
def create_publicacion(publicacion: PublicacionesCreate, db: Session = Depends(get_db)):
    db_publicacion = Publicaciones(
        id_publicaciones_usuario=publicacion.id_publicaciones_usuario,
        imagen=publicacion.imagen,
        descripcion=publicacion.descripcion,
        fecha=publicacion.fecha,
        titulo=publicacion.titulo
    )
    db.add(db_publicacion)
    db.commit()
    db.refresh(db_publicacion)
    return db_publicacion

@router.get("/{publicacion_id}", response_model=PublicacionesResponse)
def read_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    publicacion = db.query(Publicaciones).filter(Publicaciones.id_publicaciones == publicacion_id).first()
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return publicacion

@router.delete("/{publicacion_id}", response_model=PublicacionesResponse)
def delete_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    publicacion = db.query(Publicaciones).filter(Publicaciones.id_publicaciones == publicacion_id).first()
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    
    db.delete(publicacion)
    db.commit()
    return publicacion

@router.put("/{publicacion_id}", response_model=PublicacionesResponseUpdate)
def update_publicacion(publicacion_id: int, publicacion_update: PublicacionesUpdate, db: Session = Depends(get_db)):
    publicacion = db.query(Publicaciones).filter(Publicaciones.id_publicaciones == publicacion_id).first()
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    
    publicacion.imagen = publicacion_update.imagen
    publicacion.descripcion = publicacion_update.descripcion
    publicacion.titulo = publicacion_update.titulo
    db.commit()
    db.refresh(publicacion)
    return publicacion

@router.get("/", response_model=List[PublicacionesResponseconUsuario])
def read_all_chats(db: Session = Depends(get_db)):
    publicaciones = (
        db.query(Publicaciones)
        .options(joinedload(Publicaciones.usuario)) 
        .all()
    )
    result = [
        {
            "id_publicaciones": pub.id_publicaciones,
            "id_publicaciones_usuario": pub.id_publicaciones_usuario,
            "imagen": pub.imagen,
            "descripcion": pub.descripcion,
            "fecha": pub.fecha,
            "titulo": pub.titulo,
            "nombre_usuario": pub.usuario.nombre_usuario
        }
        for pub in publicaciones
    ]

    if not publicaciones:
        raise HTTPException(status_code=404, detail="No publicaciones encontradas")
    return result
