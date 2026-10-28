DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS locales;    
DROP TABLE IF EXISTS salas;
DROP TABLE IF EXISTS butacas;
DROP TABLE IF EXISTS peliculas;
DROP TABLE IF EXISTS funciones;    
DROP TABLE IF EXISTS compras;
DROP TABLE IF EXISTS entradas;
DROP TABLE IF EXISTS servicios;
DROP TABLE IF EXISTS compra_servicios;    

-- ---------------------------------------------
-- 1. SEGURIDAD Y USUARIOS
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS roles (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL,
    apellido       VARCHAR(100) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    telefono       VARCHAR(30),
    rol_id         INT NOT NULL,
    activo         BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- ---------------------------------------------
-- 2. LOCALES, SALAS Y BUTACAS
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS locales (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    nombre    VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    ciudad    VARCHAR(100),
    telefono  VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS salas (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    local_id  INT NOT NULL,
    nombre    VARCHAR(50) NOT NULL,
    capacidad INT NOT NULL,
    tipo      VARCHAR(50),
    FOREIGN KEY (local_id) REFERENCES locales(id)
);

CREATE TABLE IF NOT EXISTS butacas (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    sala_id INT NOT NULL,
    fila    VARCHAR(5) NOT NULL,
    numero  INT NOT NULL,
    tipo    VARCHAR(30) DEFAULT 'estandar',
    FOREIGN KEY (sala_id) REFERENCES salas(id),
    UNIQUE (sala_id, fila, numero)
);

-- ---------------------------------------------
-- 3. PELÍCULAS
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS peliculas (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    api_id        VARCHAR(50),
    titulo        VARCHAR(200) NOT NULL,
    sinopsis      TEXT,
    poster_url    VARCHAR(500),
    duracion_min  INT,
    clasificacion VARCHAR(20),
    genero        VARCHAR(100),
    anio_estreno  INT
);

-- ---------------------------------------------
-- 4. FUNCIONES
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS funciones (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    pelicula_id    INT NOT NULL,
    sala_id        INT NOT NULL,
    fecha          DATE NOT NULL,
    hora_inicio    TIME NOT NULL,
    hora_fin       TIME,
    precio_base    DECIMAL(10,2) NOT NULL,
    estado         ENUM('programada','en_curso','finalizada','cancelada') DEFAULT 'programada',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id),
    FOREIGN KEY (sala_id)     REFERENCES salas(id),
    UNIQUE (sala_id, fecha, hora_inicio)
);

-- ---------------------------------------------
-- 5. COMPRAS (factura y cancelación integradas)
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS compras (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id          INT NOT NULL,
    funcion_id          INT NOT NULL,
    codigo              VARCHAR(50) NOT NULL UNIQUE,
    total               DECIMAL(10,2) NOT NULL DEFAULT 0,
    estado              ENUM('pendiente','pagada','cancelada','usada') DEFAULT 'pendiente',
    fecha_compra        DATETIME DEFAULT CURRENT_TIMESTAMP,
    email_enviado       BOOLEAN DEFAULT FALSE,
    fecha_cancelacion   DATETIME,
    motivo_cancelacion  VARCHAR(255),
    monto_reembolso     DECIMAL(10,2) DEFAULT 0,
    numero_factura      VARCHAR(50) UNIQUE,
    url_factura_pdf     VARCHAR(500),
    factura_enviada     BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (funcion_id) REFERENCES funciones(id)
);

-- ---------------------------------------------
-- 6. ENTRADAS
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS entradas (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    compra_id         INT NOT NULL,
    funcion_id        INT NOT NULL,
    butaca_id         INT NOT NULL,
    precio            DECIMAL(10,2) NOT NULL,
    qr_codigo         VARCHAR(100) NOT NULL UNIQUE,
    estado            ENUM('valida','usada','cancelada') DEFAULT 'valida',
    fecha_uso         DATETIME,
    fecha_cancelacion DATETIME,
    FOREIGN KEY (compra_id)  REFERENCES compras(id),
    FOREIGN KEY (funcion_id) REFERENCES funciones(id),
    FOREIGN KEY (butaca_id)  REFERENCES butacas(id),
    UNIQUE (funcion_id, butaca_id)
);

-- ---------------------------------------------
-- 7. SERVICIOS
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS servicios (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria   VARCHAR(50),
    precio      DECIMAL(10,2) NOT NULL,
    stock       INT,
    activo      BOOLEAN DEFAULT TRUE,
    imagen_url  VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS compra_servicios (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    compra_id       INT NOT NULL,
    servicio_id     INT NOT NULL,
    cantidad        INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal        DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (compra_id)   REFERENCES compras(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);
