# Imagen base oficial de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos archivos de dependencias
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY app/ .

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]

