# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias y el código principal
COPY requirements.txt .
COPY . .

# Instalar las librerías necesarias
# Usamos --no-cache-dir para hacer la imagen más pequeña
RUN pip install --no-cache-dir -r requirements.txt

# El comando que se ejecuta cuando el contenedor inicia
# Usamos --server.port=8080 y --server.address=0.0.0.0 que son requeridos por Cloud Run
CMD ["streamlit", "run", "app_principal.py", "--server.port=8080", "--server.address=0.0.0.0"]