import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# --- Configuration (BrowserStack Integration) ---
BROWSERSTACK_USERNAME = "Raginee Darade"
BROWSERSTACK_ACCESS_KEY = "owVFMzGKEKDnZdF3tFx1"
BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Define capabilities for the test
bstack_options = {
    "os": "Windows",
    "osVersion": "10",
    "projectName": "StackDemo Hackathon",
    "buildName": "Session Establishment",
    "sessionName": "TC-125 Session Test"
}
options = ChromeOptions()
options.set_capability("bstack:options", bstack_options)
options.browser_name = "Chrome"
options.browser_version = "latest"
driver = webdriver.Remote(command_executor=BROWSERSTACK_URL, options=options)

# --- Test Script Logic ---
try:
    print("Starting TC-125: User session establishment after successful authentication.")

    # Navigate to the StackDemo website
    driver.get("https://www.bstackdemo.com/")

    # Log in with valid credentials
    signin_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signin")))
    signin_button.click()
    username_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='demouser']")))
    username_option.click()
    password_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='testingisfun99']")))
    password_option.click()
    login_button = driver.find_element(By.ID, "login-btn")
    login_button.click()

    # **CRITICAL VERIFICATION FOR SESSION ESTABLISHMENT**
    # Check for the presence of elements that only appear after a successful login
    print("Verifying session establishment...")

    # 1. Check for the 'Logout' button
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "logout"))
    )

    # 2. Check for the user's name on the page
    user_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "username"))
    )

    # 3. Check for a user-specific element (e.g., a cart)
    cart_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart"))
    )

    # Final assertion
    if logout_button and user_name_element and cart_icon.is_displayed():
        print("✅ Test Passed: User session was successfully established.")
    else:
        print("❌ Test Failed: User session could not be verified.")

except (TimeoutException, NoSuchElementException) as e:
    print(
        f"❌ Test Failed: An element was not found or the page timed out. Error: {e}")

except Exception as e:
    print(f"❌ Test Failed: An unexpected error occurred. Error: {e}")

finally:
    if driver:
        driver.quit()
