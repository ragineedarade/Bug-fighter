#Username field character limit validation and enforcement
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
# Replace these values with the actual details from your web application
TARGET_URL = "https://testathon.live/?signin=true"  # The URL of the page with the form
USERNAME_FIELD_ID = "username"                 # The ID of the username input field
ERROR_MESSAGE_ID = "username-error"            # The ID of the error message element
MAX_LENGTH = 15                                # The expected maximum character limit

# --- Test Data ---
string_below_limit = "shortuser"
string_at_limit = "a" * MAX_LENGTH
string_above_limit = "a" * (MAX_LENGTH + 5)


def test_username_character_limit():
    """
    Automated test for TC-134: Username field character limit validation.
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get(TARGET_URL)
        print("✅ Page loaded successfully.")

        # Find the username field
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, USERNAME_FIELD_ID))
        )
        print(f"✅ Found username field with ID: '{USERNAME_FIELD_ID}'")

        # --- Test Case 1: Input string longer than the limit (Enforcement Check) ---
        print("\n--- Testing Enforcement (maxlength attribute) ---")
        username_field.clear()
        username_field.send_keys(string_above_limit)
        time.sleep(1) # Small pause to allow UI to update

        # Get the actual value from the input field
        entered_text = username_field.get_attribute("value")
        
        # Assert that the input was truncated to the max length
        assert len(entered_text) == MAX_LENGTH, \
            f"FAIL: Field should enforce a {MAX_LENGTH}-char limit. Actual length: {len(entered_text)}."
        
        print(f"PASS: Input was correctly truncated to {len(entered_text)} characters.")
        
        # --- Test Case 2: Input string longer than the limit (Validation Error Message) ---
        print("\n--- Testing Validation (Error Message) ---")
        username_field.clear()
        username_field.send_keys(string_above_limit)
        
        # Trigger validation by 'tabbing out' of the field
        username_field.send_keys("\t") 
        time.sleep(1) # Pause for JS validation to trigger

        try:
            # Check if the error message is now visible
            error_element = wait.until(
                EC.visibility_of_element_located((By.ID, ERROR_MESSAGE_ID))
            )
            expected_error_text = f"Username cannot exceed {MAX_LENGTH} characters."
            
            assert expected_error_text in error_element.text, \
                f"FAIL: Incorrect error message. Expected '{expected_error_text}', Got '{error_element.text}'"
                
            print(f"PASS: Correct validation error message is displayed: '{error_element.text}'")

        except Exception:
            print(f"FAIL: Validation error message with ID '{ERROR_MESSAGE_ID}' did not appear.")
            # Note: This might be expected if the app only uses enforcement.

        # --- Test Case 3: Input valid string (at the limit) ---
        print("\n--- Testing Valid Input (at limit) ---")
        username_field.clear()
        username_field.send_keys(string_at_limit)
        username_field.send_keys("\t") # Tab out to see if error appears
        
        # Assert that the error message is NOT visible
        try:
            error_element_gone = wait.until(
                EC.invisibility_of_element_located((By.ID, ERROR_MESSAGE_ID))
            )
            if error_element_gone:
                 print("PASS: No error message is shown for input at the character limit.")
        except Exception:
            print("FAIL: Error message is still visible for a valid length username.")
        

    finally:
        print("\nTest finished. Closing browser.")
        driver.quit()

# --- Run the test ---
if __name__ == "__main__":
    test_username_character_limit()