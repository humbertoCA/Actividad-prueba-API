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
    
REQUIRED_COLUMNS = ["Folio", "Fecha", "Categoría", "Monto", "Estatus"]

def validate_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {missing}")

def validate_rows(df):
    errors = []

    for index, row in df.iterrows():
        # Validar monto
        try:
            float(row["Monto"])
        except:
            errors.append({
                "row": index,
                "error": "Monto inválido"
            })

        # Validar fecha (simple)
        if not row["Fecha"]:
            errors.append({
                "row": index,
                "error": "Fecha vacía"
            })

    return errors

def process_data(df):
    total_records = len(df)

    df["Monto"] = df["Monto"].astype(float)

    total_amount = df["Monto"].sum()

    by_status = df.groupby("Estatus").size().to_dict()

    by_category = df.groupby("Categoría")["Monto"].sum().to_dict()

    return {
        "total_records": total_records,
        "total_amount": total_amount,
        "by_status": by_status,
        "by_category": by_category
    }