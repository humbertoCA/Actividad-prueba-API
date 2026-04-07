# Imagen base
FROM python:3.11

# Carpeta de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para correr la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]