import pandas as pd
from fastapi import UploadFile

def read_file(file: UploadFile):
    try:
        # CSV
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        
        # Excel
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        
        else:
            raise ValueError("Formato no soportado")

        return df

    except Exception as e:
        raise ValueError(f"Error al leer el archivo: {str(e)}")