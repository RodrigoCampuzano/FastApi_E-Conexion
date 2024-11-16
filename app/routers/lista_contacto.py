from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.Lista_contacto import ListaContacto
from app.schemas.lista_contacto import ListaContactoCreate, ListaContactoResponse, ListaContactoUpdate, ListaContactoResponseUpdate
from typing import List

router = APIRouter()

@router.post("/", response_model=ListaContactoResponse)
def create_listacontacto(listacontacto: ListaContactoCreate, db: Session = Depends(get_db)):
    db_listacontacto = ListaContacto(
        id_usuario=listacontacto.id_usuario,
        id_usuario_lista=listacontacto.id_usuario_lista
    )
    db.add(db_listacontacto)
    db.commit()
    db.refresh(db_listacontacto)
    return db_listacontacto

@router.get("/{lista_id}", response_model=ListaContactoResponse)
def read_listacontacto(lista_id: int, db: Session = Depends(get_db)):
    listacontacto = db.query(ListaContacto).filter(ListaContacto.idlista == lista_id).first()
    if listacontacto is None:
        raise HTTPException(status_code=404, detail='Lista no encontrada')
    return listacontacto

@router.delete("/{lista_id}", response_model=ListaContactoResponse)
def delete_listacontacto(lista_id: int, db: Session = Depends(get_db)):
    listacontacto = db.query(ListaContacto).filter(ListaContacto.idlista == lista_id).first()
    if listacontacto is None:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    db.delete(listacontacto)
    db.commit()
    return listacontacto

@router.put("/{lista_id}", response_model=ListaContactoResponseUpdate)
def update_lista(lista_id: int, lista_update: ListaContactoUpdate, db: Session = Depends(get_db)):
    listacontacto = db.query(ListaContacto).filter(ListaContacto.idlista == lista_id).first()
    if listacontacto is None:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    listacontacto.id_usuario = lista_update.id_usuario
    listacontacto.id_usuario_lista = lista_update.id_usuario_lista
    db.refresh(listacontacto)
    return listacontacto



@router.get("/", response_model=List[ListaContactoResponse])
def read_all_chats(db: Session = Depends(get_db)):
    chats = db.query(ListaContacto).all()
    if not chats:
        raise HTTPException(status_code=404, detail="No chats found")
    return chats