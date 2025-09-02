from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging


class RegistrationPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Homepage elements and actions
    def get_homepage_heading(self):
        """Get the main heading text from homepage"""
        try:
            heading_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Your Child')]"))
            )
            return heading_element.text
        except Exception as e:
            logging.error(f"Homepage heading not found: {e}")
            return None

    def get_statistics_elements(self):
        """Get all statistics from homepage"""
        try:
            stats = {}
            # These selectors need to be updated based on actual DOM structure
            stats['students'] = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Students')]").text
            stats['guardians'] = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Guardians')]").text
            stats['teachers'] = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Teachers')]").text
            stats['schools'] = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Schools')]").text
            return stats
        except Exception as e:
            logging.error(f"Statistics elements not found: {e}")
            return None

    def click_sign_up_for_free_button(self):
        """Click the Sign Up for Free button on homepage"""
        try:
            sign_up_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sign Up for Free')]"))
            )
            sign_up_button.click()
            logging.info("Sign Up for Free button clicked successfully.")
        except Exception as e:
            logging.error(f"Sign Up for Free button not found: {e}")
            raise e

    # Sign Up page elements and actions
    def get_signup_heading(self):
        """Get the Sign Up page heading"""
        try:
            heading_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sign Up')]"))
            )
            return heading_element.text
        except Exception as e:
            logging.error(f"Sign Up heading not found: {e}")
            return None

    def get_signup_subtitle(self):
        """Get the Sign Up page subtitle"""
        try:
            subtitle_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Create your account')]"))
            )
            return subtitle_element.text
        except Exception as e:
            logging.error(f"Sign Up subtitle not found: {e}")
            return None

    def enter_full_name(self, fullname_value):
        """Enter full name in registration form"""
        try:
            fullname_field = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#signup_name"))
            )
            fullname_field.clear()
            fullname_field.send_keys(str(fullname_value))
            logging.info("Full Name entered successfully.")
        except Exception as e:
            logging.error(f"Full Name field not found: {e}")
            raise e

    def enter_email(self, email_value):
        """Enter email in registration form"""
        try:
            email_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#signup_email"))
            )
            email_field.clear()
            email_field.send_keys(str(email_value))
            logging.info("Email entered successfully.")
        except Exception as e:
            logging.error(f"Email field not found: {e}")
            raise e

    def enter_password(self, password_value):
        """Enter password in registration form"""
        try:
            password_field = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#signup_password"))
            )
            password_field.clear()
            password_field.send_keys(str(password_value))
            logging.info("Password entered successfully.")
        except Exception as e:
            logging.error(f"Password field not found: {e}")
            raise e

    def enter_confirm_password(self, confirm_password_value):
        """Enter confirm password in registration form"""
        try:
            confirm_password_field = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#signup_confirmPassword"))
            )
            confirm_password_field.clear()
            confirm_password_field.send_keys(str(confirm_password_value))
            logging.info("Confirm Password entered successfully.")
        except Exception as e:
            logging.error(f"Confirm Password field not found: {e}")
            raise e

    def click_signup_button(self):
        """Click the Sign Up button"""
        try:
            signup_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'] span"))
            )
            signup_button.click()
            logging.info("Sign Up button clicked successfully.")
        except Exception as e:
            logging.error(f"Sign Up button not found: {e}")
            raise e

    def click_google_signup_button(self):
        """Click the Sign up with Google button"""
        try:
            google_signup_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sign up with Google')]"))
            )
            google_signup_button.click()
            logging.info("Sign up with Google button clicked successfully.")
        except Exception as e:
            logging.error(f"Google Sign Up button not found: {e}")
            raise e

    def click_signin_link_from_signup(self):
        """Click Sign In link from Sign Up page"""
        try:
            signin_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='text-[#1a5683] hover:underline']"))
            )
            signin_link.click()
            logging.info("Sign In link clicked successfully.")
        except Exception as e:
            logging.error(f"Sign In link not found: {e}")
            raise e

    def click_back_button(self):
        """Click back arrow button"""
        try:
            back_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".back-button, [aria-label='back'], button:contains('←')"))
            )
            back_button.click()
            logging.info("Back button clicked successfully.")
        except Exception as e:
            logging.error(f"Back button not found: {e}")
            raise e

    def get_validation_error_message(self, field_name):
        """Get HTML5 validation error message for specific field"""
        try:
            field_selectors = {
                "FullName": "div[id='signup_name_help'] div[class='ant-form-item-explain-error']",
                "Email": "div[id='signup_email_help'] div[class='ant-form-item-explain-error']",
                "Password": "div[id='signup_password_help'] div[class='ant-form-item-explain-error']",
                "ConfirmPassword": "div[id='signup_confirmPassword_help'] div[class='ant-form-item-explain-error']"
            }

            field_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, field_selectors[field_name]))
            )
            return field_element.text
        except Exception as e:
            logging.error(f"Validation error message not found for {field_name}: {e}")
            return None

    def get_registration_success_message(self):
        """Get registration success/error message from Ant Design popup"""
        try:
            # Wait for any Ant Design message popup (success or error)
            message_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='ant-message'] span:nth-child(2)"))
            )
            message_text = message_element.text
            logging.info(f"Ant Design message captured: {message_text}")
            return message_text
        except Exception as e:
            logging.error(f"Ant Design message not found: {e}")

            # Fallback: Try alternative selectors for Ant Design messages
            alternative_selectors = [
                "div[class*='ant-message-notice-content']",
                "div[class*='ant-notification'] div[class*='ant-notification-notice-message']",
                "div[role='alert']",
                "div[class*='message'] span",
                ".ant-message-custom-content span"
            ]

            for selector in alternative_selectors:
                try:
                    fallback_element = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    message_text = fallback_element.text
                    logging.info(f"Message found with fallback selector '{selector}': {message_text}")
                    return message_text
                except:
                    continue

            logging.error("No registration message found with any selector")
            return None

    def get_copyright_text(self):
        """Get copyright text from page footer"""
        try:
            copyright_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '© 2025 DOER')]"))
            )
            return copyright_element.text
        except Exception as e:
            logging.error(f"Copyright text not found: {e}")
            return None

    def verify_form_fields_present(self, expected_fields):
        """Verify all expected form fields are present"""
        try:
            field_selectors = {
                "Full Name": "#signup_name",
                "Email": "#signup_email",
                "Password": "#signup_password",
                "Confirm Password": "#signup_confirmPassword"
            }

            for field in expected_fields:
                if field in field_selectors:
                    field_element = self.driver.find_element(By.CSS_SELECTOR, field_selectors[field])
                    if not field_element.is_displayed():
                        return False
            return True
        except Exception as e:
            logging.error(f"Form field verification failed: {e}")
            return False

    def verify_buttons_present(self, expected_buttons):
        """Verify all expected buttons are present"""
        try:
            for button_text in expected_buttons:
                button_element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{button_text}')]")
                if not button_element.is_displayed():
                    return False
            return True
        except Exception as e:
            logging.error(f"Button verification failed: {e}")
            return False