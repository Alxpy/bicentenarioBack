CREATE DATABASE IF NOT EXISTS bdLegado;
USE bdLegado;

CREATE TABLE IF NOT EXISTS usuario (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(250),
  apellidoPaterno VARCHAR(250),
  apellidoMaterno VARCHAR(250),
  correo VARCHAR(250) UNIQUE,
  contrasena VARCHAR(250),
  genero VARCHAR(50),
  telefono VARCHAR(50),
  pais VARCHAR(100),
  ciudad VARCHAR(100),
  estado TINYINT DEFAULT 1,
  email_verified_at DATETIME,
  ultimoIntentoFallido DATETIME,
  codeValidacion VARCHAR(250),
  cantIntentos INT,
  imagen VARCHAR(500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS categorianoticia (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre_categoria VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS rol (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  nombre_rol VARCHAR(100),
  descripcion TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS usuario_rol (
  id_usuario BIGINT,
  id_rol BIGINT,
  PRIMARY KEY(id_usuario, id_rol),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
  FOREIGN KEY (id_rol) REFERENCES rol(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS estadistica (
  id INT PRIMARY KEY AUTO_INCREMENT,
  tipo VARCHAR(255),
  detalle TEXT,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  id_usuario BIGINT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS noticia (
  id INT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(255),
  resumen TEXT,
  contenido TEXT,
  imagen VARCHAR(255),
  id_usuario BIGINT NULL,
  id_categoria INT,
  fecha_publicacion DATETIME,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE SET NULL,
  FOREIGN KEY (id_categoria) REFERENCES categorianoticia(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS categoria_historia (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(255),
  descripcion TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ubicacion (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(255),
  descripcion TEXT,
  latitud DECIMAL(9,6),
  longitud DECIMAL(9,6),
  imagen VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS cultura (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(255),
  descripcion TEXT,
  imagen VARCHAR(255),
  id_ubicacion INT,
  FOREIGN KEY (id_ubicacion) REFERENCES ubicacion(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tipo_evento (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre_evento VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS evento (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(255),
  descripcion TEXT,
  imagen VARCHAR(255),
  fecha_inicio DATETIME,
  fecha_fin DATETIME,
  id_tipo_evento INT,
  id_ubicacion INT,
  id_usuario BIGINT,
  FOREIGN KEY (id_tipo_evento) REFERENCES tipo_evento(id),
  FOREIGN KEY (id_ubicacion) REFERENCES ubicacion(id),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS usuario_evento (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_usuario BIGINT,
  id_evento INT,
  asistio BOOLEAN,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id),
  FOREIGN KEY (id_evento) REFERENCES evento(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS presidente (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(255),
  apellido VARCHAR(255),
  imagen VARCHAR(255),
  inicio_periodo DATE,
  fin_periodo DATE,
  bibliografia TEXT,
  partido_politico TEXT,
  principales_politicas TEXT,
  id_usuario BIGINT,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS historia (
  id INT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(255),
  descripcion TEXT,
  fecha_inicio DATE,
  fecha_fin DATE,
  imagen VARCHAR(255),
  id_ubicacion INT,
  id_categoria INT,
  FOREIGN KEY (id_ubicacion) REFERENCES ubicacion(id),
  FOREIGN KEY (id_categoria) REFERENCES categoria_historia(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tipo_documento (
  id INT PRIMARY KEY AUTO_INCREMENT,
  tipo VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS biblioteca (
  id INT PRIMARY KEY AUTO_INCREMENT,
  titulo VARCHAR(255),
  autor VARCHAR(255),
  imagen VARCHAR(255),
  fecha_publicacion DATE,
  edicion VARCHAR(255),
  id_usuario BIGINT,
  id_tipo INT,
  fuente VARCHAR(255),
  enlace TEXT,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id),
  FOREIGN KEY (id_tipo) REFERENCES tipo_documento(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS comentario (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_usuario BIGINT,
  contenido TEXT,
  fecha_creacion DATE,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS comentario_biblioteca (
  id_comentario INT,
  id_biblioteca INT,
  PRIMARY KEY (id_comentario, id_biblioteca),
  FOREIGN KEY (id_comentario) REFERENCES comentario(id),
  FOREIGN KEY (id_biblioteca) REFERENCES biblioteca(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS comentario_evento (
  id_comentario INT,
  id_evento INT,
  PRIMARY KEY (id_comentario, id_evento),
  FOREIGN KEY (id_comentario) REFERENCES comentario(id),
  FOREIGN KEY (id_evento) REFERENCES evento(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS multimedia (
  id INT PRIMARY KEY AUTO_INCREMENT,
  enlace VARCHAR(255),
  tipo VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS multimedia_historia (
  id_multimedia INT,
  id_historia INT,
  PRIMARY KEY (id_multimedia, id_historia),
  FOREIGN KEY (id_multimedia) REFERENCES multimedia(id),
  FOREIGN KEY (id_historia) REFERENCES historia(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS multimedia_cultura (
  id_multimedia INT,
  id_cultura INT,
  PRIMARY KEY (id_multimedia, id_cultura),
  FOREIGN KEY (id_multimedia) REFERENCES multimedia(id),
  FOREIGN KEY (id_cultura) REFERENCES cultura(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS auditoria (
  id INT PRIMARY KEY AUTO_INCREMENT,
  tipo VARCHAR(255),
  detalle VARCHAR(255),
  fecha_creacion DATETIME,
  id_usuario BIGINT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS agenda_personal (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_usuario BIGINT,
  id_evento INT,
  recordatorio DATETIME,
  notas TEXT,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id),
  FOREIGN KEY (id_evento) REFERENCES evento(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
