import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# **Ensure these are your actual credentials**
BROWSERSTACK_USERNAME = "Raginee Darade"
BROWSERSTACK_ACCESS_KEY = "owVFMzGKEKDnZdF3tFx1"

# The correct way to embed credentials in the URL
BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# Define BrowserStack-specific capabilities
bstack_options = {
    "os": "Windows",
    "osVersion": "10",
    "projectName": "StackDemo Hackathon",
    "buildName": "Valid Login Test",
    "sessionName": "TC-140 Valid Login Test",
}

# Create a ChromeOptions object
options = ChromeOptions()
options.set_capability("bstack:options", bstack_options)
options.browser_name = "Chrome"
options.browser_version = "latest"

# Initialize driver to None outside the try block
driver = None

try:
    print("Starting valid login test on BrowserStack...")

    # The credentials are part of the command_executor URL, not a separate keyword
    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=options
    )

    # --- Test Logic ---
    driver.get("https://www.bstackdemo.com/")
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
    logout_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "logout")))

    if logout_button.is_displayed():
        print("Test Passed: Login was successful.")
    else:
        print("Test Failed: The 'Logout' button was not displayed.")

except Exception as e:
    print(f"Test Failed due to an unexpected exception: {e}")

finally:
    if driver:
        driver.quit()
