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

# --- Setup Chrome for GitHub Actions ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    # --- Open Parkalot Login Page ---
    driver.get("https://app.parkalot.io/#/login")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email")))

    # --- Log In ---
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'LOG IN')]").click()

    # Wait for dashboard to load
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Login successful!")

    # --- Book all available days ---
    time.sleep(5)  # Allow page to fully load
    booking_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Book')]")

    for i, button in enumerate(booking_buttons, start=1):
        try:
            button.click()
            print(f"Booked day #{i}")
            time.sleep(2)
        except Exception as e:
            print(f"Failed to book day #{i}: {e}")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
