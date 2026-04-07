import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date
from app.db.models import metadata


if os.getenv("ENV") == "docker":
    DATABASE_URL = "mysql+pymysql://root:rootroot@db:3306/test_db"
else:
    DATABASE_URL = "mysql+pymysql://root:rootroot@localhost:3306/test_db"

engine = create_engine(DATABASE_URL)
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
metadata.create_all(engine)