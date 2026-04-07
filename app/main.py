from fastapi import FastAPI
from app.routes.upload import router as upload_router #Agregamos el router al main
from app.db.database import engine, metadata

#Crear servidor de la API con FastAPI
app = FastAPI() 

#Evento que se ejecuta al iniciar la API
@app.on_event("startup")
def startup():
    metadata.create_all(engine) #Crea las tablas en la base de datos si no existen

app.include_router(upload_router) #Conecta endpoints definidos en /upload.py