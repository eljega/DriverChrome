# Usa una imagen base de Ubuntu más ligera y con mejor soporte
FROM ubuntu:22.04

# Instala las dependencias necesarias, incluyendo Chrome y ChromeDriver
RUN apt-get update && \
    apt-get install -y wget curl unzip python3 python3-pip && \
    apt-get install -y xvfb libxi6 libgconf-2-4 && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable && \
    wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip && apt-get clean

# Instala las dependencias de Python
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Copia el código de la aplicación
COPY . /app
WORKDIR /app

# Exponer el puerto en el que Flask va a correr
EXPOSE 5000

# Ejecuta la aplicación Flask
CMD ["python3", "app.py"]
