import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Credentials from GitHub Secrets ---
EMAIL = os.getenv("PARKALOT_EMAIL")
PASSWORD = os.getenv("PARKALOT_PASSWORD")

# --- Chrome Options for GitHub Actions ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://app.parkalot.io/#/login")

try:
    # --- Login ---
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "email"))
    ).send_keys(EMAIL)

    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'LOG IN')]").click()

    # --- Wait for booking page to load ---
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Book')]"))
    )

    # --- Book all available days ---
    book_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Book')]")
    for btn in book_buttons:
        try:
            btn.click()
            print("Booked a slot.")
            time.sleep(1)
        except:
            print("Could not book a slot.")
            continue

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
