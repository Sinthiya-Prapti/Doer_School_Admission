import logging
import time
import pytest
from selenium.webdriver.common.by import By

from utils.screenshot_utils import capture_full_page_screenshot
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_reg_06(browser_config, test_case):
    """TC_Reg_06: Verify User Login with Valid Credentials"""
    logging.info("TC_Reg_06 Started..")
    logging.info(test_case["registration"][5]["TC_Reg_06"]["_comment"])

    driver, wait = browser_config

    # Create objects for page classes
    registration_page = RegistrationPage(driver, wait)
    login_page = LoginPage(driver, wait)

    # Get test data
    test_data = test_case["registration"][5]["TC_Reg_06"]

    # Navigate to Sign Up page first, then to Sign In page
    try:
        registration_page.click_sign_up_for_free_button()
        logging.info("Navigated to Sign Up page successfully.")
        time.sleep(2)

        # Navigate to Sign In page
        registration_page.click_signin_link_from_signup()
        logging.info("Navigated to Sign In page successfully.")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Navigation to Sign In page failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_06_Navigation_Error")
        pytest.fail(f"Navigation to Sign In page failed: {e}")

    # Verify we're on Sign In page
    try:
        current_url = driver.current_url
        signin_heading = login_page.get_signin_heading()

        if signin_heading and "sign in" in signin_heading.lower():
            logging.info("Sign In page loaded successfully.")
        else:
            logging.error(f"Sign In page not loaded correctly. Heading: {signin_heading}")
            capture_full_page_screenshot(driver, "TC_Reg_06_Page_Load_Error")
            pytest.fail(f"Sign In page not loaded correctly. Heading: {signin_heading}")
    except Exception as e:
        logging.error(f"Sign In page verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_06_Verification_Error")
        pytest.fail(f"Sign In page verification failed: {e}")

    # 1. Fill Email (from previous registration)
    try:
        login_page.enter_email(test_data["email"])
        logging.info("Email entered successfully in login form.")
    except Exception as e:
        logging.error(f"Email entry failed in login form: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_06_Email_Error")
        pytest.fail(f"Email entry failed in login form: {e}")

    # 2. Fill Password
    try:
        login_page.enter_password(test_data["password"])
        logging.info("Password entered successfully in login form.")
    except Exception as e:
        logging.error(f"Password entry failed in login form: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_06_Password_Error")
        pytest.fail(f"Password entry failed in login form: {e}")

    # Take screenshot before login attempt
    capture_full_page_screenshot(driver, "TC_Reg_06_Before_Login")

    # 3. Click "Log In" button
    try:
        login_page.click_login_button()
        logging.info("Log In button clicked successfully.")
        time.sleep(2)  # Wait for login process
    except Exception as e:
        logging.error(f"Log In button click failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_06_Login_Button_Error")
        pytest.fail(f"Log In button click failed: {e}")

    # Validate login success
    try:
        # Check for success indicators
        current_url = driver.current_url
        success_message = login_page.get_login_success_message()

        login_successful = False

        # Check for success message
        if "Login successful!" in success_message:
            # Take screenshot of success state
            capture_full_page_screenshot(driver, "TC_Reg_06_Login_Success")
            logging.info(f"Login success message found: {success_message}")
            login_successful = True



        # Check URL redirection
        elif ("/en" in current_url.lower() or
              "/en/profile" in current_url.lower() or
              "portal" in current_url.lower() or
              "home" in current_url.lower()):
            # Take screenshot of success state
            capture_full_page_screenshot(driver, "TC_Reg_06_Login_Success")
            logging.info(f"Login successful - redirected to: {current_url}")
            login_successful = True

        # Check if we're no longer on login page
        elif "sign-in" not in current_url.lower():
            # Take screenshot of success state
            capture_full_page_screenshot(driver, "TC_Reg_06_Login_Success")
            logging.info("Login successful - no longer on login page")
            login_successful = True

        if not login_successful:
            # Check for error messages
            error_message = login_page.get_login_error_message()
            if error_message:
                logging.error(f"Login failed with error: {error_message}")
                capture_full_page_screenshot(driver, "TC_Reg_06_Login_Error")
                pytest.fail(f"Login failed with error: {error_message}")
            else:
                logging.error(f"Login success not confirmed. Current URL: {current_url}")
                capture_full_page_screenshot(driver, "TC_Reg_06_Login_Unconfirmed")

                # Additional check for any visible error elements
                try:
                    error_elements = driver.find_elements(By.CSS_SELECTOR, ".error, .alert-danger, .login-error")
                    if error_elements and error_elements[0].is_displayed():
                        error_text = error_elements[0].text
                        logging.error(f"Login failed with visible error: {error_text}")
                        pytest.fail(f"Login failed with visible error: {error_text}")
                except:
                    pass

                pytest.fail(f"Login success not confirmed. Current URL: {current_url}")



        # Verify expected result
        expected_result = test_data["expected_result"]
        logging.info(f"Test Passed. {expected_result}")

        # Log final state
        final_url = driver.current_url
        logging.info(f"Final URL after login: {final_url}")

    except Exception as e:
        logging.error(f"Login validation failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_06_Validation_Exception")
        pytest.fail(f"Login validation failed: {e}")

    # Additional verification: Check user session/authentication status
    try:
        # Look for user indicators (profile menu, logout button, etc.)
        user_indicators = driver.find_elements(By.XPATH,
                                               "//span[@class='ant-avatar ant-avatar-circle ant-avatar-icon border-2 border-gray-200 cursor-pointer css-1k708as']")
        if user_indicators:
            logging.info("User authentication indicators found - login confirmed")

        # Log login attempt details (without password)
        logging.info(f"Login completed for user: {test_data['email']}")

    except Exception as e:
        logging.warning(f"Additional authentication verification failed: {e}")

    logging.info("TC_Reg_06 Completed..")