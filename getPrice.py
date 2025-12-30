import os
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
URL = "https://www.arcaplanet.it/next-natural-cat-lattina-multipack-6x50g-5307/p"
DUMP_DIR = Path("dump")
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

DUMP_DIR.mkdir(exist_ok=True)

load_dotenv()
APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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
    png_path = DUMP_DIR / f"arcaplanet_{timestamp}.png"

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

    # 1️⃣ Primary method: "Single order:"
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

    raise ValueError("Price not found")


# --------------------------------------------------
# SAVE PRICE to Google Sheets
# --------------------------------------------------
def save_price(price):
    requests.post(
        APPS_SCRIPT_URL,
        json={"prezzo": round(price, 2)},
        timeout=10
    )

# --------------------------------------------------
# SEND PRICE via Telegram
# --------------------------------------------------
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

# --------------------------------------------------
# SEND SCREENSHOT via Telegram
# --------------------------------------------------
def send_telegram_photo(photo_path, caption=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    with open(photo_path, "rb") as photo:
        files = {
            "photo": photo
        }
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": caption,
            "parse_mode": "HTML"
        }

        requests.post(url, files=files, data=data)

# --------------------------------------------------
# WAIT WEB PAGE
# --------------------------------------------------
def wait_for_stable_render(driver, timeout=10):
    driver.execute_script("""
        let lastHeight = document.body.scrollHeight;
        let stableCount = 0;
        window.__stable = false;

        const interval = setInterval(() => {
            const newHeight = document.body.scrollHeight;
            if (newHeight === lastHeight) {
                stableCount++;
                if (stableCount >= 5) {
                    window.__stable = true;
                    clearInterval(interval);
                }
            } else {
                stableCount = 0;
                lastHeight = newHeight;
            }
        }, 200);
    """)

    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return window.__stable === true")
    )

# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    driver = create_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(URL)

        # 1️⃣ DOM caricato
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        # 2️⃣ Prezzo presente nel DOM
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "main [class*='price']")
            )
        )

        # 3️⃣🔥 ATTENDI RENDER STABILE
        wait_for_stable_render(driver)

        html_path, png_path = save_page(driver)

        price = extract_price_from_html(html_path)

        print(f"✅ Price found: {price:.2f} €")
        print(f"📄 HTML saved in: {html_path}")
        print(f"📸 Screenshot saved in: {png_path}")

        if price:
            save_price(price)

            send_telegram_photo(
                png_path,
                caption=(
                    f"🐱 <b>Price detected</b>\n"
                    f"Product: Next Natural Cat 6x50g\n"
                    f"Price: <b>{price:.2f} €</b>\n"
                    f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                )
            )

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

# --------------------------------------------------
if __name__ == "__main__":
    main()
