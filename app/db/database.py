from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date
from app.db.models import metadata

DATABASE_URL = f"mysql+pymysql://root:rootroot@localhost/test_db"

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