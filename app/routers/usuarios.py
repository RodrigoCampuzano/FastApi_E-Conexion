import jwt
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Usuarios import Usuario
from app.models.Publicaciones import Publicaciones
from app.models.Lista_contacto import ListaContacto
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate, UsuarioResponseUpdate
from typing import List, Dict
import os
import shutil
from pydantic import EmailStr
from datetime import datetime, timedelta

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

UPLOAD_DIRECTORY = "uploads/publicaciones"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

SECRET_KEY = "ilGJrZmMbQDswbWtKknBzRzK639VhGCg"
ALGORITHM = "HS256"

def create_access_token(data: Dict[str, str], expires_delta: timedelta = timedelta(days=365)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UsuarioResponse)
def register_usuario(
    nombre_usuario: str = Form(...),
    apellidos_usuario: str = Form(...),
    correo_usuario: EmailStr = Form(...), 
    contraseña_usuario: str = Form(...),
    telefono_usuario: str = Form(...),
    tipo_usuario: str = Form(...),
    estatus: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    existing_user = db.query(Usuario).filter(Usuario.correo_usuario == correo_usuario).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    hashed_password = pwd_context.hash(contraseña_usuario)

    if file:
        if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
            raise HTTPException(status_code=400, detail="Unsupported file type. Only .png, .jpg, and .jpeg are allowed.")
        file_path = f"{UPLOAD_DIRECTORY}/{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_url = f"http://34.197.52.229:8000/uploads/publicaciones/{file.filename}"
    else:
        file_url = None  

    new_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        apellidos_usuario=apellidos_usuario,
        correo_usuario=correo_usuario,
        contraseña_usuario=hashed_password,
        telefono_usuario=telefono_usuario,
        tipo_usuario=tipo_usuario,
        imagen_usuario=file_path,  
        estatus=estatus,
    )

    db.add(new_usuario)
    db.commit()
    db.refresh(new_usuario)
    return new_usuario

@router.post("/login", response_model=Dict[str, str])
def login_usuario(
    correo_usuario: str = Form(...),
    contraseña_usuario: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.correo_usuario == correo_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")
    if not pwd_context.verify(contraseña_usuario, usuario.contraseña_usuario):
        raise HTTPException(status_code=401, detail="Credenciales inválidas.")
    
    access_token = create_access_token(data={"sub": str(usuario.id_usuario)})

    return {
        "mensaje": "Inicio de sesión exitoso",
        "id_usuario": str(usuario.id_usuario),
        "access_token": access_token
    }

@router.post("/", response_model=UsuarioResponse)
def create_usuario(
    nombre_usuario: str = Form(...),
    apellidos_usuario: str = Form(...),
    correo_usuario: EmailStr = Form(...),  
    contraseña_usuario: str = Form(...),
    telefono_usuario: str = Form(...),
    tipo_usuario: str = Form(...),
    estatus: str = Form(...),
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
    db_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        apellidos_usuario=apellidos_usuario,
        correo_usuario=correo_usuario,
        contraseña_usuario=contraseña_usuario,
        telefono_usuario=telefono_usuario,
        tipo_usuario=tipo_usuario,
        imagen_usuario=file_path,
        estatus=estatus
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
    db.commit()    
    
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponseUpdate)
async def update_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario_update.contraseña_usuario:
        usuario_update.contraseña_usuario = pwd_context.hash(usuario_update.contraseña_usuario)

    if file:
        if usuario.imagen_usuario and os.path.exists(usuario.imagen_usuario):
            os.remove(usuario.imagen_usuario)
        new_file_path = f"{UPLOAD_DIRECTORY}/{file.filename}"
        with open(new_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        usuario.imagen_usuario = new_file_path

    usuario.nombre_usuario = usuario_update.nombre_usuario
    usuario.apellidos_usuario = usuario_update.apellidos_usuario
    usuario.correo_usuario = usuario_update.correo_usuario
    usuario.contraseña_usuario = usuario_update.contraseña_usuario
    usuario.telefono_usuario = usuario_update.telefono_usuario
    usuario.tipo_usuario = usuario_update.tipo_usuario
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
