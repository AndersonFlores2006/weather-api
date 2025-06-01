FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto que usa la aplicación
EXPOSE 8080

# Variable de entorno para indicar que estamos en producción
ENV FLASK_ENV=production

# Comando para ejecutar la aplicación
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app