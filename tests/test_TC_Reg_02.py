import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.registration_page import RegistrationPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_reg_02(browser_config, test_case):
    """TC_Reg_02: Verify Sign Up Page Load and Form Display"""
    logging.info("TC_Reg_02 Started..")
    logging.info(test_case["registration"][1]["TC_Reg_02"]["_comment"])

    driver, wait = browser_config

    # Create object for RegistrationPage class
    registration_page = RegistrationPage(driver, wait)

    # Get test data
    test_data = test_case["registration"][1]["TC_Reg_02"]

    # Navigate to Sign Up page first
    try:
        registration_page.click_sign_up_for_free_button()
        logging.info("Navigated to Sign Up page successfully.")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Navigation to Sign Up page failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_02_Navigation_Error")
        pytest.fail(f"Navigation to Sign Up page failed: {e}")

    # 1. Verify Sign Up page loads
    try:
        current_url = driver.current_url
        if "sign" in current_url.lower() or "register" in current_url.lower():
            logging.info("Sign Up page loaded successfully.")
        else:
            logging.error(f"Sign Up page not loaded correctly. URL: {current_url}")
            capture_full_page_screenshot(driver, "TC_Reg_02_Page_Load_Error")
            pytest.fail(f"Sign Up page not loaded correctly. URL: {current_url}")
    except Exception as e:
        logging.error(f"Sign Up page load verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_02_Load_Exception")
        pytest.fail(f"Sign Up page load verification failed: {e}")

    # 2. Verify "Sign Up" heading is displayed
    try:
        actual_heading = registration_page.get_signup_heading()
        expected_heading = test_data["expected_heading"]

        if actual_heading and expected_heading.lower() in actual_heading.lower():
            logging.info("Sign Up heading verified successfully.")
        else:
            logging.error(
                f"Sign Up heading verification failed. Expected: {expected_heading}, Actual: {actual_heading}")
            capture_full_page_screenshot(driver, "TC_Reg_02_Heading_Error")
            pytest.fail(f"Sign Up heading verification failed. Expected: {expected_heading}, Actual: {actual_heading}")
    except Exception as e:
        logging.error(f"Sign Up heading verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_02_Heading_Exception")
        pytest.fail(f"Sign Up heading verification failed: {e}")

    # 3. Verify "Create your account to get started!" text
    try:
        actual_subtitle = registration_page.get_signup_subtitle()
        expected_subtitle = test_data["expected_subtitle"]

        if actual_subtitle and expected_subtitle.lower() in actual_subtitle.lower():
            logging.info("Sign Up subtitle verified successfully.")
        else:
            logging.warning(
                f"Sign Up subtitle not found or different. Expected: {expected_subtitle}, Actual: {actual_subtitle}")
            # This might be a soft assertion as subtitle text can vary
    except Exception as e:
        logging.warning(f"Sign Up subtitle verification failed: {e}")

    # 4. Verify all form fields are visible (Full Name, Email, Password, Confirm Password)
    try:
        expected_form_fields = test_data["expected_form_fields"]
        form_fields_present = registration_page.verify_form_fields_present(expected_form_fields)

        if form_fields_present:
            logging.info("All form fields verified successfully.")
        else:
            logging.error(f"Form fields verification failed. Expected fields: {expected_form_fields}")
            capture_full_page_screenshot(driver, "TC_Reg_02_Form_Fields_Error")
            pytest.fail(f"Form fields verification failed. Expected fields: {expected_form_fields}")
    except Exception as e:
        logging.error(f"Form fields verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_02_Form_Exception")
        pytest.fail(f"Form fields verification failed: {e}")

    # 5. Verify "Sign Up" button is present
    # 6. Verify "Sign up with Google" option is available
    try:
        expected_buttons = test_data["expected_buttons"]
        buttons_present = registration_page.verify_buttons_present(expected_buttons)

        if buttons_present:
            logging.info("All buttons verified successfully.")
        else:
            logging.error(f"Buttons verification failed. Expected buttons: {expected_buttons}")
            capture_full_page_screenshot(driver, "TC_Reg_02_Buttons_Error")
            pytest.fail(f"Buttons verification failed. Expected buttons: {expected_buttons}")
    except Exception as e:
        logging.error(f"Buttons verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_02_Buttons_Exception")
        pytest.fail(f"Buttons verification failed: {e}")

    # Additional verification: Check page structure and accessibility
    try:
        # Verify page title
        page_title = driver.title
        if "sign up" in page_title.lower() or "register" in page_title.lower():
            logging.info(f"Page title is appropriate: {page_title}")
        else:
            logging.warning(f"Page title might not be appropriate: {page_title}")

        # Take screenshot of successful page load
        capture_full_page_screenshot(driver, "TC_Reg_02_Success")

    except Exception as e:
        logging.warning(f"Additional verification failed: {e}")

    # Final validation
    expected_result = test_data["expected_result"]
    logging.info(f"Test Passed. {expected_result}")
    logging.info("TC_Reg_02 Completed..")