from fastapi import FastAPI
from app.routers import donaciones, foro_lista_usuario, foro, lista_contacto, mensajes, publicaciones, eventos, usuarios, chat

app = FastAPI()

app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(eventos.router, prefix="/eventos", tags=["eventos"])
app.include_router(publicaciones.router, prefix="/publicaciones", tags=["publicaciones"])
app.include_router(mensajes.router, prefix="/mensajes", tags=["mensajes"])
app.include_router(lista_contacto.router, prefix="/lista_contacto", tags=["lista_contacto"])
app.include_router(foro.router, prefix="/foro", tags=["foro"])
app.include_router(foro_lista_usuario.router, prefix="/foro_usuario", tags=["foro_usuario"])
app.include_router(donaciones.router, prefix="/donaciones", tags=["donaciones"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])