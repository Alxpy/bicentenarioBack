CREATE TABLE usuariotest (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(250) NOT NULL,
  apellidoPaterno VARCHAR(250) NOT NULL,
  apellidoMaterno VARCHAR(250) NOT NULL,
  correo VARCHAR(250) UNIQUE NOT NULL,
  contrasena VARCHAR(250) NOT NULL,
  genero VARCHAR(250) NOT NULL,
  telefono VARCHAR(250) NOT NULL,
  pais VARCHAR(250) NOT NULL,
  ciudad VARCHAR(250) NOT NULL,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  id_rol BIGINT,
  email_verified_at DATETIME DEFAULT NULL,
  ultimoIntentoFallido DATETIME DEFAULT NULL,
  codeValidacion VARCHAR(250) DEFAULT NULL,
  cantIntentos INT DEFAULT 0,
  FOREIGN KEY (id_rol) REFERENCES rol(id) ON DELETE SET NULL
);

CREATE TABLE rol (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre_rol VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250)
);

CREATE TABLE usuario_rol (
  id_usuario BIGINT,
  id_rol BIGINT,
  PRIMARY KEY (id_usuario, id_rol),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
  FOREIGN KEY (id_rol) REFERENCES rol(id) ON DELETE CASCADE
);

CREATE TABLE articulo (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(250) NOT NULL,
  contenido VARCHAR(250) NOT NULL,
  imagen VARCHAR(250),
  fecha_publicacion DATETIME DEFAULT CURRENT_DATETIME,
  id_autor BIGINT,
  FOREIGN KEY (id_autor) REFERENCES usuario(id) ON DELETE SET NULL
);

CREATE TABLE multimedia (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  tipo VARCHAR(250) NOT NULL,
  url VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250),
  id_articulo BIGINT,
  FOREIGN KEY (id_articulo) REFERENCES articulo(id) ON DELETE CASCADE
);

CREATE TABLE documento (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250),
  fecha_publicacion DATETIME DEFAULT CURRENT_DATETIME,
  archivo_url VARCHAR(250) NOT NULL,
  id_autor BIGINT,
  FOREIGN KEY (id_autor) REFERENCES usuario(id) ON DELETE SET NULL
);

CREATE TABLE categoria_documento (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250)
);

CREATE TABLE documento_categoria (
  id_documento BIGINT,
  id_categoria BIGINT,
  PRIMARY KEY (id_documento, id_categoria),
  FOREIGN KEY (id_documento) REFERENCES documento(id) ON DELETE CASCADE,
  FOREIGN KEY (id_categoria) REFERENCES categoria_documento(id) ON DELETE CASCADE
);

CREATE TABLE evento (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250),
  fecha_inicio DATETIME NOT NULL,
  fecha_fin DATETIME NOT NULL,
  ubicacion VARCHAR(250) NOT NULL,
  id_organizador BIGINT,
  FOREIGN KEY (id_organizador) REFERENCES usuario(id) ON DELETE SET NULL
);

CREATE TABLE participante_evento (
  id_usuario BIGINT,
  id_evento BIGINT,
  estado_asistencia VARCHAR(250) NOT NULL,
  PRIMARY KEY (id_usuario, id_evento),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
  FOREIGN KEY (id_evento) REFERENCES evento(id) ON DELETE CASCADE
);

CREATE TABLE encuesta (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  pregunta VARCHAR(250) NOT NULL,
  id_creador BIGINT,
  fecha_creacion DATETIME DEFAULT CURRENT_DATETIME,
  FOREIGN KEY (id_creador) REFERENCES usuario(id) ON DELETE SET NULL
);

CREATE TABLE respuesta_encuesta (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  id_encuesta BIGINT,
  respuesta VARCHAR(250) NOT NULL,
  votos INT DEFAULT 0,
  FOREIGN KEY (id_encuesta) REFERENCES encuesta(id) ON DELETE CASCADE
);

CREATE TABLE ruta_turistica (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250),
  id_creador BIGINT,
  FOREIGN KEY (id_creador) REFERENCES usuario(id) ON DELETE SET NULL
);

CREATE TABLE punto_interes (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250),
  coordenadas VARCHAR(250) NOT NULL,
  id_ruta BIGINT,
  FOREIGN KEY (id_ruta) REFERENCES ruta_turistica(id) ON DELETE CASCADE
);

CREATE TABLE producto (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250),
  precio DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL,
  id_vendedor BIGINT,
  FOREIGN KEY (id_vendedor) REFERENCES usuario(id) ON DELETE SET NULL
);

CREATE TABLE categoria_producto (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(250) NOT NULL,
  descripcion VARCHAR(250)
);

CREATE TABLE producto_categoria (
  id_producto BIGINT,
  id_categoria BIGINT,
  PRIMARY KEY (id_producto, id_categoria),
  FOREIGN KEY (id_producto) REFERENCES producto(id) ON DELETE CASCADE,
  FOREIGN KEY (id_categoria) REFERENCES categoria_producto(id) ON DELETE CASCADE
);

CREATE TABLE pedido (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  id_usuario BIGINT,
  fecha_pedido DATETIME DEFAULT CURRENT_DATETIME,
  estado VARCHAR(250) NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE SET NULL
);

CREATE TABLE detalle_pedido (
  id_pedido BIGINT,
  id_producto BIGINT,
  cantidad INT NOT NULL,
  precio_unitario DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_pedido, id_producto),
  FOREIGN KEY (id_pedido) REFERENCES pedido(id) ON DELETE CASCADE,
  FOREIGN KEY (id_producto) REFERENCES producto(id) ON DELETE CASCADE
);

CREATE TABLE reporte (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  descripcion VARCHAR(250) NOT NULL,
  tipo_reporte VARCHAR(250) NOT NULL,
  id_usuario BIGINT,
  estado VARCHAR(250) NOT NULL,
  fecha_reporte DATETIME DEFAULT CURRENT_DATETIME,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE SET NULL
);
