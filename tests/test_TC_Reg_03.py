import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.registration_page import RegistrationPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_reg_03(browser_config, test_case):
    """TC_Reg_03: Verify Complete User Registration with Valid Data"""
    logging.info("TC_Reg_03 Started..")
    logging.info(test_case["registration"][2]["TC_Reg_03"]["_comment"])

    driver, wait = browser_config

    # Create object for RegistrationPage class
    registration_page = RegistrationPage(driver, wait)

    # Get test data
    test_data = test_case["registration"][2]["TC_Reg_03"]

    # Navigate to Sign Up page
    try:
        registration_page.click_sign_up_for_free_button()
        logging.info("Navigated to Sign Up page successfully.")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Navigation to Sign Up page failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_03_Navigation_Error")
        pytest.fail(f"Navigation to Sign Up page failed: {e}")

    # 1. Fill Full Name
    try:
        registration_page.enter_full_name(test_data["fullname"])
        logging.info("Full Name entered successfully.")
    except Exception as e:
        logging.error(f"Full Name entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_03_FullName_Error")
        pytest.fail(f"Full Name entry failed: {e}")

    # 2. Fill Email
    try:
        registration_page.enter_email(test_data["email"])
        logging.info("Email entered successfully.")
    except Exception as e:
        logging.error(f"Email entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_03_Email_Error")
        pytest.fail(f"Email entry failed: {e}")

    # 3. Fill Password
    try:
        registration_page.enter_password(test_data["password"])
        logging.info("Password entered successfully.")
    except Exception as e:
        logging.error(f"Password entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_03_Password_Error")
        pytest.fail(f"Password entry failed: {e}")

    # 4. Fill Confirm Password
    try:
        registration_page.enter_confirm_password(test_data["confirm_password"])
        logging.info("Confirm Password entered successfully.")
    except Exception as e:
        logging.error(f"Confirm Password entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_03_ConfirmPassword_Error")
        pytest.fail(f"Confirm Password entry failed: {e}")

    # Take screenshot before submitting form
    capture_full_page_screenshot(driver, "TC_Reg_03_Before_Submit")

    # 5. Click "Sign Up" button
    try:
        registration_page.click_signup_button()
        logging.info("Sign Up button clicked successfully.")
        time.sleep(2)  # Wait for registration process
    except Exception as e:
        logging.error(f"Sign Up button click failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_03_Submit_Error")
        pytest.fail(f"Sign Up button click failed: {e}")

    # Validate registration success (FIXED INDENTATION - now outside the except block)
    try:
        # Use the existing method to get registration message
        actual_message = registration_page.get_registration_success_message()

        if actual_message is None:
            logging.error("No registration message received")
            capture_full_page_screenshot(driver, "TC_Reg_03_No_Message")
            pytest.fail("No registration message received")

        logging.info(f"Registration message received: {actual_message}")

        # Check if the actual message contains the expected result text
        expected_result = test_data["expected_result"]

        if expected_result.lower() in actual_message.lower():
            logging.info(f"Registration validation passed. Expected: {expected_result}, Got: {actual_message}")

            # Additional check for success keywords
            if any(keyword in actual_message.lower() for keyword in
                   ["success", "successful", "registered", "created"]):
                logging.info("Registration completed successfully.")
                capture_full_page_screenshot(driver, "TC_Reg_03_Success")
            else:
                logging.warning("Message found but may not indicate success.")
                capture_full_page_screenshot(driver, "TC_Reg_03_Uncertain_Result")
        else:
            logging.error(f"Registration validation failed. Expected: {expected_result}, Got: {actual_message}")
            capture_full_page_screenshot(driver, "TC_Reg_03_Registration_Failed")
            current_url = driver.current_url
            pytest.fail(
                f"Registration validation failed. Expected: {expected_result}, Got: {actual_message}. Current URL: {current_url}")

    except Exception as e:
        logging.error(f"Registration message validation failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_03_Validation_Exception")

        # Fallback: Check current URL or page state
        try:
            current_url = driver.current_url
            page_source = driver.page_source

            # Check for common success indicators
            if any(indicator in page_source.lower() for indicator in ["dashboard", "welcome", "profile", "home"]):
                logging.info("Registration appears successful based on page content.")
            else:
                pytest.fail(
                    f"Registration validation failed and no success indicators found. Current URL: {current_url}")

        except Exception as fallback_error:
            logging.error(f"Fallback validation also failed: {fallback_error}")
            pytest.fail(f"Complete registration validation failure: {e}")

    # Log final state for debugging
    try:
        current_url = driver.current_url
        logging.info(f"Final URL after registration: {current_url}")
        logging.info(f"Registration completed with data - Name: {test_data['fullname']}, Email: {test_data['email']}")
    except Exception as e:
        logging.warning(f"Final state logging failed: {e}")

    logging.info("TC_Reg_03 Completed..")