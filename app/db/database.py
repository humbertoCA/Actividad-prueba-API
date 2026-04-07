import os #Permite leer variables del sistema
import time #Permite usar pausas
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date
from sqlalchemy.exc import OperationalError


if os.getenv("ENV") == "docker": #Revisa si estas en estado docker
    DATABASE_URL = "mysql+pymysql://root:rootroot@db:3306/test_db"
else: # Si estoy en local
    DATABASE_URL = "mysql+pymysql://root:rootroot@localhost:3306/test_db"

#Funcion de conexion con intentos     
def get_engine(): 
    for i in range(10):  # Va a intentar conectarse 10 veces
        try:
            engine = create_engine(DATABASE_URL) #Crea la conexion usando SQLalchemy
            with engine.connect(): #Hace la conexion 
                print("Conectado a MySQL")
            return engine
        except OperationalError:
            print(f"Intento {i+1} fallido, reintentando en 3s...")
            time.sleep(3)
    raise Exception("No se pudo conectar a la base de datos") #Se arroja el error despues de intentar 10 veces

engine = get_engine()
metadata = MetaData() #Registro de la estructura de la DB

transactions = Table( #Define el nombre de la tabla como "transactions"
    "transactions",
    metadata,
    #Se crean los atributos de la tabla
    Column("id", Integer, primary_key=True, autoincrement=True), 
    Column("folio", String(50)),
    Column("fecha", Date),
    Column("categoria", String(100)),
    Column("monto", Float),
    Column("estatus", String(50)),
)

