from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

def obtener_transcripcion(url):
    # Configura las opciones de Selenium para Chrome
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Especifica la ubicación del binario de Chrome
    chrome_options.add_argument("--headless")  # Ejecuta el navegador en modo headless en producción
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--window-size=1920,1080")

    # Define la ubicación del driver de Chrome (en Railway se instala en /usr/local/bin/)
    chrome_driver_path = "/usr/local/bin/chromedriver"  # Ruta para Railway
    service = Service(chrome_driver_path)

    # Inicializa el navegador
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Navegando a la URL del video de YouTube")
        driver.get(url)
        
        # Espera a que la página cargue completamente
        print("Esperando que la página cargue")
        time.sleep(2)
        
        # Encuentra y presiona el botón de "Más"
        print("Buscando el botón 'Más'")
        print("Verificando si el botón 'Más' está presente")
        try:
            more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "expand"))
            )
            print("El botón 'Más' está presente")
        except Exception as e:
            print(f"No se encontró el botón 'Más': {e}")
            driver.quit()
            raise e
        print("Presionando el botón 'Más' usando Javascript")
        driver.execute_script("arguments[0].click();", more_button)
        # Espera un momento para que el desplegable esté completamente cargado
        print("Esperando que el desplegable se cargue")
        time.sleep(2)
        
        # Encuentra y desplaza la vista al botón de "Mostrar transcripción"
        print("Buscando el botón 'Mostrar transcripción'")
        transcript_button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//ytd-button-renderer[@class='style-scope ytd-video-description-transcript-section-renderer']//button[contains(@aria-label, 'transcript')]"))
        )
        print("Desplazándose al botón 'Mostrar transcripción'")
        driver.execute_script("arguments[0].scrollIntoView(true);", transcript_button)
        time.sleep(1)  # Espera breve después del desplazamiento
        
        print("Presionando el botón 'Mostrar transcripción' usando Javascript")
        driver.execute_script("arguments[0].click();", transcript_button)
        
        # Incrementamos el tiempo de espera para que la transcripción se cargue
        print("Esperando que la transcripción se cargue")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='segments-container']"))
        )
        
        # Ahora extraemos los textos de los segmentos de transcripción
        print("Extrayendo los textos de la transcripción")
        segments = driver.find_elements(By.XPATH, "//div[@id='segments-container']//yt-formatted-string[@class='segment-text style-scope ytd-transcript-segment-renderer']")
        
        # Concatenar el texto de todos los segmentos
        transcript_text = "\n".join([segment.text for segment in segments])
        
        # Limitar la transcripción a los primeros 20,000 caracteres
        if len(transcript_text) > 20000:
            print("La transcripción es demasiado larga, truncando a 20,000 caracteres")
            transcript_text = transcript_text[:20000]
        
        print("Transcripción extraída con éxito")
        
        return transcript_text
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None
    
    finally:
        # Cierra el navegador
        print("Cerrando el navegador")
        driver.quit()


@app.route("/transcripcion", methods=["POST"])
def transcripcion():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Falta la URL"}), 400
    
    transcript = obtener_transcripcion(url)
    if transcript:
        return jsonify({"transcript": transcript})
    else:
        return jsonify({"error": "No se pudo obtener la transcripción"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
