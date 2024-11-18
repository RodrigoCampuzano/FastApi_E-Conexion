from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Usuarios import Usuario
from app.models.Publicaciones import Publicaciones
from app.models.Lista_contacto import ListaContacto 
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate, UsuarioResponseUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=UsuarioResponse)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        apellidos_usuario=usuario.apellidos_usuario,
        correo_usuario=usuario.correo_usuario,
        contraseña_usuario=usuario.contraseña_usuario,
        telefono_usuario=usuario.telefono_usuario,
        tipo_usuario=usuario.tipo_usuario,
        imagen_usuario=usuario.imagen_usuario,
        estatus=usuario.estatus
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    publicaciones = db.query(Publicaciones).filter(Publicaciones.id_publicaciones_usuario == usuario_id).all()
    for pub in publicaciones:
        db.delete(pub)
    db.commit()
    
    lista = db.query(ListaContacto).filter(ListaContacto.id_usuario_lista == usuario_id).all()
    for lis in lista:
        db.delete(lis)
    db.commit(
        
    )    
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponseUpdate)
def update_usuario(usuario_id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.nombre_usuario = usuario_update.nombre_usuario
    usuario.apellidos_usuario = usuario_update.apellidos_usuario
    usuario.correo_usuario = usuario_update.correo_usuario
    usuario.contraseña_usuario = usuario_update.contraseña_usuario
    usuario.telefono_usuario = usuario_update.telefono_usuario
    usuario.tipo_usuario = usuario_update.tipo_usuario
    usuario.imagen_usuario = usuario_update.imagen_usuario
    usuario.estatus = usuario_update.estatus
    
    db.commit()
    db.refresh(usuario)
    return usuario



@router.get("/", response_model=List[UsuarioResponse])
def read_all_chats(db: Session = Depends(get_db)):
    chats = db.query(Usuario).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found")
    return chats