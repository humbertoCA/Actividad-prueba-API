from fastapi import FastAPI
from app.routes.upload import router as upload_router #Agregamos el router al main

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API funcionando 🚀"}
app.include_router(upload_router)