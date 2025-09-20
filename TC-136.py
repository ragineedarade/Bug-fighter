#Username field special character handling and validation
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
# Replace these values with your application's details
TARGET_URL = "https://testathon.live/?signin=true"  # URL of the page with the form
USERNAME_FIELD_ID = "username"                 # ID of the username input field
ERROR_MESSAGE_ID = "username-error"            # ID of the error message element
# The exact error text your application shows for invalid characters
EXPECTED_ERROR_MESSAGE = "Username contains invalid characters" 

# --- Test Data ---
# Define which special characters are allowed and which are not
ALLOWED_CHARS = ['_', '-', '.']
DISALLOWED_CHARS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=']
BASE_USERNAME = "testuser"

def test_username_special_characters():
    """
    Automated test for username field special character handling.
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 5) # Use a shorter wait for faster loops
    
    # Track test results
    passed_cases = 0
    failed_cases = 0

    try:
        driver.get(TARGET_URL)
        print("✅ Page loaded successfully.")

        # --- Test Case 1: Allowed Special Characters ---
        print("\n--- Testing ALLOWED Special Characters ---")
        for char in ALLOWED_CHARS:
            test_username = f"{BASE_USERNAME}{char}valid"
            print(f"Testing with username: '{test_username}'")
            
            try:
                username_field = driver.find_element(By.ID, USERNAME_FIELD_ID)
                username_field.clear()
                username_field.send_keys(test_username)
                username_field.send_keys("\t") # Trigger validation by tabbing out
                
                # We expect the error message NOT to be visible
                wait.until(
                    EC.invisibility_of_element_located((By.ID, ERROR_MESSAGE_ID))
                )
                print("  -> PASS: No error message appeared as expected.")
                passed_cases += 1
            except Exception:
                print(f"  -> FAIL: An unexpected error message appeared for allowed character '{char}'.")
                failed_cases += 1
            time.sleep(0.5) # Small delay between tests

        # --- Test Case 2: Disallowed Special Characters ---
        print("\n--- Testing DISALLOWED Special Characters ---")
        for char in DISALLOWED_CHARS:
            test_username = f"{BASE_USERNAME}{char}invalid"
            print(f"Testing with username: '{test_username}'")
            
            try:
                username_field = driver.find_element(By.ID, USERNAME_FIELD_ID)
                username_field.clear()
                username_field.send_keys(test_username)
                username_field.send_keys("\t") # Trigger validation
                
                # We expect the error message TO BE visible
                error_element = wait.until(
                    EC.visibility_of_element_located((By.ID, ERROR_MESSAGE_ID))
                )
                
                # Optionally, check if the error text is correct
                assert EXPECTED_ERROR_MESSAGE in error_element.text
                
                print(f"  -> PASS: Validation error message appeared as expected: '{error_element.text}'")
                passed_cases += 1
            except Exception:
                print(f"  -> FAIL: The expected error message did not appear for disallowed character '{char}'.")
                failed_cases += 1
            time.sleep(0.5)

    finally:
        print("\n--- Test Summary ---")
        print(f"✅ Passed: {passed_cases}")
        print(f"❌ Failed: {failed_cases}")
        print("----------------------")
        print("Test finished. Closing browser.")
        driver.quit()

# --- Run the test ---
if __name__ == "__main__":
    test_username_special_characters()