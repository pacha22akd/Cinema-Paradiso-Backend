-- Se eliminan primero las tablas hijas para respetar las FOREIGN KEY.
-- ATENCION: ejecutar este archivo elimina los datos existentes.
DROP TABLE IF EXISTS compra_servicios;
DROP TABLE IF EXISTS entradas;
DROP TABLE IF EXISTS compras;
DROP TABLE IF EXISTS funciones;
DROP TABLE IF EXISTS butacas;
DROP TABLE IF EXISTS servicios;
DROP TABLE IF EXISTS peliculas;
DROP TABLE IF EXISTS salas;
DROP TABLE IF EXISTS locales;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS roles;

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
    precio_base    FLOAT NOT NULL,
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
    precio            FLOAT NOT NULL,
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

-- ============================================================
-- DATOS DE PRUEBA: basados en datos_demo.sql
-- ============================================================
-- Se fijan algunos ID porque datos_demo.sql los referencia directamente.
-- Se conserva la estructura de todas las tablas sin columnas adicionales.
-- Los valores 'hash_demo_*' son marcadores y NO son hashes válidos para login.

-- 1. ROLES (archivo datos_demo.sql)
INSERT INTO roles (id, nombre) VALUES
    (1, 'Administrador'),
    (2, 'Cliente');

-- 2. LOCALES (3 únicos; se excluye el segundo INSERT duplicado)
-- Nota: datos_demo.sql repite Palermo con teléfono diferente.
-- Se conserva la primera versión: 011-4822-9980.
INSERT INTO locales (id, nombre, direccion, ciudad, telefono) VALUES
    (1, 'Cine Paradiso Centro', 'Av. Corrientes 1234', 'CABA', '011-4000-0000'),
    (2, 'Cine Paradiso Belgrano', 'Av. Cabildo 2450', 'CABA', '011-4789-1234'),
    (3, 'Cine Paradiso Palermo', 'Av. Santa Fe 3200', 'CABA', '011-4822-9980');

-- 3. USUARIOS
-- Los primeros tres usuarios son los de datos_demo.sql.
-- Se añade un usuario de prueba id=4 porque COMPRA-004 refiere a usuario_id=4.
INSERT INTO usuarios (id, nombre, apellido, email, password_hash, telefono, rol_id) VALUES
    (1, 'María', 'Gómez', 'maria.gomez@email.com', 'hash_demo_456', '1122334455', 2),
    (2, 'Carlos', 'López', 'carlos.lopez@email.com', 'hash_demo_789', '1166778899', 2),
    (3, 'Ana', 'Martínez', 'ana.martinez@email.com', 'hash_demo_101', '1144556677', 1),
    (4, 'Usuario', 'DePrueba', 'usuario4.demo@example.com', 'hash_demo_usuario4', NULL, 2);

-- 4. SALAS (datos_demo.sql)
INSERT INTO salas (id, local_id, nombre, capacidad, tipo) VALUES
    (1, 1, 'Sala IMAX', 150, 'IMAX 3D'),
    (2, 2, 'Sala VIP 1', 50, 'Premium'),
    (3, 2, 'Sala VIP 2', 50, 'Premium'),
    (4, 3, 'Sala 1', 120, '2D');

-- 5. PELÍCULAS (ids 3..6 para respetar las referencias de datos_demo.sql)
INSERT INTO peliculas (id, titulo, sinopsis, duracion_min, clasificacion, genero, anio_estreno) VALUES
    (3, 'Nueve Reinas', 'Dos estafadores de poca monta se unen para un gran negocio.', 114, '+13', 'Policial/Comedia', 2000),
    (4, 'El Robo del Siglo', 'Un grupo de ladrones planea el asalto al Banco Río de Acassuso.', 114, '+13', 'Suspenso/Comedia', 2020),
    (5, 'Argentina, 1985', 'Un equipo jurídico se atreve a enjuiciar a la dictadura militar.', 140, '+13', 'Drama/Historia', 2022),
    (6, 'Esperando la Carroza', 'Una comedia clásica sobre los conflictos de una familia argentina.', 94, 'ATP', 'Comedia', 1985);

-- 6. FUNCIONES (datos_demo.sql: ids 3..6 para que las compras referencien las correctas)
INSERT INTO funciones (id, pelicula_id, sala_id, fecha, hora_inicio, hora_fin, precio_base, estado) VALUES
    (3, 3, 3, '2026-11-01', '15:00:00', '17:20:00', 6000.00, 'programada'),
    (4, 4, 4, '2026-11-01', '19:00:00', '20:34:00', 7500.00, 'programada'),
    (5, 5, 1, '2026-11-02', '21:30:00', '23:50:00', 5000.00, 'programada'),
    (6, 6, 2, '2026-11-02', '18:00:00', '19:34:00', 4000.00, 'programada');

-- 7. BUTACAS
-- Se conservan exactamente las tres posiciones indicadas en datos_demo.sql:
-- id=4 sala=3 B1, id=5 sala=3 B2, id=6 sala=4 A1 (vip).
-- El resto se generan como datos de prueba para igualar las capacidades de las salas.
INSERT INTO butacas (id, sala_id, fila, numero, tipo) VALUES
    (1, 1, 'A', 1, 'estandar'),
    (2, 1, 'A', 2, 'estandar'),
    (3, 2, 'A', 1, 'vip'),
    (4, 3, 'B', 1, 'estandar'),
    (5, 3, 'B', 2, 'estandar'),
    (6, 4, 'A', 1, 'vip'),
    (7, 1, 'A', 3, 'estandar'),
    (8, 1, 'A', 4, 'estandar'),
    (9, 1, 'A', 5, 'estandar'),
    (10, 1, 'A', 6, 'estandar'),
    (11, 1, 'A', 7, 'estandar'),
    (12, 1, 'A', 8, 'estandar'),
    (13, 1, 'A', 9, 'estandar'),
    (14, 1, 'A', 10, 'estandar'),
    (15, 1, 'B', 1, 'estandar'),
    (16, 1, 'B', 2, 'estandar'),
    (17, 1, 'B', 3, 'estandar'),
    (18, 1, 'B', 4, 'estandar'),
    (19, 1, 'B', 5, 'estandar'),
    (20, 1, 'B', 6, 'estandar'),
    (21, 1, 'B', 7, 'estandar'),
    (22, 1, 'B', 8, 'estandar'),
    (23, 1, 'B', 9, 'estandar'),
    (24, 1, 'B', 10, 'estandar'),
    (25, 1, 'C', 1, 'estandar'),
    (26, 1, 'C', 2, 'estandar'),
    (27, 1, 'C', 3, 'estandar'),
    (28, 1, 'C', 4, 'estandar'),
    (29, 1, 'C', 5, 'estandar'),
    (30, 1, 'C', 6, 'estandar'),
    (31, 1, 'C', 7, 'estandar'),
    (32, 1, 'C', 8, 'estandar'),
    (33, 1, 'C', 9, 'estandar'),
    (34, 1, 'C', 10, 'estandar'),
    (35, 1, 'D', 1, 'estandar'),
    (36, 1, 'D', 2, 'estandar'),
    (37, 1, 'D', 3, 'estandar'),
    (38, 1, 'D', 4, 'estandar'),
    (39, 1, 'D', 5, 'estandar'),
    (40, 1, 'D', 6, 'estandar'),
    (41, 1, 'D', 7, 'estandar'),
    (42, 1, 'D', 8, 'estandar'),
    (43, 1, 'D', 9, 'estandar'),
    (44, 1, 'D', 10, 'estandar'),
    (45, 1, 'E', 1, 'estandar'),
    (46, 1, 'E', 2, 'estandar'),
    (47, 1, 'E', 3, 'estandar'),
    (48, 1, 'E', 4, 'estandar'),
    (49, 1, 'E', 5, 'estandar'),
    (50, 1, 'E', 6, 'estandar'),
    (51, 1, 'E', 7, 'estandar'),
    (52, 1, 'E', 8, 'estandar'),
    (53, 1, 'E', 9, 'estandar'),
    (54, 1, 'E', 10, 'estandar'),
    (55, 1, 'F', 1, 'estandar'),
    (56, 1, 'F', 2, 'estandar'),
    (57, 1, 'F', 3, 'estandar'),
    (58, 1, 'F', 4, 'estandar'),
    (59, 1, 'F', 5, 'estandar'),
    (60, 1, 'F', 6, 'estandar'),
    (61, 1, 'F', 7, 'estandar'),
    (62, 1, 'F', 8, 'estandar'),
    (63, 1, 'F', 9, 'estandar'),
    (64, 1, 'F', 10, 'estandar'),
    (65, 1, 'G', 1, 'estandar'),
    (66, 1, 'G', 2, 'estandar'),
    (67, 1, 'G', 3, 'estandar'),
    (68, 1, 'G', 4, 'estandar'),
    (69, 1, 'G', 5, 'estandar'),
    (70, 1, 'G', 6, 'estandar'),
    (71, 1, 'G', 7, 'estandar'),
    (72, 1, 'G', 8, 'estandar'),
    (73, 1, 'G', 9, 'estandar'),
    (74, 1, 'G', 10, 'estandar'),
    (75, 1, 'H', 1, 'estandar'),
    (76, 1, 'H', 2, 'estandar'),
    (77, 1, 'H', 3, 'estandar'),
    (78, 1, 'H', 4, 'estandar'),
    (79, 1, 'H', 5, 'estandar'),
    (80, 1, 'H', 6, 'estandar'),
    (81, 1, 'H', 7, 'estandar'),
    (82, 1, 'H', 8, 'estandar'),
    (83, 1, 'H', 9, 'estandar'),
    (84, 1, 'H', 10, 'estandar'),
    (85, 1, 'I', 1, 'estandar'),
    (86, 1, 'I', 2, 'estandar'),
    (87, 1, 'I', 3, 'estandar'),
    (88, 1, 'I', 4, 'estandar'),
    (89, 1, 'I', 5, 'estandar'),
    (90, 1, 'I', 6, 'estandar'),
    (91, 1, 'I', 7, 'estandar'),
    (92, 1, 'I', 8, 'estandar'),
    (93, 1, 'I', 9, 'estandar'),
    (94, 1, 'I', 10, 'estandar'),
    (95, 1, 'J', 1, 'estandar'),
    (96, 1, 'J', 2, 'estandar'),
    (97, 1, 'J', 3, 'estandar'),
    (98, 1, 'J', 4, 'estandar'),
    (99, 1, 'J', 5, 'estandar'),
    (100, 1, 'J', 6, 'estandar'),
    (101, 1, 'J', 7, 'estandar'),
    (102, 1, 'J', 8, 'estandar'),
    (103, 1, 'J', 9, 'estandar'),
    (104, 1, 'J', 10, 'estandar'),
    (105, 1, 'K', 1, 'estandar'),
    (106, 1, 'K', 2, 'estandar'),
    (107, 1, 'K', 3, 'estandar'),
    (108, 1, 'K', 4, 'estandar'),
    (109, 1, 'K', 5, 'estandar'),
    (110, 1, 'K', 6, 'estandar'),
    (111, 1, 'K', 7, 'estandar'),
    (112, 1, 'K', 8, 'estandar'),
    (113, 1, 'K', 9, 'estandar'),
    (114, 1, 'K', 10, 'estandar'),
    (115, 1, 'L', 1, 'estandar'),
    (116, 1, 'L', 2, 'estandar'),
    (117, 1, 'L', 3, 'estandar'),
    (118, 1, 'L', 4, 'estandar'),
    (119, 1, 'L', 5, 'estandar'),
    (120, 1, 'L', 6, 'estandar'),
    (121, 1, 'L', 7, 'estandar'),
    (122, 1, 'L', 8, 'estandar'),
    (123, 1, 'L', 9, 'estandar'),
    (124, 1, 'L', 10, 'estandar'),
    (125, 1, 'M', 1, 'estandar'),
    (126, 1, 'M', 2, 'estandar'),
    (127, 1, 'M', 3, 'estandar'),
    (128, 1, 'M', 4, 'estandar'),
    (129, 1, 'M', 5, 'estandar'),
    (130, 1, 'M', 6, 'estandar'),
    (131, 1, 'M', 7, 'estandar'),
    (132, 1, 'M', 8, 'estandar'),
    (133, 1, 'M', 9, 'estandar'),
    (134, 1, 'M', 10, 'estandar'),
    (135, 1, 'N', 1, 'estandar'),
    (136, 1, 'N', 2, 'estandar'),
    (137, 1, 'N', 3, 'estandar'),
    (138, 1, 'N', 4, 'estandar'),
    (139, 1, 'N', 5, 'estandar'),
    (140, 1, 'N', 6, 'estandar'),
    (141, 1, 'N', 7, 'estandar'),
    (142, 1, 'N', 8, 'estandar'),
    (143, 1, 'N', 9, 'estandar'),
    (144, 1, 'N', 10, 'estandar'),
    (145, 1, 'O', 1, 'estandar'),
    (146, 1, 'O', 2, 'estandar'),
    (147, 1, 'O', 3, 'estandar'),
    (148, 1, 'O', 4, 'estandar'),
    (149, 1, 'O', 5, 'estandar'),
    (150, 1, 'O', 6, 'estandar'),
    (151, 1, 'O', 7, 'estandar'),
    (152, 1, 'O', 8, 'estandar'),
    (153, 1, 'O', 9, 'estandar'),
    (154, 1, 'O', 10, 'estandar'),
    (155, 2, 'A', 2, 'vip'),
    (156, 2, 'A', 3, 'vip'),
    (157, 2, 'A', 4, 'vip'),
    (158, 2, 'A', 5, 'vip'),
    (159, 2, 'A', 6, 'vip'),
    (160, 2, 'A', 7, 'vip'),
    (161, 2, 'A', 8, 'vip'),
    (162, 2, 'A', 9, 'vip'),
    (163, 2, 'A', 10, 'vip'),
    (164, 2, 'B', 1, 'vip'),
    (165, 2, 'B', 2, 'vip'),
    (166, 2, 'B', 3, 'vip'),
    (167, 2, 'B', 4, 'vip'),
    (168, 2, 'B', 5, 'vip'),
    (169, 2, 'B', 6, 'vip'),
    (170, 2, 'B', 7, 'vip'),
    (171, 2, 'B', 8, 'vip'),
    (172, 2, 'B', 9, 'vip'),
    (173, 2, 'B', 10, 'vip'),
    (174, 2, 'C', 1, 'vip'),
    (175, 2, 'C', 2, 'vip'),
    (176, 2, 'C', 3, 'vip'),
    (177, 2, 'C', 4, 'vip'),
    (178, 2, 'C', 5, 'vip'),
    (179, 2, 'C', 6, 'vip'),
    (180, 2, 'C', 7, 'vip'),
    (181, 2, 'C', 8, 'vip'),
    (182, 2, 'C', 9, 'vip'),
    (183, 2, 'C', 10, 'vip'),
    (184, 2, 'D', 1, 'vip'),
    (185, 2, 'D', 2, 'vip'),
    (186, 2, 'D', 3, 'vip'),
    (187, 2, 'D', 4, 'vip'),
    (188, 2, 'D', 5, 'vip'),
    (189, 2, 'D', 6, 'vip'),
    (190, 2, 'D', 7, 'vip'),
    (191, 2, 'D', 8, 'vip'),
    (192, 2, 'D', 9, 'vip'),
    (193, 2, 'D', 10, 'vip'),
    (194, 2, 'E', 1, 'vip'),
    (195, 2, 'E', 2, 'vip'),
    (196, 2, 'E', 3, 'vip'),
    (197, 2, 'E', 4, 'vip'),
    (198, 2, 'E', 5, 'vip'),
    (199, 2, 'E', 6, 'vip'),
    (200, 2, 'E', 7, 'vip'),
    (201, 2, 'E', 8, 'vip'),
    (202, 2, 'E', 9, 'vip'),
    (203, 2, 'E', 10, 'vip'),
    (204, 3, 'A', 1, 'vip'),
    (205, 3, 'A', 2, 'vip'),
    (206, 3, 'A', 3, 'vip'),
    (207, 3, 'A', 4, 'vip'),
    (208, 3, 'A', 5, 'vip'),
    (209, 3, 'A', 6, 'vip'),
    (210, 3, 'A', 7, 'vip'),
    (211, 3, 'A', 8, 'vip'),
    (212, 3, 'A', 9, 'vip'),
    (213, 3, 'A', 10, 'vip'),
    (214, 3, 'B', 3, 'vip'),
    (215, 3, 'B', 4, 'vip'),
    (216, 3, 'B', 5, 'vip'),
    (217, 3, 'B', 6, 'vip'),
    (218, 3, 'B', 7, 'vip'),
    (219, 3, 'B', 8, 'vip'),
    (220, 3, 'B', 9, 'vip'),
    (221, 3, 'B', 10, 'vip'),
    (222, 3, 'C', 1, 'vip'),
    (223, 3, 'C', 2, 'vip'),
    (224, 3, 'C', 3, 'vip'),
    (225, 3, 'C', 4, 'vip'),
    (226, 3, 'C', 5, 'vip'),
    (227, 3, 'C', 6, 'vip'),
    (228, 3, 'C', 7, 'vip'),
    (229, 3, 'C', 8, 'vip'),
    (230, 3, 'C', 9, 'vip'),
    (231, 3, 'C', 10, 'vip'),
    (232, 3, 'D', 1, 'vip'),
    (233, 3, 'D', 2, 'vip'),
    (234, 3, 'D', 3, 'vip'),
    (235, 3, 'D', 4, 'vip'),
    (236, 3, 'D', 5, 'vip'),
    (237, 3, 'D', 6, 'vip'),
    (238, 3, 'D', 7, 'vip'),
    (239, 3, 'D', 8, 'vip'),
    (240, 3, 'D', 9, 'vip'),
    (241, 3, 'D', 10, 'vip'),
    (242, 3, 'E', 1, 'vip'),
    (243, 3, 'E', 2, 'vip'),
    (244, 3, 'E', 3, 'vip'),
    (245, 3, 'E', 4, 'vip'),
    (246, 3, 'E', 5, 'vip'),
    (247, 3, 'E', 6, 'vip'),
    (248, 3, 'E', 7, 'vip'),
    (249, 3, 'E', 8, 'vip'),
    (250, 3, 'E', 9, 'vip'),
    (251, 3, 'E', 10, 'vip'),
    (252, 4, 'A', 2, 'estandar'),
    (253, 4, 'A', 3, 'estandar'),
    (254, 4, 'A', 4, 'estandar'),
    (255, 4, 'A', 5, 'estandar'),
    (256, 4, 'A', 6, 'estandar'),
    (257, 4, 'A', 7, 'estandar'),
    (258, 4, 'A', 8, 'estandar'),
    (259, 4, 'A', 9, 'estandar'),
    (260, 4, 'A', 10, 'estandar'),
    (261, 4, 'B', 1, 'estandar'),
    (262, 4, 'B', 2, 'estandar'),
    (263, 4, 'B', 3, 'estandar'),
    (264, 4, 'B', 4, 'estandar'),
    (265, 4, 'B', 5, 'estandar'),
    (266, 4, 'B', 6, 'estandar'),
    (267, 4, 'B', 7, 'estandar'),
    (268, 4, 'B', 8, 'estandar'),
    (269, 4, 'B', 9, 'estandar'),
    (270, 4, 'B', 10, 'estandar'),
    (271, 4, 'C', 1, 'estandar'),
    (272, 4, 'C', 2, 'estandar'),
    (273, 4, 'C', 3, 'estandar'),
    (274, 4, 'C', 4, 'estandar'),
    (275, 4, 'C', 5, 'estandar'),
    (276, 4, 'C', 6, 'estandar'),
    (277, 4, 'C', 7, 'estandar'),
    (278, 4, 'C', 8, 'estandar'),
    (279, 4, 'C', 9, 'estandar'),
    (280, 4, 'C', 10, 'estandar'),
    (281, 4, 'D', 1, 'estandar'),
    (282, 4, 'D', 2, 'estandar'),
    (283, 4, 'D', 3, 'estandar'),
    (284, 4, 'D', 4, 'estandar'),
    (285, 4, 'D', 5, 'estandar'),
    (286, 4, 'D', 6, 'estandar'),
    (287, 4, 'D', 7, 'estandar'),
    (288, 4, 'D', 8, 'estandar'),
    (289, 4, 'D', 9, 'estandar'),
    (290, 4, 'D', 10, 'estandar'),
    (291, 4, 'E', 1, 'estandar'),
    (292, 4, 'E', 2, 'estandar'),
    (293, 4, 'E', 3, 'estandar'),
    (294, 4, 'E', 4, 'estandar'),
    (295, 4, 'E', 5, 'estandar'),
    (296, 4, 'E', 6, 'estandar'),
    (297, 4, 'E', 7, 'estandar'),
    (298, 4, 'E', 8, 'estandar'),
    (299, 4, 'E', 9, 'estandar'),
    (300, 4, 'E', 10, 'estandar'),
    (301, 4, 'F', 1, 'estandar'),
    (302, 4, 'F', 2, 'estandar'),
    (303, 4, 'F', 3, 'estandar'),
    (304, 4, 'F', 4, 'estandar'),
    (305, 4, 'F', 5, 'estandar'),
    (306, 4, 'F', 6, 'estandar'),
    (307, 4, 'F', 7, 'estandar'),
    (308, 4, 'F', 8, 'estandar'),
    (309, 4, 'F', 9, 'estandar'),
    (310, 4, 'F', 10, 'estandar'),
    (311, 4, 'G', 1, 'estandar'),
    (312, 4, 'G', 2, 'estandar'),
    (313, 4, 'G', 3, 'estandar'),
    (314, 4, 'G', 4, 'estandar'),
    (315, 4, 'G', 5, 'estandar'),
    (316, 4, 'G', 6, 'estandar'),
    (317, 4, 'G', 7, 'estandar'),
    (318, 4, 'G', 8, 'estandar'),
    (319, 4, 'G', 9, 'estandar'),
    (320, 4, 'G', 10, 'estandar'),
    (321, 4, 'H', 1, 'estandar'),
    (322, 4, 'H', 2, 'estandar'),
    (323, 4, 'H', 3, 'estandar'),
    (324, 4, 'H', 4, 'estandar'),
    (325, 4, 'H', 5, 'estandar'),
    (326, 4, 'H', 6, 'estandar'),
    (327, 4, 'H', 7, 'estandar'),
    (328, 4, 'H', 8, 'estandar'),
    (329, 4, 'H', 9, 'estandar'),
    (330, 4, 'H', 10, 'estandar'),
    (331, 4, 'I', 1, 'estandar'),
    (332, 4, 'I', 2, 'estandar'),
    (333, 4, 'I', 3, 'estandar'),
    (334, 4, 'I', 4, 'estandar'),
    (335, 4, 'I', 5, 'estandar'),
    (336, 4, 'I', 6, 'estandar'),
    (337, 4, 'I', 7, 'estandar'),
    (338, 4, 'I', 8, 'estandar'),
    (339, 4, 'I', 9, 'estandar'),
    (340, 4, 'I', 10, 'estandar'),
    (341, 4, 'J', 1, 'estandar'),
    (342, 4, 'J', 2, 'estandar'),
    (343, 4, 'J', 3, 'estandar'),
    (344, 4, 'J', 4, 'estandar'),
    (345, 4, 'J', 5, 'estandar'),
    (346, 4, 'J', 6, 'estandar'),
    (347, 4, 'J', 7, 'estandar'),
    (348, 4, 'J', 8, 'estandar'),
    (349, 4, 'J', 9, 'estandar'),
    (350, 4, 'J', 10, 'estandar'),
    (351, 4, 'K', 1, 'estandar'),
    (352, 4, 'K', 2, 'estandar'),
    (353, 4, 'K', 3, 'estandar'),
    (354, 4, 'K', 4, 'estandar'),
    (355, 4, 'K', 5, 'estandar'),
    (356, 4, 'K', 6, 'estandar'),
    (357, 4, 'K', 7, 'estandar'),
    (358, 4, 'K', 8, 'estandar'),
    (359, 4, 'K', 9, 'estandar'),
    (360, 4, 'K', 10, 'estandar'),
    (361, 4, 'L', 1, 'estandar'),
    (362, 4, 'L', 2, 'estandar'),
    (363, 4, 'L', 3, 'estandar'),
    (364, 4, 'L', 4, 'estandar'),
    (365, 4, 'L', 5, 'estandar'),
    (366, 4, 'L', 6, 'estandar'),
    (367, 4, 'L', 7, 'estandar'),
    (368, 4, 'L', 8, 'estandar'),
    (369, 4, 'L', 9, 'estandar'),
    (370, 4, 'L', 10, 'estandar');

-- 8. COMPRAS (datos_demo.sql, preservando los tres registros y sus importes)
-- IMPORTANTE: los totales 12000 y 7500 NO incluyen sus servicios agregados.
-- Se mantienen los importes originales para no alterar los datos proporcionados.
INSERT INTO compras (id, usuario_id, funcion_id, codigo, total, estado, numero_factura) VALUES
    (2, 2, 3, 'COMPRA-002', 12000.00, 'pagada', 'FAC-0001'),
    (3, 3, 4, 'COMPRA-003', 7500.00, 'pagada', 'FAC-0002'),
    (4, 4, 5, 'COMPRA-004', 5000.00, 'cancelada', 'FAC-0003');

-- 9. ENTRADAS (ids de butaca 4,5,6 respetados)
INSERT INTO entradas (compra_id, funcion_id, butaca_id, precio, qr_codigo, estado) VALUES
    (2, 3, 4, 6000.00, 'QR-ENTRY-002', 'valida'),
    (2, 3, 5, 6000.00, 'QR-ENTRY-003', 'valida'),
    (3, 4, 6, 7500.00, 'QR-ENTRY-004', 'valida');

-- 10. SERVICIOS (tercer servicio id=4 porque datos_demo.sql lo referencia así)
INSERT INTO servicios (id, nombre, descripcion, categoria, precio, stock) VALUES
    (1, 'Nachos con Queso', 'Porción de nachos acompañados de salsa de queso caliente', 'Candy Bar', 4200.00, 30),
    (2, 'Golosinas Variadas', 'Pack de chocolates y gomitas', 'Candy Bar', 2800.00, 100),
    (4, 'Balde Pochoclo Gigante', 'Balde para compartir', 'Candy Bar', 4500.00, 40);

-- 11. COMPRA DE SERVICIOS (datos_demo.sql)
INSERT INTO compra_servicios (compra_id, servicio_id, cantidad, precio_unitario, subtotal) VALUES
    (2, 1, 1, 3500.00, 3500.00),
    (2, 2, 1, 4200.00, 4200.00),
    (3, 4, 1, 4500.00, 4500.00);