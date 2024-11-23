from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre_usuario: str
    apellidos_usuario: str
    correo_usuario: Optional[str] = None
    contrasena_usuario: Optional[str] = None
    telefono_usuario: str
    tipo_usuario: str
    imagen_usuario: Optional[str] = None
    estatus: str

class UsuarioResponse(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre_usuario: str
    apellidos_usuario: str
    contrasena_usuario: Optional[str] = None
    telefono_usuario: str
    tipo_usuario: str
    imagen_usuario: Optional[str] = None
    estatus: str

class UsuarioResponseUpdate(UsuarioUpdate):
    id_usuario: int

    class Config:
        from_attributes = True
