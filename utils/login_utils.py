import logging
import time
from selenium.webdriver.common.by import By
from utils.screenshot_utils import capture_full_page_screenshot
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage


def perform_login(driver, wait, login_data, test_name=""):
    """
    Utility function to perform login with given credentials

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        login_data: Dictionary containing email and password
        test_name: Name of the test calling this function (for screenshots)

    Returns:
        bool: True if login successful, False otherwise

    Raises:
        Exception: If login process fails
    """
    logging.info(f"Starting login process for {test_name}")

    # Create page objects
    registration_page = RegistrationPage(driver, wait)
    login_page = LoginPage(driver, wait)

    try:
        # Navigate to Sign Up page first, then to Sign In page
        registration_page.click_sign_up_for_free_button()
        logging.info("Navigated to Sign Up page successfully.")
        time.sleep(2)

        # Navigate to Sign In page
        registration_page.click_signin_link_from_signup()
        logging.info("Navigated to Sign In page successfully.")
        time.sleep(2)

    except Exception as e:
        logging.error(f"Navigation to Sign In page failed: {e}")
        capture_full_page_screenshot(driver, f"{test_name}_Navigation_Error")
        raise Exception(f"Navigation to Sign In page failed: {e}")

    # Verify we're on Sign In page
    try:
        signin_heading = login_page.get_signin_heading()
        if signin_heading and "sign in" in signin_heading.lower():
            logging.info("Sign In page loaded successfully.")
        else:
            logging.error(f"Sign In page not loaded correctly. Heading: {signin_heading}")
            capture_full_page_screenshot(driver, f"{test_name}_Page_Load_Error")
            raise Exception(f"Sign In page not loaded correctly. Heading: {signin_heading}")
    except Exception as e:
        logging.error(f"Sign In page verification failed: {e}")
        capture_full_page_screenshot(driver, f"{test_name}_Verification_Error")
        raise Exception(f"Sign In page verification failed: {e}")

    # Enter email
    try:
        login_page.enter_email(login_data["email"])
        logging.info("Email entered successfully in login form.")
    except Exception as e:
        logging.error(f"Email entry failed in login form: {e}")
        capture_full_page_screenshot(driver, f"{test_name}_Email_Error")
        raise Exception(f"Email entry failed in login form: {e}")

    # Enter password
    try:
        login_page.enter_password(login_data["password"])
        logging.info("Password entered successfully in login form.")
    except Exception as e:
        logging.error(f"Password entry failed in login form: {e}")
        capture_full_page_screenshot(driver, f"{test_name}_Password_Error")
        raise Exception(f"Password entry failed in login form: {e}")

    # Take screenshot before login attempt
    capture_full_page_screenshot(driver, f"{test_name}_Before_Login")

    # Click login button
    try:
        login_page.click_login_button()
        logging.info("Log In button clicked successfully.")
        time.sleep(3)  # Wait for login process
    except Exception as e:
        logging.error(f"Log In button click failed: {e}")
        capture_full_page_screenshot(driver, f"{test_name}_Login_Button_Error")
        raise Exception(f"Log In button click failed: {e}")

    # Validate login success
    try:
        current_url = driver.current_url
        success_message = login_page.get_login_success_message()
        login_successful = False

        # Check for success message
        if "Login successful!" in success_message:
            capture_full_page_screenshot(driver, f"{test_name}_Login_Success")
            logging.info(f"Login success message found: {success_message}")
            login_successful = True

        # Check URL redirection
        elif ("/en" in current_url.lower() or
              "/en/profile" in current_url.lower() or
              "portal" in current_url.lower() or
              "home" in current_url.lower()):
            capture_full_page_screenshot(driver, f"{test_name}_Login_Success")
            logging.info(f"Login successful - redirected to: {current_url}")
            login_successful = True

        # Check if we're no longer on login page
        elif "sign-in" not in current_url.lower():
            capture_full_page_screenshot(driver, f"{test_name}_Login_Success")
            logging.info("Login successful - no longer on login page")
            login_successful = True

        if not login_successful:
            # Check for error messages
            error_message = login_page.get_login_error_message()
            if error_message:
                logging.error(f"Login failed with error: {error_message}")
                capture_full_page_screenshot(driver, f"{test_name}_Login_Error")
                raise Exception(f"Login failed with error: {error_message}")
            else:
                # Additional check for any visible error elements
                try:
                    error_elements = driver.find_elements(By.CSS_SELECTOR, ".error, .alert-danger, .login-error")
                    if error_elements and error_elements[0].is_displayed():
                        error_text = error_elements[0].text
                        logging.error(f"Login failed with visible error: {error_text}")
                        raise Exception(f"Login failed with visible error: {error_text}")
                except:
                    pass

                logging.error(f"Login success not confirmed. Current URL: {current_url}")
                capture_full_page_screenshot(driver, f"{test_name}_Login_Unconfirmed")
                raise Exception(f"Login success not confirmed. Current URL: {current_url}")

        # Additional verification: Check user session/authentication status
        try:
            user_indicators = driver.find_elements(By.XPATH,
                                                   "//span[@class='ant-avatar ant-avatar-circle ant-avatar-icon border-2 border-gray-200 cursor-pointer css-1k708as']")
            if user_indicators:
                logging.info("User authentication indicators found - login confirmed")
        except Exception as e:
            logging.warning(f"Additional authentication verification failed: {e}")

        logging.info(f"Login completed successfully for user: {login_data['email']}")
        return True

    except Exception as e:
        logging.error(f"Login validation failed: {e}")
        capture_full_page_screenshot(driver, f"{test_name}_Validation_Exception")
        raise Exception(f"Login validation failed: {e}")