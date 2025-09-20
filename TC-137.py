#Password field visibility toggle functionality
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
# Replace these with the actual details from your web application
TARGET_URL = "https://testathon.live/?signin=true"
PASSWORD_FIELD_ID = "password"
# This is the button/icon (often an 'eye') you click to toggle visibility
TOGGLE_VISIBILITY_BUTTON_ID = "toggle-password-visibility" 

def test_password_visibility_toggle():
    """
    Automated test for password field visibility toggle functionality.
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        print(f"Navigating to {TARGET_URL}...")
        driver.get(TARGET_URL)
        
        # Locate the elements
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, PASSWORD_FIELD_ID))
        )
        toggle_button = wait.until(
            EC.element_to_be_clickable((By.ID, TOGGLE_VISIBILITY_BUTTON_ID))
        )
        print("✅ Found password field and toggle button.")

        # --- Test Case 1: Verify initial state is masked ---
        print("\n--- Testing Initial State ---")
        initial_type = password_field.get_attribute("type")
        assert initial_type == "password", \
            f"FAIL: Initial state is not 'password'. Found: '{initial_type}'"
        print("PASS: Password field is initially masked (type='password').")
        
        # Enter some text to see the effect
        password_field.send_keys("MySecret123!")

        # --- Test Case 2: Click toggle to show password ---
        print("\n--- Testing Toggle to Visible ---")
        toggle_button.click()
        time.sleep(1) # Brief pause for UI transition
        
        visible_type = password_field.get_attribute("type")
        assert visible_type == "text", \
            f"FAIL: Password field did not become visible. Type is still: '{visible_type}'"
        print("PASS: Password field is now visible (type='text').")

        # --- Test Case 3: Click toggle again to hide password ---
        print("\n--- Testing Toggle Back to Masked ---")
        toggle_button.click()
        time.sleep(1) # Brief pause for UI transition

        hidden_type = password_field.get_attribute("type")
        assert hidden_type == "password", \
            f"FAIL: Password field did not become masked again. Type is: '{hidden_type}'"
        print("PASS: Password field is masked again (type='password').")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        
    finally:
        print("\nTest finished. Closing browser.")
        driver.quit()

# --- Run the test ---
if __name__ == "__main__":
    test_password_visibility_toggle()