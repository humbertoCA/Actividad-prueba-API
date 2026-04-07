from fastapi import FastAPI
from app.routes.upload import router as upload_router #Agregamos el router al main
from app.db.database import engine, metadata

app = FastAPI()

@app.on_event("startup")
def startup():
    metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "API funcionando 🚀"}
app.include_router(upload_router)