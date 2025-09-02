from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging


class LoginPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def get_signin_heading(self):
        """Get the Sign In page heading"""
        try:
            heading_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[@class='text-3xl font-bold text-[#1a5683]']"))
            )
            return heading_element.text
        except Exception as e:
            logging.error(f"Sign In heading not found: {e}")
            return None

    def get_signin_subtitle(self):
        """Get the Sign In page subtitle"""
        try:
            subtitle_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//p[@class='text-gray-500 mt-2']"))
            )
            return subtitle_element.text
        except Exception as e:
            logging.error(f"Sign In subtitle not found: {e}")
            return None

    def enter_email(self, email_value):
        """Enter email in login form"""
        try:
            email_field = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#login_email"))
            )
            email_field.clear()
            email_field.send_keys(str(email_value))
            logging.info("Email entered successfully in login form.")
        except Exception as e:
            logging.error(f"Email field not found in login form: {e}")
            raise e

    def enter_password(self, password_value):
        """Enter password in login form"""
        try:
            password_field = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#login_password"))
            )
            password_field.clear()
            password_field.send_keys(str(password_value))
            logging.info("Password entered successfully in login form.")
        except Exception as e:
            logging.error(f"Password field not found in login form: {e}")
            raise e

    def click_password_visibility_view(self):
        """Click password visibility toggle (eye icon)"""
        try:
            toggle_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='eye-invisible']//*[name()='svg']"))
            )
            toggle_button.click()
            logging.info("Password visibility toggle clicked successfully.")
        except Exception as e:
            logging.error(f"Password visibility toggle not found: {e}")
            raise e

    def click_password_visibility_hide(self):
        """Click password visibility toggle (eye icon)"""
        try:
            toggle_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='eye']//*[name()='svg']"))
            )
            toggle_button.click()
            logging.info("Password visibility toggle clicked successfully.")
        except Exception as e:
            logging.error(f"Password visibility toggle not found: {e}")
            raise e

    def check_keep_me_logged_in(self, should_check=True):
        """Check or uncheck the 'Keep me logged in' checkbox"""
        try:
            checkbox = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".ant-checkbox-label"))
            )
            if should_check != checkbox.is_selected():
                checkbox.click()
            logging.info(f"Keep me logged in checkbox {'checked' if should_check else 'unchecked'} successfully.")
        except Exception as e:
            logging.error(f"Keep me logged in checkbox not found: {e}")
            raise e

    def click_login_button(self):
        """Click the Log In button"""
        try:
            login_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[type='submit']"))
            )
            login_button.click()
            logging.info("Log In button clicked successfully.")
        except Exception as e:
            logging.error(f"Log In button not found: {e}")
            raise e

    def click_google_signin_button(self):
        """Click the Sign in with Google button"""
        try:
            google_signin_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='button']"))
            )
            google_signin_button.click()
            logging.info("Sign in with Google button clicked successfully.")
        except Exception as e:
            logging.error(f"Google Sign In button not found: {e}")
            raise e

    def click_forgot_password_link(self):
        """Click the Forgot password? link"""
        try:
            forgot_password_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='text-gray-500 hover:text-[#1a5683] text-sm']"))
            )
            forgot_password_link.click()
            logging.info("Forgot password link clicked successfully.")
        except Exception as e:
            logging.error(f"Forgot password link not found: {e}")
            raise e

    def click_create_account_link(self):
        """Click Create an Account link from Sign In page"""
        try:
            create_account_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='text-[#1a5683] hover:underline']"))
            )
            create_account_link.click()
            logging.info("Create an Account link clicked successfully.")
        except Exception as e:
            logging.error(f"Create an Account link not found: {e}")
            raise e

    def get_login_error_message(self):
        """Get login error message"""
        try:
            error_message = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class='ant-message ant-message-top css-1rfzxih'] span:nth-child(2)"))
            )
            return error_message.text
        except Exception as e:
            logging.error(f"Login error message not found: {e}")
            return None

    def get_login_success_message(self):
        """Get login success message or check if redirected to dashboard"""
        try:
            # Check for success message
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='ant-message ant-message-top css-1rfzxih'] span:nth-child(2)"))
            )
            return success_message.text
        except:
            # If no success message, check if URL changed (redirected)
            current_url = self.driver.current_url
            if "dashboard" in current_url.lower() or "admin" in current_url.lower():
                return "Redirected to dashboard successfully"
            return None

    def verify_signin_form_elements(self, expected_elements):
        """Verify all expected sign in form elements are present"""
        try:
            element_selectors = {
                "Email": "//input[@id='login_email']",
                "Password": "//input[@id='login_password']",
                "Keep me logged in": "//span[@class='ant-checkbox-label']",
                "Forgot password?": "//a[@class='text-gray-500 hover:text-[#1a5683] text-sm']",
                "Log In": "//button[@type='submit']",
                "Sign in with Google": "//span[normalize-space()='Sign in with Google']"
            }

            for element_name in expected_elements:
                if element_name in element_selectors:
                    selector = element_selectors[element_name]
                    if selector.startswith("/"):  # XPath selector
                        element = self.driver.find_element(By.XPATH, selector)
                    else:  # CSS selector
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)

                    if not element.is_displayed():
                        return False
            return True
        except Exception as e:
            logging.error(f"Sign in form elements verification failed: {e}")
            return False

    def get_password_field_type(self):
        """Get the type attribute of password field (to check visibility)"""
        try:
            password_field = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#login_password"))
            )
            return password_field.get_attribute("type")
        except Exception as e:
            logging.error(f"Password field not found: {e}")
            return None

    def is_keep_logged_in_checked(self):
        """Check if Keep me logged in checkbox is checked"""
        try:
            checkbox = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox'], input[name='keepLoggedIn']"))
            )
            return checkbox.is_selected()
        except Exception as e:
            logging.error(f"Keep me logged in checkbox not found: {e}")
            return False

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

    def verify_navigation_links_present(self):
        """Verify navigation links are present"""
        try:
            not_registered_text = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Not registered yet')]")
            create_account_link = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Create an Account')]")
            return not_registered_text.is_displayed() and create_account_link.is_displayed()
        except Exception as e:
            logging.error(f"Navigation links verification failed: {e}")
            return False