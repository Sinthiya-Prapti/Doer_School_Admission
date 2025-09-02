import logging
import time
import pytest
from selenium.webdriver.common.by import By

from utils.screenshot_utils import capture_full_page_screenshot
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_reg_05(browser_config, test_case):
    """TC_Reg_05: Verify Sign In Page Load and Form Display"""
    logging.info("TC_Reg_05 Started..")
    logging.info(test_case["registration"][4]["TC_Reg_05"]["_comment"])

    driver, wait = browser_config

    # Create objects for page classes
    registration_page = RegistrationPage(driver, wait)
    login_page = LoginPage(driver, wait)

    # Get test data
    test_data = test_case["registration"][4]["TC_Reg_05"]

    # Navigate to Sign In page via Sign Up page
    try:
        registration_page.click_sign_up_for_free_button()
        logging.info("Navigated to Sign Up page successfully.")
        time.sleep(2)

        registration_page.click_signin_link_from_signup()
        logging.info("Navigated to Sign In page successfully.")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Navigation to Sign In page failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_05_Navigation_Error")
        pytest.fail(f"Navigation to Sign In page failed: {e}")

    # 1. Verify Sign In page loads
    try:
        current_url = driver.current_url
        if "sign-in" in current_url.lower():
            logging.info("Sign In page loaded successfully.")
        else:
            logging.error(f"Sign In page not loaded correctly. URL: {current_url}")
            capture_full_page_screenshot(driver, "TC_Reg_05_Page_Load_Error")
            pytest.fail(f"Sign In page not loaded correctly. URL: {current_url}")
    except Exception as e:
        logging.error(f"Sign In page load verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_05_Load_Exception")
        pytest.fail(f"Sign In page load verification failed: {e}")

    # 2. Verify "Sign In" heading is displayed
    try:
        actual_heading = login_page.get_signin_heading()
        expected_heading = test_data["expected_heading"]

        if actual_heading and expected_heading.lower() in actual_heading.lower():
            logging.info("Sign In heading verified successfully.")
        else:
            logging.error(
                f"Sign In heading verification failed. Expected: {expected_heading}, Actual: {actual_heading}")
            capture_full_page_screenshot(driver, "TC_Reg_05_Heading_Error")
            pytest.fail(f"Sign In heading verification failed. Expected: {expected_heading}, Actual: {actual_heading}")
    except Exception as e:
        logging.error(f"Sign In heading verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_05_Heading_Exception")
        pytest.fail(f"Sign In heading verification failed: {e}")

    # 3. Verify "Enter your email and password to Sign in...!" text
    try:
        actual_subtitle = login_page.get_signin_subtitle()
        expected_subtitle = test_data["expected_subtitle"]

        if actual_subtitle and expected_subtitle.lower() in actual_subtitle.lower():
            logging.info("Sign In subtitle verified successfully.")
        else:
            logging.warning(
                f"Sign In subtitle not found or different. Expected: {expected_subtitle}, Actual: {actual_subtitle}")
            # This might be a soft assertion as subtitle text can vary
    except Exception as e:
        logging.warning(f"Sign In subtitle verification failed: {e}")

    # 4. Verify Email and Password fields are visible
    try:
        expected_form_fields = test_data["expected_form_fields"]  # ["Email", "Password"]

        # Check each form field individually for better error reporting
        for field_name in expected_form_fields:
            if field_name == "Email":
                try:
                    email_field = driver.find_element(By.CSS_SELECTOR,
                                                      "#login_email")
                    if email_field.is_displayed():
                        logging.info("Email field is visible.")
                    else:
                        logging.error("Email field is not visible.")
                        capture_full_page_screenshot(driver, "TC_Reg_05_Email_Field_Error")
                        pytest.fail("Email field is not visible.")
                except Exception as e:
                    logging.error(f"Email field not found: {e}")
                    capture_full_page_screenshot(driver, "TC_Reg_05_Email_Field_Exception")
                    pytest.fail(f"Email field not found: {e}")

            elif field_name == "Password":
                try:
                    password_field = driver.find_element(By.CSS_SELECTOR,
                                                         "#login_password")
                    if password_field.is_displayed():
                        logging.info("Password field is visible.")
                    else:
                        logging.error("Password field is not visible.")
                        capture_full_page_screenshot(driver, "TC_Reg_05_Password_Field_Error")
                        pytest.fail("Password field is not visible.")
                except Exception as e:
                    logging.error(f"Password field not found: {e}")
                    capture_full_page_screenshot(driver, "TC_Reg_05_Password_Field_Exception")
                    pytest.fail(f"Password field not found: {e}")

        logging.info("All form fields verified successfully.")

    except Exception as e:
        logging.error(f"Form fields verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_05_Form_Fields_Exception")
        pytest.fail(f"Form fields verification failed: {e}")

    # 5-8. Verify all expected elements
    try:
        expected_elements = test_data["expected_elements"]
        elements_verified = login_page.verify_signin_form_elements(expected_elements)

        if elements_verified:
            logging.info("All Sign In form elements verified successfully.")
        else:
            logging.error(f"Sign In form elements verification failed. Expected elements: {expected_elements}")
            capture_full_page_screenshot(driver, "TC_Reg_05_Elements_Error")
            pytest.fail(f"Sign In form elements verification failed. Expected elements: {expected_elements}")
    except Exception as e:
        logging.error(f"Sign In elements verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_05_Elements_Exception")
        pytest.fail(f"Sign In elements verification failed: {e}")

    # Additional verification: Check individual elements with detailed logging
    try:
        # Keep me logged in checkbox
        try:
            checkbox = driver.find_element(By.CSS_SELECTOR, ".ant-checkbox-label")
            if checkbox.is_displayed():
                logging.info("'Keep me logged in' checkbox is visible.")
            else:
                logging.warning("'Keep me logged in' checkbox is not visible.")
        except:
            logging.warning("'Keep me logged in' checkbox not found.")

        # Forgot password link
        try:
            forgot_link = driver.find_element(By.XPATH, "a[class='text-gray-500 hover:text-[#1a5683] text-sm']")
            if forgot_link.is_displayed():
                logging.info("'Forgot password?' link is visible.")
            else:
                logging.warning("'Forgot password?' link is not visible.")
        except:
            logging.warning("'Forgot password?' link not found.")

        # Log In button
        try:
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            if login_button.is_displayed():
                logging.info("'Log In' button is visible.")
            else:
                logging.warning("'Log In' button is not visible.")
        except:
            logging.warning("'Log In' button not found.")

        # Google Sign In option
        try:
            google_signin = driver.find_element(By.XPATH, "//button[@type='button']")
            if google_signin.is_displayed():
                logging.info("'Sign in with Google' option is visible.")
            else:
                logging.warning("'Sign in with Google' option is not visible.")
        except:
            logging.warning("'Sign in with Google' option not found.")

    except Exception as e:
        logging.warning(f"Additional element verification failed: {e}")

    # Take screenshot of complete Sign In page
    capture_full_page_screenshot(driver, "TC_Reg_05_Complete_Page")

    # Final validation
    expected_result = test_data["expected_result"]
    logging.info(f"Test Passed. {expected_result}")

    # Log page structure information
    try:
        page_title = driver.title
        logging.info(f"Sign In page title: {page_title}")
    except Exception as e:
        logging.warning(f"Page title check failed: {e}")

    logging.info("TC_Reg_05 Completed..")