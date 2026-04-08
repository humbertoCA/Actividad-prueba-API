import pandas as pd
import unicodedata
from fastapi import UploadFile
from sqlalchemy import text

def normalize_columns(df): #Normalizacion de columnas
    df.columns = [
        unicodedata.normalize('NFKD', col) #Convierte caracteres especiales a forma "base" í => i + ´
        .encode('ascii', 'ignore') #Elimina caracteres que no son ASCII (´,~)
        .decode('utf-8') #Convierte bytes a texto
        .strip() #Quita espacios al inicio y final
        .lower() #Convierte a minusculas
        for col in df.columns
    ]
    return df #Devuelve el DataFrame normalizado

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
        
        df = normalize_columns(df)
        
        df.columns = df.columns.str.strip().str.lower()

        if df.empty:
            raise ValueError("El archivo está vacío")

        return df

    except Exception as e:
        raise ValueError(f"Error al leer el archivo: {str(e)}")
    
REQUIRED_COLUMNS = ["folio", "fecha", "categoria", "monto", "estatus"]

#Verifica que el archivo tenga lo necesario
def validate_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {missing}") #ej. Si el archivo no trae "Fecha" se exhibe

#Validacion de filas
def validate_rows(df):
    errors = []

    for index, row in df.iterrows(): #Recorre num de fila y contenido
        # Validar monto
        try:
            float(row["monto"]) #Monto sea numerico
        except:
            errors.append({
                "row": index,
                "error": "Monto inválido"
            })

        # Validar fecha vacia (simple)
        if pd.isna(row["fecha"]) or str(row["fecha"]).strip() == "":
            errors.append({
                "row": index,
                "error": "Fecha vacía"
            })
        else:
            # Intenta convertir a fecha valida
            try:
                pd.to_datetime(row["fecha"])
            except:
                errors.append({
                    "row": index,
                    "error": "Fecha con formato inválido"
                })
    return errors

def process_data(df):
    total_records = len(df) #Total de filas

    df["monto"] = pd.to_numeric(df["monto"], errors="coerce") #Convierte monto a numerico, si falla ponen NaN

    valid_df = df.dropna(subset=["monto"]) #Elimina filas donde el monto sea invalido

    total_amount = valid_df["monto"].sum() #Suma solamente los montos validos

    by_status = df.groupby("estatus").size().to_dict() #Cuenta registros por status

    by_category = df.groupby("categoria")["monto"].sum().to_dict() #Suma dinero por categoria 

    return {
        "total_records": int(len(df)),
        "total_amount": float(df["monto"].sum()),
        "by_status": {k: int(v) for k, v in df["estatus"].value_counts().to_dict().items()},
        "by_category": {k: float(v) for k, v in df.groupby("categoria")["monto"].sum().to_dict().items()}
    }

def detect_duplicates(df): #Encuentra folios duplicados 
    duplicates = df[df.duplicated(subset=["folio"], keep=False)]

    errors = []

    for index, row in duplicates.iterrows():
        errors.append({
            "row": index,
            "error": f"Folio duplicado: {row['folio']}"
        })

    return errors

def check_existing_folios(df, engine):
    folios = df["folio"].tolist()
    
    query = f"SELECT folio FROM transactions WHERE folio IN ({','.join(map(str, folios))})" #query para buscar duplicados en DB
    
    with engine.connect() as conn: #Abre la conexion a la DB con SQLAlchemy
        result = conn.execute(text(query), {"folios": tuple(folios)})
        existing = sorted(set([row[0] for row in result]))
    if existing:
        raise ValueError(f"Folios ya existen en DB: {existing}")

def save_to_db(df, engine, table):
    
    records = df.to_dict(orient="records")

    with engine.connect() as conn: #Inserta Datos a la DB
        conn.execute(table.insert(), records)
        conn.commit()

    df = df[["folio", "fecha", "categoria", "monto", "estatus"]]

    #df.to_sql("transactions", con=engine, if_exists="append", index=False)