# Usa una imagen base de Ubuntu más ligera y con mejor soporte
FROM ubuntu:22.04

# Instala las dependencias necesarias, incluyendo Chrome y ChromeDriver
RUN apt-get update && \
    apt-get install -y wget curl unzip python3 python3-pip libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxrender1 libxss1 libxtst6 libxi6 libxcomposite1 libxcursor1 libxdamage1 libxrandr2 libasound2 libatk1.0-0 libcups2 libpangocairo-1.0-0 libgbm1 libgtk-3-0 libdrm2 libxshmfence1 libxkbcommon0 libxkbcommon-x11-0 && \
    apt-get install -y xvfb

# Descargar e instalar Google Chrome versión 129.0.6668.70
RUN wget https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /usr/local/bin/ && \
    ln -s /usr/local/bin/chrome-linux64/chrome /usr/bin/google-chrome && \
    chmod +x /usr/local/bin/chrome-linux64/chrome && \
    rm chrome-linux64.zip

# Descargar e instalar ChromeDriver versión 129.0.6668.70
RUN wget https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    ln -s /usr/local/bin/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver-linux64.zip

# Instala las dependencias de Python
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copia el código de la aplicación
COPY . /app
WORKDIR /app

# Exponer el puerto en el que Flask va a correr
EXPOSE 5000

# Ejecuta la aplicación Flask
CMD ["python3", "app.py"]
