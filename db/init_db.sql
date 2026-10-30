DROP TABLE IF EXISTS compra_servicios;
DROP TABLE IF EXISTS entradas;
DROP TABLE IF EXISTS compras;
DROP TABLE IF EXISTS servicios;
DROP TABLE IF EXISTS funciones;
DROP TABLE IF EXISTS peliculas;
DROP TABLE IF EXISTS butacas;
DROP TABLE IF EXISTS salas;
DROP TABLE IF EXISTS locales;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS roles;

-- ---------------------------------------------
-- 1. SEGURIDAD Y USUARIOS
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS roles (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL,
    apellido       VARCHAR(100) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    telefono       VARCHAR(30),
    rol_id         INT NOT NULL,
    activo         BOOLEAN NOT NULL DEFAULT TRUE,
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
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin    DATETIME NOT NULL,
    precio_base    FLOAT NOT NULL,
    estado         ENUM('programada','en_curso','finalizada','cancelada') DEFAULT 'programada',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id),
    FOREIGN KEY (sala_id)     REFERENCES salas(id),
    UNIQUE (sala_id, fecha_hora_inicio),
    CONSTRAINT chk_funcion_horario CHECK (fecha_hora_fin > fecha_hora_inicio)
);

-- ---------------------------------------------
-- 5. COMPRAS (factura y cancelación integradas)
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS compras (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id          INT NOT NULL,
    funcion_id          INT NOT NULL,
    codigo              VARCHAR(50) NOT NULL UNIQUE,
    total               FLOAT NOT NULL DEFAULT 0,
    estado              ENUM('pendiente','pagada','cancelada','usada') DEFAULT 'pendiente',
    fecha_compra        DATETIME DEFAULT CURRENT_TIMESTAMP,
    email_enviado       BOOLEAN DEFAULT FALSE,
    fecha_cancelacion   DATETIME,
    motivo_cancelacion  VARCHAR(255),
    numero_factura      VARCHAR(50) UNIQUE,
    url_factura_pdf     VARCHAR(500),
    factura_enviada     BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (funcion_id) REFERENCES funciones(id),
    UNIQUE (id, funcion_id)
);

-- ---------------------------------------------
-- 6. ENTRADAS
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS entradas (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    compra_id         INT NOT NULL,
    funcion_id        INT NOT NULL,
    butaca_id         INT NOT NULL,
    precio            FLOAT NOT NULL,
    qr_codigo         VARCHAR(100) UNIQUE,
    estado            ENUM('pendiente','valida','usada','cancelada') NOT NULL DEFAULT 'pendiente',
    -- MySQL permite multiples NULL en UNIQUE. Una entrada cancelada deja de bloquear su butaca.
    butaca_ocupada_id INT GENERATED ALWAYS AS (
        CASE WHEN estado = 'cancelada' THEN NULL ELSE butaca_id END
    ) STORED,
    fecha_uso         DATETIME,
    fecha_cancelacion DATETIME,
    -- Esta FK compuesta exige que la funcion de la entrada sea la misma que la compra.
    FOREIGN KEY (compra_id, funcion_id) REFERENCES compras(id, funcion_id),
    FOREIGN KEY (funcion_id) REFERENCES funciones(id),
    FOREIGN KEY (butaca_id)  REFERENCES butacas(id),
    UNIQUE (funcion_id, butaca_ocupada_id)
);

-- ---------------------------------------------
-- 7. SERVICIOS
-- Se mantiene el borrado fisico; si hay compra_servicios asociados, la FK impide eliminar.
-- ---------------------------------------------
CREATE TABLE IF NOT EXISTS servicios (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria   VARCHAR(50),
    precio      FLOAT NOT NULL,
    stock       INT,
    imagen_url  VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS compra_servicios (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    compra_id       INT NOT NULL,
    servicio_id     INT NOT NULL,
    cantidad        INT NOT NULL DEFAULT 1,
    precio_unitario FLOAT NOT NULL,
    subtotal        FLOAT NOT NULL,
    FOREIGN KEY (compra_id)   REFERENCES compras(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);


-- ---------------------------------------------
-- 8. DATOS DE PRUEBA (INSERT INTO)
-- ---------------------------------------------
-- Para pruebas locales exclusivamente; NO son cuentas reales ni datos de producción.
-- Contraseña de los cuatro usuarios de prueba: Demo1234!
-- Los hashes son PBKDF2 SHA-256 compatibles con werkzeug.security.check_password_hash().
-- Si el Backend usa otro mecanismo de contraseñas, adaptar estos hashes.
-- Los importes usan FLOAT, de acuerdo con la modificación solicitada.

-- ROLES: 2 registros
INSERT INTO roles (nombre) VALUES
    ('administrador'),
    ('cliente');

-- USUARIOS: 4 registros
INSERT INTO usuarios (nombre, apellido, email, password_hash, telefono, rol_id, fecha_registro) VALUES
    ('Admin', 'Demo', 'admin.demo@example.com', 'pbkdf2:sha256:600000$b2d73c3902681173$f7b8d8b40213bd93b9b18c68e6776b348f0ce5641accd5c9873c572e351dd9f8', '1111-1000', 1, '2026-10-20 10:00:00'),
    ('Ana', 'Prueba', 'ana.prueba@example.com', 'pbkdf2:sha256:600000$42c968950e71908e$c980f9d267e4623bfccd0a021ed713c6c0f8f563632d492c35e9d7a6ebd5e161', '1111-2000', 2, '2026-10-20 10:00:00'),
    ('Bruno', 'Prueba', 'bruno.prueba@example.com', 'pbkdf2:sha256:600000$9d159d1bead84571$3be8af095b8250ae5b1cd49a87d4b457f0c35854c993dbf178a49416dce619b3', '1111-3000', 2, '2026-10-20 10:00:00'),
    ('Carla', 'Prueba', 'carla.prueba@example.com', 'pbkdf2:sha256:600000$2e6cccb8fc6df658$167a1108a0b670795bc873cd543820a4a46040f91d7883901da82cca18a22f43', '1111-4000', 2, '2026-10-20 10:00:00');

-- LOCALES: 3 registros, como indica el contexto del enunciado
INSERT INTO locales (nombre, direccion, ciudad, telefono) VALUES
    ('Cine Paradiso Centro', 'Av. Corrientes 1200', 'CABA', '011-4000-1000'),
    ('Cine Paradiso Norte', 'Av. Cabildo 2200', 'CABA', '011-4000-2000'),
    ('Cine Paradiso Oeste', 'Av. Rivadavia 6400', 'CABA', '011-4000-3000');

-- SALAS: 4 registros (12 butacas cada una); una sala para el tercer local
INSERT INTO salas (local_id, nombre, capacidad, tipo) VALUES
    (1, 'Sala 1', 12, '2D'),
    (1, 'Sala 2', 12, '3D'),
    (2, 'Sala 1', 12, '2D'),
    (3, 'Sala 1', 12, '2D');

-- BUTACAS: 48 registros, 12 en cada sala
INSERT INTO butacas (sala_id, fila, numero, tipo) VALUES
    (1, 'A', 1, 'estandar'),
    (1, 'A', 2, 'estandar'),
    (1, 'A', 3, 'estandar'),
    (1, 'A', 4, 'estandar'),
    (1, 'B', 1, 'estandar'),
    (1, 'B', 2, 'estandar'),
    (1, 'B', 3, 'estandar'),
    (1, 'B', 4, 'estandar'),
    (1, 'C', 1, 'estandar'),
    (1, 'C', 2, 'estandar'),
    (1, 'C', 3, 'estandar'),
    (1, 'C', 4, 'estandar'),
    (2, 'A', 1, 'estandar'),
    (2, 'A', 2, 'estandar'),
    (2, 'A', 3, 'estandar'),
    (2, 'A', 4, 'estandar'),
    (2, 'B', 1, 'estandar'),
    (2, 'B', 2, 'estandar'),
    (2, 'B', 3, 'estandar'),
    (2, 'B', 4, 'estandar'),
    (2, 'C', 1, 'estandar'),
    (2, 'C', 2, 'estandar'),
    (2, 'C', 3, 'estandar'),
    (2, 'C', 4, 'estandar'),
    (3, 'A', 1, 'estandar'),
    (3, 'A', 2, 'estandar'),
    (3, 'A', 3, 'estandar'),
    (3, 'A', 4, 'estandar'),
    (3, 'B', 1, 'estandar'),
    (3, 'B', 2, 'estandar'),
    (3, 'B', 3, 'estandar'),
    (3, 'B', 4, 'estandar'),
    (3, 'C', 1, 'estandar'),
    (3, 'C', 2, 'estandar'),
    (3, 'C', 3, 'estandar'),
    (3, 'C', 4, 'estandar'),
    (4, 'A', 1, 'estandar'),
    (4, 'A', 2, 'estandar'),
    (4, 'A', 3, 'estandar'),
    (4, 'A', 4, 'estandar'),
    (4, 'B', 1, 'estandar'),
    (4, 'B', 2, 'estandar'),
    (4, 'B', 3, 'estandar'),
    (4, 'B', 4, 'estandar'),
    (4, 'C', 1, 'estandar'),
    (4, 'C', 2, 'estandar'),
    (4, 'C', 3, 'estandar'),
    (4, 'C', 4, 'estandar');

-- PELICULAS: 6 registros, con URLs de poster publicas de TMDb para el frontend
-- Son enlaces de un servicio externo y pueden cambiar con el tiempo.
INSERT INTO peliculas
    (api_id, titulo, sinopsis, poster_url, duracion_min, clasificacion, genero, anio_estreno)
VALUES
    ('tt0816692', 'Interestelar', 'Un grupo de exploradores busca un nuevo hogar para la humanidad.', 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', 169, 'PG-13', 'Ciencia ficcion', 2014),
    ('tt1375666', 'El origen', 'Un equipo intenta implantar una idea mediante los suenos.', 'https://image.tmdb.org/t/p/w500/pIkRyD18kl4FhoCNQuWxWu5cBLM.jpg', 148, 'PG-13', 'Ciencia ficcion', 2010),
    ('tt0120338', 'Titanic', 'Historia de amor a bordo de un transatlantico.', 'https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg', 194, 'PG-13', 'Romance', 1997),
    ('tt0114709', 'Toy Story', 'Los juguetes cobran vida cuando nadie los ve.', 'https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg', 81, 'G', 'Animacion', 1995),
    ('tt2380307', 'Coco', 'Un chico viaja al mundo de los muertos y descubre su historia familiar.', 'https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg', 105, 'PG', 'Animacion', 2017),
    ('tt10872600', 'Spider-Man: No Way Home', 'Peter Parker enfrenta las consecuencias de una identidad revelada.', 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg', 148, 'PG-13', 'Accion', 2021);

-- FUNCIONES: 10 registros (futuras, finalizadas y una cancelada)
INSERT INTO funciones
    (pelicula_id, sala_id, fecha_hora_inicio, fecha_hora_fin, precio_base, estado)
VALUES
    (1, 1, '2026-11-02 18:00:00', '2026-11-02 21:00:00', 8500.00, 'programada'),
    (2, 1, '2026-11-02 21:15:00', '2026-11-02 23:50:00', 8000.00, 'programada'),
    (3, 2, '2026-11-03 17:00:00', '2026-11-03 20:20:00', 7500.00, 'programada'),
    (4, 2, '2026-11-03 20:45:00', '2026-11-03 22:15:00', 7000.00, 'programada'),
    (5, 3, '2026-11-03 18:30:00', '2026-11-03 20:30:00', 7000.00, 'programada'),
    (6, 1, '2026-11-04 19:00:00', '2026-11-04 21:35:00', 9000.00, 'programada'),
    (1, 2, '2026-10-10 19:00:00', '2026-10-10 22:00:00', 6500.00, 'finalizada'),
    (5, 3, '2026-10-15 18:00:00', '2026-10-15 20:00:00', 6500.00, 'finalizada'),
    (2, 3, '2026-11-05 20:00:00', '2026-11-05 22:40:00', 8000.00, 'cancelada'),
    (3, 4, '2026-11-06 17:30:00', '2026-11-06 20:50:00', 8000.00, 'programada');

-- SERVICIOS: 6 registros
INSERT INTO servicios (nombre, descripcion, categoria, precio, stock, imagen_url) VALUES
    ('Pochoclos medianos', 'Pochoclos para una persona', 'Comida', 2500.00, 50, NULL),
    ('Gaseosa 500 ml', 'Gaseosa individual', 'Bebida', 1800.00, 70, NULL),
    ('Combo pochoclos y gaseosa', 'Pochoclos medianos y bebida', 'Combo', 4000.00, 30, NULL),
    ('Nachos', 'Nachos con salsa de queso', 'Comida', 2900.00, 25, NULL),
    ('Agua mineral', 'Botella de agua 500 ml', 'Bebida', 1500.00, 60, NULL),
    ('Golosinas surtidas', 'Pack de golosinas', 'Comida', 1300.00, 40, NULL);

-- COMPRAS: 10 registros (pendientes, pagadas, cancelada y usadas)
-- CMP-010 vuelve a reservar una butaca que CMP-005 habia cancelado.
-- Cada total coincide con sus entradas y sus servicios adicionales.
INSERT INTO compras
    (usuario_id, funcion_id, codigo, total, estado, fecha_compra,
     email_enviado, fecha_cancelacion, motivo_cancelacion,
     numero_factura, url_factura_pdf, factura_enviada)
VALUES
    (2, 1, 'CMP-001', 21000.00, 'pagada', '2026-10-27 14:00:00', TRUE, NULL, NULL, 'FAC-001', NULL, TRUE),
    (3, 2, 'CMP-002', 11600.00, 'pendiente', '2026-10-28 16:00:00', FALSE, NULL, NULL, NULL, NULL, FALSE),
    (4, 3, 'CMP-003',  7500.00, 'pagada', '2026-10-29 12:30:00', TRUE, NULL, NULL, 'FAC-003', NULL, TRUE),
    (2, 7, 'CMP-004', 15500.00, 'usada', '2026-10-09 10:00:00', TRUE, NULL, NULL, 'FAC-004', NULL, TRUE),
    (3, 5, 'CMP-005',  7000.00, 'cancelada', '2026-10-29 11:20:00', FALSE, '2026-10-30 09:00:00', 'Cambio de planes', NULL, NULL, FALSE),
    (4, 6, 'CMP-006', 11900.00, 'pagada', '2026-10-29 15:00:00', TRUE, NULL, NULL, 'FAC-006', NULL, TRUE),
    (3, 8, 'CMP-007',  8000.00, 'usada', '2026-10-14 13:00:00', TRUE, NULL, NULL, 'FAC-007', NULL, TRUE),
    (2, 4, 'CMP-008', 11000.00, 'pagada', '2026-10-29 20:30:00', TRUE, NULL, NULL, 'FAC-008', NULL, TRUE),
    (4, 1, 'CMP-009',  8500.00, 'pendiente', '2026-10-30 09:30:00', FALSE, NULL, NULL, NULL, NULL, FALSE),
    (4, 5, 'CMP-010',  7000.00, 'pagada', '2026-10-30 11:00:00', TRUE, NULL, NULL, 'FAC-010', NULL, TRUE);

-- ENTRADAS: 12 registros. La butaca 25 de funcion 5 aparece cancelada en CMP-005
-- y vuelta a comprar en CMP-010; UNIQUE solo bloquea entradas NO canceladas.
-- Las compras pendientes tienen estado 'pendiente' y qr_codigo NULL: se genera QR al pagar.
-- La validacion del QR debe verificar tambien que la compra este pagada o usada.
INSERT INTO entradas
    (compra_id, funcion_id, butaca_id, precio, qr_codigo, estado, fecha_uso, fecha_cancelacion)
VALUES
    (1, 1,  1, 8500.00, 'QR-DEMO-CMP001-A1', 'valida', NULL, NULL),
    (1, 1,  2, 8500.00, 'QR-DEMO-CMP001-A2', 'valida', NULL, NULL),
    (2, 2,  3, 8000.00, NULL, 'pendiente', NULL, NULL),
    (3, 3, 13, 7500.00, 'QR-DEMO-CMP003-A1', 'valida', NULL, NULL),
    (4, 7, 14, 6500.00, 'QR-DEMO-CMP004-A2', 'usada', '2026-10-10 18:55:00', NULL),
    (4, 7, 15, 6500.00, 'QR-DEMO-CMP004-A3', 'usada', '2026-10-10 18:58:00', NULL),
    (5, 5, 25, 7000.00, 'QR-DEMO-CMP005-A1', 'cancelada', NULL, '2026-10-30 09:00:00'),
    (6, 6,  4, 9000.00, 'QR-DEMO-CMP006-A4', 'valida', NULL, NULL),
    (7, 8, 26, 6500.00, 'QR-DEMO-CMP007-A2', 'usada', '2026-10-15 17:59:00', NULL),
    (8, 4, 16, 7000.00, 'QR-DEMO-CMP008-A4', 'valida', NULL, NULL),
    (9, 1,  5, 8500.00, NULL, 'pendiente', NULL, NULL),
    (10, 5, 25, 7000.00, 'QR-DEMO-CMP010-A1', 'valida', NULL, NULL);

-- SERVICIOS COMPRADOS: 6 registros
INSERT INTO compra_servicios
    (compra_id, servicio_id, cantidad, precio_unitario, subtotal)
VALUES
    (1, 3, 1, 4000.00, 4000.00),
    (2, 2, 2, 1800.00, 3600.00),
    (4, 1, 1, 2500.00, 2500.00),
    (6, 4, 1, 2900.00, 2900.00),
    (7, 5, 1, 1500.00, 1500.00),
    (8, 3, 1, 4000.00, 4000.00);


-- ---------------------------------------------
-- 9. REGLAS QUE DEBE IMPLEMENTAR EL BACKEND
-- ---------------------------------------------
-- La base ya impide reservas activas duplicadas por (funcion_id, butaca_id).
-- Para cancelar: actualizar compras.estado y entradas.estado a 'cancelada'
-- DENTRO DE LA MISMA TRANSACCION. Asi se libera la butaca y se conserva el historial.
-- Para pagar: verificar compra pendiente y generar qr_codigo (UNIQUE),
-- pasando sus entradas de 'pendiente' a 'valida' en una transaccion.
-- Para reservas pendientes abandonadas: definir una politica de expiracion
-- que cancele compra+entradas en una transaccion para liberar las butacas.
-- El backend debe verificar que butacas.sala_id = funciones.sala_id,
-- que la sala no tenga funciones superpuestas y que los intervalos sean validos.
-- Al programar/editar funciones, comprobar solapamientos bajo bloqueo/transaccion:
--   existente.fecha_hora_inicio < nueva_fin
--   AND existente.fecha_hora_fin > nueva_inicio
-- Los locales, usuarios, posters y entradas de este archivo son datos DEMO.
-- Al borrar un servicio con compras asociadas, la FK lo rechaza (manejar HTTP 409).
-- El SQL NO envia emails, no genera PDFs y no crea codigos QR reales:
-- esas tareas corresponden al backend y a los endpoints del TP.