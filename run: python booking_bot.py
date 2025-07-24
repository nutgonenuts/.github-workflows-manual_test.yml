import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Credentials from secrets ---
EMAIL = os.getenv("PARKALOT_EMAIL")
PASSWORD = os.getenv("PARKALOT_PASSWORD")

# --- Setup Chrome for GitHub Actions ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

try:
    # --- Step 1: Go to login page ---
    driver.get("https://app.parkalot.io/#/login")
    print("Opened Parkalot login page...")

    # --- Step 2: Enter login details ---
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='email']"))).send_keys(EMAIL)
    driver.find_element(By.XPATH, "//input[@placeholder='password']").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'LOG IN')]").click()
    print("Logged in successfully...")

    # --- Step 3: Wait for dashboard ---
    WebDriverWait(driver, 15).until(EC.url_contains("dashboard"))
    print("Dashboard loaded.")

    # --- Step 4: Book all available days ---
    # This step needs the actual structure of booking buttons on the dashboard.
    # Assuming buttons with class 'reserve-slot':
    slots = driver.find_elements(By.XPATH, "//button[contains(text(), 'Book')]")
    for slot in slots:
        try:
            slot.click()
            print("Booked a slot.")
            time.sleep(1)
        except:
            print("Failed to book one slot.")

finally:
    driver.quit()
    print("Bot finished.")
