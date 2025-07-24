import sys
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Selenium Setup ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

print("Starting Parkalot Booking Bot...")

# Log in
driver.get("https://your-parking-site.com/login")
driver.find_element(By.ID, "email").send_keys("YOUR_EMAIL")
driver.find_element(By.ID, "password").send_keys("YOUR_PASSWORD")
driver.find_element(By.ID, "login-button").click()

# Wait for page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "booking-calendar")))

# --- Book All Available Days ---
dates = driver.find_elements(By.CLASS_NAME, "available-date")  # Adjust selector based on site

for date in dates:
    try:
        print(f"Attempting to book {date.text}...")
        date.click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "book-button"))).click()
        print(f"Booked {date.text} successfully!")
    except Exception as e:
        print(f"Could not book {date.text}: {e}")

driver.quit()
