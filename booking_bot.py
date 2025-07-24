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

print("Starting booking bot...")

# --- Chrome Options for GitHub Actions ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://app.parkalot.io/#/login")
print("Opened Parkalot login page.")

try:
    # --- Login ---
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(PASSWORD)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'LOG IN')]"))).click()
    print("Login submitted. Waiting for dashboard...")
    
    # --- Wait for dashboard ---
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Logged in successfully.")

    # --- Book all available days ---
    buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Book')]")
    if not buttons:
        print("No booking buttons found!")
    else:
        for i, btn in enumerate(buttons, start=1):
            try:
                btn.click()
                print(f"Booked day #{i}")
                time.sleep(1)
            except Exception as e:
                print(f"Failed to click button #{i}: {e}")

except Exception as e:
    print(f"Error during booking process: {e}")

finally:
    driver.quit()
    print("Booking bot finished.")
