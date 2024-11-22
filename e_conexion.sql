-- Crear el esquema si no existe
CREATE SCHEMA IF NOT EXISTS e_conexion;

-- Tabla: chat
CREATE TABLE IF NOT EXISTS e_conexion.chat (
    id_chat SERIAL PRIMARY KEY,
    ultimo_msj TEXT NOT NULL
);

-- Tabla: donaciones
CREATE TABLE IF NOT EXISTS e_conexion.donaciones (
    id_donaciones SERIAL PRIMARY KEY,
    id_donacion_usuario INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    tipo_donacion VARCHAR(255) NOT NULL,
    estatus VARCHAR(255) NOT NULL,
    id_evento INTEGER,
    CONSTRAINT fk_donacion_evento FOREIGN KEY (id_evento)
        REFERENCES e_conexion.eventos (id_eventos) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Tabla: eventos
CREATE TABLE IF NOT EXISTS e_conexion.eventos (
    id_eventos SERIAL PRIMARY KEY,
    id_evento_usuario INTEGER NOT NULL,
    id_organizador INTEGER NOT NULL,
    id_donacion INTEGER,
    descripcion VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    fecha_termino TIMESTAMP WITHOUT TIME ZONE,
    estatus VARCHAR(45) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(500) NOT NULL,
    estatus_donacion VARCHAR(100) NOT NULL,
    estatus_donador VARCHAR(100),
    CONSTRAINT fk_donacion_evento FOREIGN KEY (id_donacion)
        REFERENCES e_conexion.donaciones (id_donaciones) ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT fk_evento_organizador FOREIGN KEY (id_organizador)
        REFERENCES e_conexion.usuarios (id_usuario) ON UPDATE NO ACTION ON DELETE CASCADE,
    CONSTRAINT fk_evento_usuario FOREIGN KEY (id_evento_usuario)
        REFERENCES e_conexion.usuarios (id_usuario) ON UPDATE NO ACTION ON DELETE CASCADE
);

-- Tabla: foro
CREATE TABLE IF NOT EXISTS e_conexion.foro (
    id_foro SERIAL PRIMARY KEY,
    id_chat INTEGER NOT NULL,
    nombre_foro VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    CONSTRAINT fk_chat_foro FOREIGN KEY (id_chat)
        REFERENCES e_conexion.chat (id_chat) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Tabla: usuario_has_chat
CREATE TABLE IF NOT EXISTS e_conexion.usuario_has_chat (
    usuario_idusuario INTEGER NOT NULL,
    chat_idchat INTEGER NOT NULL,
    CONSTRAINT fk_Usuario_has_Chat_Usuario FOREIGN KEY (usuario_idusuario)
        REFERENCES e_conexion.usuarios (id_usuario) ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT fk_Usuario_has_Chat_Chat1 FOREIGN KEY (chat_idchat)
        REFERENCES e_conexion.chat (id_chat) ON UPDATE NO ACTION ON DELETE NO ACTION,
    PRIMARY KEY (usuario_idusuario, chat_idchat)
);

-- Tabla: lista_contacto
CREATE TABLE IF NOT EXISTS e_conexion.lista_contacto (
    idlista SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    usuario_idusuario INTEGER NOT NULL,
    CONSTRAINT fk_Lista_Contacto_Usuario FOREIGN KEY (usuario_idusuario)
        REFERENCES e_conexion.usuarios (id_usuario) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Tabla: mensajes
CREATE TABLE IF NOT EXISTS e_conexion.mensajes (
    id_mensaje SERIAL PRIMARY KEY,
    id_chat INTEGER NOT NULL,
    fecha TIMESTAMP WITH TIME ZONE NOT NULL,
    estatus TEXT NOT NULL,
    mensaje TEXT NOT NULL,
    id_emisor INTEGER NOT NULL,
    CONSTRAINT fk_Mensaje_Chat FOREIGN KEY (id_chat)
        REFERENCES e_conexion.chat (id_chat) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Tabla: publicaciones
CREATE TABLE IF NOT EXISTS e_conexion.publicaciones (
    id_publicaciones SERIAL PRIMARY KEY,
    id_publicaciones_usuario INTEGER NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    fecha TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    CONSTRAINT fk_publicacio_usuario FOREIGN KEY (id_publicaciones_usuario)
        REFERENCES e_conexion.usuarios (id_usuario) ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Tabla: usuarios
CREATE TABLE IF NOT EXISTS e_conexion.usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL,
    apellidos_usuario VARCHAR(255) NOT NULL,
    correo_usuario VARCHAR(255) UNIQUE NOT NULL,
    contraseña_usuario VARCHAR(255) NOT NULL,
    telefono_usuario VARCHAR(25) NOT NULL,
    tipo_usuario VARCHAR(255) NOT NULL,
    imagen_usuario VARCHAR(255) NOT NULL,
    estatus VARCHAR(100) NOT NULL
);
