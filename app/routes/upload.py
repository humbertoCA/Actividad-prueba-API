from fastapi import APIRouter, UploadFile, File, HTTPException #Herramientas para crear rutas y manejar errores 
#Separacion de responsabilidades
from app.services.processor import read_file, validate_columns, validate_rows, process_data, detect_duplicates 
from app.services.processor import save_to_db, check_existing_folios

#Conexion a base de datos y tabla
from app.db.database import engine, transactions

#Manejar errores de duplicados en DB
from sqlalchemy.exc import IntegrityError

router = APIRouter() #Crear router para agrupar endpoints

@router.post("/upload") #Endpoint POST para subir archivos
async def upload_file(file: UploadFile = File(...)):
    
    # Validar que exista archivo
    if not file:
        raise HTTPException(status_code=400, detail="No se envió ningún archivo")
    
    # Validar tipo de archivo (CSV o Excel)
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Formato no soportado. Usa CSV o Excel")
    
    try:
        #Intenta leer el archivo y convertirlo a DataFrame 
        df = read_file(file)

        if df.empty: #Validar que no este vacio
            raise ValueError("El archivo está vacío")

        validate_columns(df) #Validar columnas obligatorias

        duplicate_errors = detect_duplicates(df) #Detectar duplicados dentro del archivo

        row_errors = validate_rows(df) #Validaciones por fila (Tipos, valores, formatos, etc.)

        errors = row_errors + duplicate_errors #Union de errores encontrados

        result = process_data(df) #Procesar datos (Resumen, metricas, etc.)

        check_existing_folios(df, engine) #Validar duplicados frente a la base de datos

        try:
            #Intenta solo guardar si no hay errores
            if not errors:
                save_to_db(df, engine, transactions)
        
        #Respuesta a errores con duplicados en DB
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Ya existen registros con el mismo folio (duplicados)"
            )

        df = df.dropna(subset=["monto"]) #Limpiar datos

        #Respuesta de la API
        return {
            "filename": file.filename,
            "summary": result,
            "errors": errors
        }

    except Exception as e:
        #Respuesta general a errores
        raise HTTPException(status_code=400, detail=str(e))
    