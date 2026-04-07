import os
import time
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date
from app.db.models import metadata


if os.getenv("ENV") == "docker":
    DATABASE_URL = "mysql+pymysql://root:rootroot@db:3306/test_db"
else:
    DATABASE_URL = "mysql+pymysql://root:rootroot@localhost:3306/test_db"

def get_engine():
    for i in range(10):  # intenta 10 veces
        try:
            engine = create_engine(DATABASE_URL)
            engine.connect()
            print("✅ Conectado a MySQL")
            return engine
        except Exception as e:
            print(f"⏳ Intento {i+1} fallido, reintentando...")
            time.sleep(3)
    raise Exception("❌ No se pudo conectar a la base de datos")

engine = get_engine()
metadata = MetaData()

transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("folio", String(50)),
    Column("fecha", Date),
    Column("categoria", String(100)),
    Column("monto", Float),
    Column("estatus", String(50)),
)
