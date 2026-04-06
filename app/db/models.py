from sqlalchemy import Table, Column, Integer, String, Float, MetaData

metadata = MetaData()

transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("folio", String(50)),
    Column("fecha", String(50)),
    Column("categoria", String(100)),
    Column("monto", Float),
    Column("estatus", String(50)),
)