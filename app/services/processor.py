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

        elif df.empty:
            raise ValueError("El archivo está vacío")
        
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
        if pd.isna(row["Fecha"]) or str(row["Fecha"]).strip() == "":
            errors.append({
                "row": index,
                "error": "Fecha vacía"
            })
        else:
            # Fecha mal formateada
            try:
                pd.to_datetime(row["Fecha"])
            except:
                errors.append({
                    "row": index,
                    "error": "Fecha con formato inválido"
                })
    return errors

def process_data(df):
    total_records = len(df)

    df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce")

    valid_df = df.dropna(subset=["Monto"])

    total_amount = valid_df["Monto"].sum()

    by_status = df.groupby("Estatus").size().to_dict()

    by_category = df.groupby("Categoría")["Monto"].sum().to_dict()

    return {
        "total_records": total_records,
        "total_amount": total_amount,
        "by_status": by_status,
        "by_category": by_category
    }

def detect_duplicates(df):
    duplicates = df[df.duplicated(subset=["Folio"], keep=False)]

    errors = []

    for index, row in duplicates.iterrows():
        errors.append({
            "row": index,
            "error": f"Folio duplicado: {row['Folio']}"
        })

    return errors

def validate_date_format(df):
    errors = []

    for index, row in df.iterrows():
        try:
            pd.to_datetime(row["Fecha"])
        except:
            errors.append({
                "row": index,
                "error": "Fecha con formato inválido"
            })

    return errors