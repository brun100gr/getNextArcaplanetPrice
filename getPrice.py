import re
import requests
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
URL = "https://www.arcaplanet.it/next-natural-cat-lattina-multipack-6x50g-5307/p"
APPS_SCRIPT_URL = "..."
DUMP_DIR = Path("dump")
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

DUMP_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# SELENIUM SETUP
# --------------------------------------------------
def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    return webdriver.Chrome(
        service=Service(CHROMEDRIVER_PATH),
        options=options
    )

# --------------------------------------------------
# SAVE HTML + SCREENSHOT
# --------------------------------------------------
def save_page(driver):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    html_path = DUMP_DIR / f"arcaplanet_{timestamp}.html"
    png_path  = DUMP_DIR / f"arcaplanet_{timestamp}.png"

    html_path.write_text(driver.page_source, encoding="utf-8")
    driver.save_screenshot(str(png_path))

    return html_path, png_path

# --------------------------------------------------
# PRICE EXTRACTION (BeautifulSoup)
# --------------------------------------------------
def extract_price_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    text = soup.get_text(separator=" ", strip=True)

    # 1️⃣ Metodo principale: "Ordine singolo:"
    match = re.search(
        r"Ordine singolo:\s*€?\s*([\d.,]+)",
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1).replace(",", "."))

    # 2️⃣ Fallback: meta tag
    meta_price = soup.find("meta", {"property": "product:price:amount"})
    if meta_price and meta_price.get("content"):
        return float(meta_price["content"])

    raise ValueError("Prezzo non trovato")

# --------------------------------------------------
# SALVA IL PREZZO su Google sheets
# --------------------------------------------------
def salva_prezzo(prezzo):
    requests.post(
        APPS_SCRIPT_URL,
        json={"prezzo": round(prezzo, 2)},
        timeout=10
    )

# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(URL)

        # attende che la pagina carichi qualcosa di significativo
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))

        html_path, png_path = save_page(driver)

        prezzo = extract_price_from_html(html_path)

        print(f"✅ Prezzo trovato: {prezzo:.2f} €")
        print(f"📄 HTML salvato in: {html_path}")
        print(f"📸 Screenshot salvato in: {png_path}")

        salva_prezzo(prezzo)

    except Exception as e:
        print("❌ Errore:", e)

    finally:
        driver.quit()

# --------------------------------------------------
if __name__ == "__main__":
    main()

