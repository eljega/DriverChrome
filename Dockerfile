# Usa una imagen base que ya tenga Chrome y ChromeDriver instalados
FROM selenium/standalone-chrome:latest

# Instala dependencias adicionales si es necesario
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

# Copia tu código fuente a la imagen
COPY . /app

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias de Python
RUN pip3 install -r requirements.txt

# Expone el puerto en el que correrá tu aplicación (usualmente Flask corre en el puerto 5000)
EXPOSE 5000

# Comando para ejecutar tu aplicación
CMD ["python3", "app.py"]
