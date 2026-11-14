# Cine Paradiso - Backend API

Este repositorio contiene el Backend de la aplicación web **Cine Paradiso**, desarrollado en Python con el framework Flask. Su función principal es actuar como una API RESTful que centraliza la lógica de negocio, la seguridad (JWT), el acceso a la base de datos (MySQL) y la generación de códigos QR para la validación de entradas.

### Integrantes
* **María Eugenia Vallejo**
* **Maximo Febles**
* **Sebastián Romero**
* **Brunella Mía Valdata**
* **Sofia Levin**
* **Joaquín Ventura**
* **Córdoba Milagros Belén**

## Tecnologías Utilizadas

El proyecto fue desarrollado utilizando las siguientes librerías y herramientas:

*   **Flask (v3.1.3)** 
*   **Flask-SQLAlchemy (v3.1.1)**
*   **SQLAlchemy (v2.0.53)** 
*   **mysql-connector-python (v26.7.0)** 
*   **PyJWT (v2.15.1)** 
*   **Werkzeug (v3.1.8)** 
*   **python-dotenv (v1.2.3)**
*   **qrcode (v8.2)** 
*   **Pillow (v13.0.0)** 
*   **requests (v2.34.2)** 
*   **MarkupSafe (v3.0.3)** 

## Funcionalidades Principales

* Autenticación Segura (JWT): Login de usuarios y administradores. Generación de tokens con caducidad y protección de rutas según el rol (cliente o administrador).

* Gestión de Cartelera: Endpoints para listar películas, funciones y salas disponibles.

* Compra y Bloqueo de Butacas: Validación estricta a nivel base de datos para evitar que una butaca sea vendida dos veces en la misma función.

* Checkout de Servicios: Posibilidad de agregar comida, bebida a la compra de entradas.

* Cancelación de Compras: Liberación automática de las butacas si el usuario cancela dentro del plazo permitido.

* Generación y Envío de QR: Al confirmar una compra, el sistema genera un código QR único por cada entrada y lo envía al correo electrónico del usuario junto con la factura.

* Validación de Ingreso (Backoffice): Endpoint exclusivo para administradores que permite escanear el QR en la puerta del cine. El sistema verifica que corresponda a la función del día, que no haya sido utilizado ni cancelado.

* Dashboards y Estadísticas: Endpoints para alimentar las métricas del administrador (ocupación, ventas por género, franjas horarias, cancelaciones).

* Integración con **OMDb API**: El backoffice permite buscar y cargar películas directamente desde la API de OMDb (título, sinopsis, póster, duración, género y clasificación) para agilizar la gestión de la cartelera.

## Instalación y Ejecución Local

Seguí estos pasos para correr el backend en tu máquina:

### Requisitos Previos
*   Python 3.10 o superior.
*   MySQL Server.
*   Git.
*   Opcional: Postman (para probar los endpoints).

### 1. Clonar el repositorio y crear el entorno virtual
Abrí una terminal y ejecutá:
```bash
git clone https://github.com/pacha22akd/Cinema-Paradiso-Backend.git
cd cine-paradiso-backend
python -m venv venv

# Activar el entorno virtual:
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```
### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```
### 3. Levantar la base de datos
* Crear la base de datos y correr el init_db.sql:

```powershell
# WLS
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS cine_paradiso;"
Get-Content db\init_db.sql | mysql -u root -p club_deportivo
```

```bash
# Linux / macOS
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS cine_paradiso;"
mysql -u root -p cine_paradiso < db/init_db.sql
```

* Verificar que las tablas esten cargadas en la base de datos:

```powershell
# WLS
mysql -u root -p -e "USE cine_paradiso; SHOW TABLES;"
```

```bash
# Linux / macOS 
mysql -u root -p -e "USER cine_paradiso; SHOW TABLES;"
```


### 4. Configurar variables de entorno
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=cine_paradiso
OMDB_API_KEY=tu_ombd_key
SECRET_KEY=tu_clave_secreta
MAIL_USUARIO=tu_mail
MAIL_CONTRASENA=tu_contraseña_de_aplicacion
```
Para la secret key, debes abrir una terminal de python y ejecutar este comando
```
python -c “import secrets; print(secrets.token_urlsafe(48))”
```
Lo que te devuelve, lo tenes que pegar en SECRET_KEY.
Para la key de ombdb debes entrar en https://www.omdbapi.com/apikey.aspx. Una vez en la pagina seleccionas en el formulario 'FREE' y te registras con tu correo. Te llegara la key a tu correo y la pegas tal cual en OMDB_API_KEY.

### 5. Levantar el servidor
Para levantar el back tenes que estar en la carpeta raiz del proyecto y abrir una terminal para luego ejecutar el siguiente comando.
```bash
# Linux / macOS 
python app.py

# WSL
python3 app.py
```
Una vez ejecutado, el servidor comenzara a correrse en http://127.0.0.1:5000.