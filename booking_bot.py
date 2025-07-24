import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Credentials from GitHub Secrets ---
EMAIL = os.getenv("PARKALOT_EMAIL")
PASSWORD = os.getenv("PARKALOT_PASSWORD")

# --- Chrome Options for GitHub Actions ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# --- Initialize WebDriver ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Navigating to Parkalot...")
    driver.get("https://app.parkalot.io/#/login")

    # --- Login ---
    print("Logging in...")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'LOG IN')]").click()

    # Wait for dashboard to load
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Parking')]")))
    print("Login successful!")

    # --- Navigate to booking section ---
    print("Navigating to booking page...")
    driver.get("https://app.parkalot.io/#/booking")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Book')]")))

    # --- Try booking all available days ---
    print("Attempting to book all available days...")
    book_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Book')]")

    if not book_buttons:
        print("No available days found to book.")
    else:
        for button in book_buttons:
            try:
                button.click()
                print("Booked a day successfully!")
                time.sleep(1)  # Small delay to avoid spam
            except Exception as e:
                print(f"Failed to book a day: {e}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()
    print("Booking bot finished.")
