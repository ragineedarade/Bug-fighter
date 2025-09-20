import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# --- Configuration (Update these values) ---
LOGIN_URL = "https://testathon.live/login"
MFA_URL = "https://testathon.live/mfa"
DASHBOARD_URL = "https://testathon.live/dashboard"

# Locators for web elements
USERNAME_INPUT_LOCATOR = (By.ID, "username")
PASSWORD_INPUT_LOCATOR = (By.ID, "password")
LOGIN_BUTTON_LOCATOR = (By.ID, "login-btn")
MFA_INPUT_LOCATOR = (By.ID, "otp")
MFA_SUBMIT_BUTTON_LOCATOR = (By.ID, "mfa-submit-btn")
LOGOUT_BUTTON_LOCATOR = (By.ID, "logout")  # To verify successful login

# Your credentials
VALID_USERNAME = "demouser"
VALID_PASSWORD = "password123"
# Note: The OTP is simulated here. In a real scenario, you'd need a way to fetch this value.
SIMULATED_OTP = "123456"

# --- BrowserStack Integration ---
BROWSERSTACK_USERNAME = "Raginee Darade"
BROWSERSTACK_ACCESS_KEY = "owVFMzGKEKDnZdF3tFx1"
BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

bstack_options = {
    "os": "Windows",
    "osVersion": "10",
    "projectName": "Hackathon Tests",
    "buildName": "MFA Security Validation",
    "sessionName": "TC-121 MFA Test"
}
options = ChromeOptions()
options.set_capability("bstack:options", bstack_options)
options.browser_name = "Chrome"
options.browser_version = "latest"
driver = webdriver.Remote(command_executor=BROWSERSTACK_URL, options=options)

# --- Test Script Logic ---
try:
    print("Starting TC-121: MFA Security Validation.")

    # 1. Go to the login page and perform the initial login
    driver.get(LOGIN_URL)
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(USERNAME_INPUT_LOCATOR))
    username_input.send_keys(VALID_USERNAME)
    password_input = driver.find_element(PASSWORD_INPUT_LOCATOR)
    password_input.send_keys(VALID_PASSWORD)
    login_button = driver.find_element(LOGIN_BUTTON_LOCATOR)
    login_button.click()

    # 2. Wait for the MFA page and enter the OTP
    print("MFA page should be loading...")
    mfa_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(MFA_INPUT_LOCATOR))
    mfa_input.send_keys(SIMULATED_OTP)

    mfa_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(MFA_SUBMIT_BUTTON_LOCATOR))
    mfa_submit_button.click()

    # 3. Verify successful login by checking for the dashboard or a logout button
    print("Verifying successful login...")
    WebDriverWait(driver, 10).until(EC.url_to_be(DASHBOARD_URL))
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(LOGOUT_BUTTON_LOCATOR))

    if logout_button.is_displayed():
        print("✅ Test Passed: MFA validation successful and user logged in.")
    else:
        print("❌ Test Failed: User was not redirected to the dashboard or login failed.")

except (TimeoutException, NoSuchElementException) as e:
    print(
        f"❌ Test Failed: An element was not found or the page timed out. Error: {e}")

except Exception as e:
    print(f"❌ Test Failed: An unexpected error occurred. Error: {e}")

finally:
    if driver:
        driver.quit()
