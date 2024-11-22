from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import Usuario_has_chat, donaciones, foro, lista_contacto, mensajes, publicaciones, eventos, usuarios, chat
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(eventos.router, prefix="/eventos", tags=["eventos"])
app.include_router(publicaciones.router, prefix="/publicaciones", tags=["publicaciones"])
app.include_router(mensajes.router, prefix="/mensajes", tags=["mensajes"])
app.include_router(lista_contacto.router, prefix="/lista_contacto", tags=["lista_contacto"])
app.include_router(foro.router, prefix="/foro", tags=["foro"])
app.include_router(Usuario_has_chat.router, prefix="/usuario_has_chat", tags=["usuario_has_chat"])
app.include_router(donaciones.router, prefix="/donaciones", tags=["donaciones"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
