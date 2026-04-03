from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.processor import read_file, validate_columns, validate_rows, process_data

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    
    # Validar que exista archivo
    if not file:
        raise HTTPException(status_code=400, detail="No se envió ningún archivo")
    
    # Validar tipo de archivo (CSV o Excel)
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Formato no soportado. Usa CSV o Excel")
    
    try:
        df = read_file(file)

        validate_columns(df)

        errors = validate_rows(df)

        result = process_data(df)

        return {
            "filename": file.filename,
            "summary": result,
            "errors": errors
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    