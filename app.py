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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service("/usr/local/bin/chromedriver")  # Ruta estándar en Railway
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)

        more_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "expand"))
        )
        driver.execute_script("arguments[0].click();", more_button)
        time.sleep(2)

        transcript_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ytd-button-renderer//button[contains(@aria-label, 'transcript')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", transcript_button)
        driver.execute_script("arguments[0].click();", transcript_button)

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='segments-container']"))
        )

        segments = driver.find_elements(By.XPATH, "//div[@id='segments-container']//yt-formatted-string[@class='segment-text']")
        transcript_text = "\n".join([segment.text for segment in segments])

        if len(transcript_text) > 20000:
            transcript_text = transcript_text[:20000]

        return transcript_text
    except Exception as e:
        return str(e)
    finally:
        driver.quit()

@app.route("/transcripcion", methods=["POST"])
def transcripcion():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Falta la URL"}), 400
    
    transcript = obtener_transcripcion(url)
    return jsonify({"transcript": transcript})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
