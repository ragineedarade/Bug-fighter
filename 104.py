from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# **1. Configuration: Update these values to match your website's elements**
# URL of the "Forgot Password" or "Password Reset" page
PASSWORD_RESET_URL = "https://testathon.live/forgot_password"

# A valid email address that is registered on the website
VALID_EMAIL = "ragineedarade@example.com"

# Locators for the email input field and the submit button
EMAIL_INPUT_LOCATOR = (By.ID, "email")
SUBMIT_BUTTON_LOCATOR = (By.XPATH, "//button[@type='submit']")
# A locator for the success message that appears after submission
SUCCESS_MESSAGE_LOCATOR = (By.CLASS_NAME, "success-message")


# **2. BrowserStack Integration (Choose one)**
# Option A: Local execution (for quick testing)
driver = webdriver.Chrome(ChromeDriverManager().install())

# OR

# Option B: BrowserStack execution (recommended for hackathon)
# BROWSERSTACK_USERNAME = "Raginee Darade"
# BROWSERSTACK_ACCESS_KEY = "owVFMzGKEKDnZdF3tFx1"
# BROWSERSTACK_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
#
# bstack_options = {
#     "os": "Windows",
#     "osVersion": "10",
#     "projectName": "Hackathon Tests",
#     "buildName": "Password Reset",
#     "sessionName": "TC-104 Valid Password Reset"
# }
# options = ChromeOptions()
# options.set_capability("bstack:options", bstack_options)
# options.browser_name = "Chrome"
# options.browser_version = "latest"
# driver = webdriver.Remote(command_executor=BROWSERSTACK_URL, options=options)


# **3. Test Script Logic**
try:
    print("Starting TC-104: Password Reset Request with Valid Email.")

    # Navigate to the password reset page
    driver.get(PASSWORD_RESET_URL)

    # Find the email input field and enter the valid email
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(EMAIL_INPUT_LOCATOR)
    )
    email_input.send_keys(VALID_EMAIL)

    # Find and click the submit button
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(SUBMIT_BUTTON_LOCATOR)
    )
    submit_button.click()

    # Verify that a success message is displayed
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(SUCCESS_MESSAGE_LOCATOR)
    )

    # Check if the message text indicates a successful reset
    if "reset link has been sent" in success_message.text.lower():
        print("✅ Test Passed: Password reset email successfully requested.")
    else:
        print(
            f"❌ Test Failed: Unexpected message displayed - '{success_message.text}'")

except (TimeoutException, NoSuchElementException) as e:
    print(
        f"❌ Test Failed: An element was not found or the page timed out. Error: {e}")

except Exception as e:
    print(f"❌ Test Failed: An unexpected error occurred. Error: {e}")

finally:
    # Always close the browser session
    if driver:
        driver.quit()
