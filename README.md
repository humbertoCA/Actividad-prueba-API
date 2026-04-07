# API de Carga de Transacciones
## Descripción

Este proyecto consiste en una API desarrollada con FastAPI que permite cargar archivos (CSV o Excel) con información de transacciones, validar su contenido y almacenarlo en una base de datos MySQL.

Incluye validaciones de:

- Estructura del archivo
- Tipos de datos
- Duplicados dentro del archivo
- Duplicados contra la base de datos

El proyecto está completamente dockerizado para facilitar su ejecución.

---

## Tecnologías utilizadas:

- Python 3.11
- FastAPI
- Pandas
- SQLAlchemy
- MySQL
- Docker & Docker Compose

---

## Cómo ejecutar el proyecto:

### 1. Clonar repositorio
```bash
git clone https://github.com/humbertoCA/Actividad-prueba-API
cd Actividad-prueba-API
```
### 2. Ejecutar con Docker
```bash
docker-compose up --build
```
### 3. Acceder a la API

Abrir en navegador:

http://localhost:8000/docs

---

## Uso de la API

Endpoint principal:

-POST /upload

Permite subir archivos:

-CSV
-Excel (.xlsx)

---

## Validaciones implementadas
Columnas obligatorias:
- folio
- fecha
- categoria
- monto
- estatus
- Archivo no vacío
- Tipos de datos correctos
- No duplicados dentro del archivo
- No duplicados en base de datos (folio único)

---

## Decisiones importantes
- Se eligió FastAPI por su facilidad de uso, Pandas para procesar archivos y SQLalchemy Core para control directo sobre consultas.
- Se utilizó folio como identificador único para evitar duplicados.
- Se implementó validación previa a la inserción en base de datos para evitar errores SQL.
- Se utilizó Docker para garantizar portabilidad y fácil ejecución.
- Se manejan errores controlados usando HTTP exception para inputs inválidos y respuestas claras al usuario.

--- 

### Variables de entorno

Se utiliza conexión a base de datos mediante:
```bash
DATABASE_URL=mysql+pymysql://root:rootroot@db:3306/test_db
```
---

### Mejoras futuras (producción)

- Mejor manejo de las credenciales para mayor seguridad
- Mejorar mensajes de error para que sean mas claros al usuario
- Agregar mas validaciones (ej. monto negativo, estatus validos)
- Permitir subir archivos muy grandes de forma eficiente
- Agregar autenticación para controlar quien puede usar la API
- Segmentación de consulta (de 10 en 10) para consultas grandes
- Manejo de rendimiento cuando varios usuarios usan la API

---

## Autor
Humberto Coronel Alarcón
- Proyecto desarrollado como prueba técnica para desarrollador jr.