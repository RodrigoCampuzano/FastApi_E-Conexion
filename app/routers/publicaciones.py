from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, FastAPI
from sqlalchemy.orm import Session, joinedload
from app.db.dependencies import get_db
from app.models.Publicaciones import Publicaciones
from app.schemas.publicaciones import PublicacionesCreate, PublicacionesResponse, PublicacionesUpdate, PublicacionesResponseUpdate, PublicacionesResponseconUsuario
from typing import List
import os
import shutil
from fastapi.staticfiles import StaticFiles

router = FastAPI()

UPLOAD_DIRECTORY = "uploads/publicaciones"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/", response_model=PublicacionesResponse)
def create_publicacion(
    id_publicaciones_usuario: int = Form(...),
    descripcion: str = Form(...),
    fecha: str = Form(...),
    titulo: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    if file:
        if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(status_code=400, detail="Unsupported file type. Only .png, .jpg, and .jpeg are allowed.")
        file_path = f"{UPLOAD_DIRECTORY}/{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_url = f"http://34.197.52.229:8000/uploads/publicaciones/{file.filename}"
    else:
        file_url = None 

    db_publicacion = Publicaciones(
        id_publicaciones_usuario=id_publicaciones_usuario,
        imagen=file_url,
        descripcion=descripcion,
        fecha=fecha,
        titulo=titulo,
    )
    db.add(db_publicacion)
    db.commit()
    db.refresh(db_publicacion)
    
    return db_publicacion


@router.get("/{publicacion_id}", response_model=List[PublicacionesResponse])
def read_publicaciones_by_user(publicacion_id: int, db: Session = Depends(get_db)):
    publicacion = db.query(Publicaciones).filter(Publicaciones.id_publicaciones_usuario == publicacion_id).first()
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    publicaciones_relacionadas = (
        db.query(Publicaciones).filter(Publicaciones.id_publicaciones_usuario == publicacion.id_publicaciones_usuario).all()
    )
    if not publicaciones_relacionadas:
        raise HTTPException(status_code=404, detail="No se encontraron publicaciones relacionadas")    
    return publicaciones_relacionadas


@router.delete("/{publicacion_id}", response_model=PublicacionesResponse)
def delete_publicacion(publicacion_id: int, db: Session = Depends(get_db)):
    publicacion = db.query(Publicaciones).filter(Publicaciones.id_publicaciones == publicacion_id).first()
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    
    db.delete(publicacion)
    db.commit()
    return publicacion

@router.put("/{publicacion_id}", response_model=PublicacionesResponseUpdate)
def update_publicacion(
    publicacion_id: int,
    publicacion_update: PublicacionesUpdate,
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    publicacion = db.query(Publicaciones).filter(Publicaciones.id_publicaciones == publicacion_id).first()
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    
    if file:
        if publicacion.imagen and os.path.exists(publicacion.imagen):
            os.remove(publicacion.imagen)
    
        new_file_path = f"{UPLOAD_DIRECTORY}/{file.filename}"
        with open(new_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        publicacion.imagen = f"http://34.197.52.229:8000/uploads/publicaciones/{file.filename}"
    
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

@router.get("/publicacionById/{publicacion_id}", response_model = PublicacionesResponse)
def     read_publicacion_by_id(publicacion_id: int, db: Session =  Depends(get_db)):
        publicacion = db.query(Publicaciones).filter(Publicaciones.id_publicaciones == publicacion_id).first()
        if publicacion is None:
                raise HTTPException(status_code = 404, detail= "Publicaion no encontrada")
        return publicacion