#Password field character limit validation and enforcement

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class PasswordFieldValidationTest(unittest.TestCase):

    def setUp(self):
        # Launch browser
        self.driver = webdriver.Chrome()
        self.driver.get("https://testathon.live/?signin=true")  # Change to your target URL
        self.driver.maximize_window()

    def test_password_character_limit(self):
        driver = self.driver

        # Locate the password field (update selector as per your site)
        password_field = driver.find_element(By.ID, "password")

        # Test Data
        max_limit = 12  # Change according to your app rule
        long_password = "A" * (max_limit + 5)  # 5 chars more than limit

        # Enter password longer than allowed
        password_field.send_keys(long_password)

        # Get actual value in the field
        entered_value = password_field.get_attribute("value")

        # Validation: Length should not exceed limit
        self.assertLessEqual(len(entered_value), max_limit, 
            f"Password field accepted more than {max_limit} characters!")

        print(f"✅ Test Passed: Field restricted input to {len(entered_value)} characters.")

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
