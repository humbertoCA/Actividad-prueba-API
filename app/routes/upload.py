from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.processor import read_file

print("debug")

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

        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    