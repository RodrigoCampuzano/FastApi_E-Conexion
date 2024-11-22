from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Lista_contacto import ListaContacto
from app.schemas.lista_contacto import ListaContactoCreate, ListaContactoResponse, ListaContactoUpdate, ListaContactoResponseUpdate
from typing import List

router = APIRouter()

# Ruta para crear una nueva lista de contactos
@router.post("/", response_model=ListaContactoResponse)
def create_listacontacto(listacontacto: ListaContactoCreate, db: Session = Depends(get_db)):
    db_listacontacto = ListaContacto(
        id_usuario=listacontacto.id_usuario,
        usuario_idusuario=listacontacto.usuario_idusuario  
    )
    db.add(db_listacontacto)
    db.commit()
    db.refresh(db_listacontacto)  
    return db_listacontacto

# Ruta para obtener una lista de contactos por su ID
@router.get("/{lista_id}", response_model=ListaContactoResponse)
def read_listacontacto(lista_id: int, db: Session = Depends(get_db)):
    listacontacto = db.query(ListaContacto).filter(ListaContacto.idlista == lista_id).first()
    if listacontacto is None:
        raise HTTPException(status_code=404, detail="Lista de contactos no encontrada")
    return listacontacto

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
    listacontacto.usuario_idusuario = lista_update.usuario_idusuario  
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
