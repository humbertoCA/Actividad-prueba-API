API de Carga de Transacciones
Descripción

Este proyecto consiste en una API desarrollada con FastAPI que permite cargar archivos (CSV o Excel) con información de transacciones, validar su contenido y almacenarlo en una base de datos MySQL.

Incluye validaciones de:

Estructura del archivo
Tipos de datos
Duplicados dentro del archivo
Duplicados contra la base de datos

El proyecto está completamente dockerizado para facilitar su ejecución.

Tecnologías utilizadas:

-Python 3.11
-FastAPI
-Pandas
-SQLAlchemy
-MySQL
-Docker & Docker Compose

Cómo ejecutar el proyecto:

1. Clonar repositorio
git clone <tu_repo_url>
cd <nombre_repo>
2. Ejecutar con Docker
docker-compose up --build
3. Acceder a la API

Abrir en navegador:

http://localhost:8000/docs

Uso de la API

Endpoint principal:

-POST /upload

Permite subir archivos:

-CSV
-Excel (.xlsx)

Validaciones implementadas
Columnas obligatorias:
-folio
-fecha
-categoria
-monto
-estatus

-Archivo no vacío
-Tipos de datos correctos
-No duplicados dentro del archivo
-No duplicados en base de datos (folio único)

Decisiones importantes
-Se utilizó folio como identificador único para evitar duplicados.
-Se implementó validación previa a la inserción en base de datos para evitar errores SQL.
-Se utilizó Docker para garantizar portabilidad y fácil ejecución.
-Se manejan errores controlados (HTTP 400) para inputs inválidos.

Variables de entorno

Se utiliza conexión a base de datos mediante:

DATABASE_URL=mysql+pymysql://root:rootroot@db:3306/test_db

Mejoras futuras (producción)

Implementar autenticación (JWT)
Manejo de logs estructurados
Paginación y endpoints de consulta
Tests automatizados (pytest)
Manejo de concurrencia
Deploy en la nube (AWS, GCP)
Uso de migrations (Alembic)

Autor
Humberto Coronel Alarcón
Proyecto desarrollado como prueba técnica para desarrollador jr.