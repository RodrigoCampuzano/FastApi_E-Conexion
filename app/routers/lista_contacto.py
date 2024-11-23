from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.dependencies import get_db
from app.models.Lista_contacto import ListaContacto
from app.models.Usuarios import Usuario
from app.schemas.lista_contacto import ListaContactoCreate, ListaContactoResponse, ListaContactoUpdate, ListaContactoResponseUpdate
from typing import List

router = APIRouter()

# Ruta para crear una nueva lista de contactos
@router.post("/", response_model=ListaContactoResponse)
def create_listacontacto(listacontacto: ListaContactoCreate, db: Session = Depends(get_db)):
    db_listacontacto = ListaContacto(
        id_usuario=listacontacto.id_usuario,
        usuario_correo=listacontacto.usuario_correo  
    )
    db.add(db_listacontacto)
    db.commit()
    db.refresh(db_listacontacto)  
    return db_listacontacto

# Ruta para obtener una lista de contactos por id del usuario
@router.get("/{id_usuario}", response_model=List[ListaContactoResponse])
def read_listacontacto(id_usuario: int, db: Session = Depends(get_db)):
    listacontacto = db.query(ListaContacto).filter(ListaContacto.id_usuario == id_usuario).all()
    if not listacontacto:
        raise HTTPException(status_code=404, detail="Lista de contactos no encontrada")
    result = []
    for lista in listacontacto:
        try:
            usuario = db.query(Usuario).filter(Usuario.correo_usuario == lista.usuario_correo).first()
            if usuario:  # Si encontramos el usuario
                result.append({
                    "idlista": lista.idlista,
                    "id_usuario": lista.id_usuario,
                    "usuario_correo": lista.usuario_correo,
                    "usuario_id": usuario.id_usuario,  # ID del usuario
                    "usuario_nombre": usuario.nombre_usuario  # Nombre del usuario
                })
            else:  # Si no encontramos un usuario para el correo
                result.append({
                    "idlista": lista.idlista,
                    "id_usuario": lista.id_usuario,
                    "usuario_correo": lista.usuario_correo,
                    "usuario_id": None,  # Si no se encuentra el usuario
                    "usuario_nombre": None  # Si no se encuentra el usuario
                })
        except Exception as e:
            print(f"Error al obtener usuario para correo {lista.usuario_correo}: {e}")
            raise HTTPException(status_code=500, detail="Error al procesar los datos del usuario")
    
    return result


# Ruta para eliminar una lista de contactos por su ID
@router.delete("/{lista_id}", response_model=ListaContactoResponse)
def delete_listacontacto(lista_id: int, db: Session = Depends(get_db)):
    listacontacto = db.query(ListaContacto).filter(ListaContacto.idlista == lista_id).first()
    if listacontacto is None:
        raise HTTPException(status_code=404, detail="Lista de contactos no encontrada")
    
    db.delete(listacontacto)
    db.commit()  
    return listacontacto


# Ruta para actualizar una lista de contactos por su ID
@router.put("/{lista_id}", response_model=ListaContactoResponseUpdate)
def update_lista(lista_id: int, lista_update: ListaContactoUpdate, db: Session = Depends(get_db)):
    listacontacto = db.query(ListaContacto).filter(ListaContacto.idlista == lista_id).first()
    if listacontacto is None:
        raise HTTPException(status_code=404, detail="Lista de contactos no encontrada")
    
    listacontacto.id_usuario = lista_update.id_usuario
    listacontacto.usuario_correo = lista_update.usuario_correo  
    db.commit()  
    db.refresh(listacontacto)  
    return listacontacto

# Ruta para obtener todas las listas de contactos
@router.get("/", response_model=List[ListaContactoResponse])
def read_all_listas(db: Session = Depends(get_db)):
    listas = db.query(ListaContacto).all()
    if not listas:
        raise HTTPException(status_code=404, detail="No se encontraron listas de contactos")
    return listas
