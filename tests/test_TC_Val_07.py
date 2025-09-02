import logging
import time
import pytest
from selenium.webdriver.common.by import By

from utils.screenshot_utils import capture_full_page_screenshot
from utils.bug_report_template import generate_bug_report, save_bug_report
from pages.registration_page import RegistrationPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_val_07(browser_config, test_case):
    """TC_Val_07: Verify registration fails with mismatched passwords"""
    logging.info("TC_Val_07 Started..")
    logging.info(test_case["validation_cases"][6]["TC_Val_07"]["_comment"])

    driver, wait = browser_config

    # Create object for RegistrationPage class
    registration_page = RegistrationPage(driver, wait)

    # Get test data
    test_data = test_case["validation_cases"][6]["TC_Val_07"]

    # Navigate to Sign Up page
    try:
        registration_page.click_sign_up_for_free_button()
        logging.info("Navigated to Sign Up page successfully.")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Navigation to Sign Up page failed: {e}")
        capture_full_page_screenshot(driver, "TC_Val_07_Navigation_Error")
        pytest.fail(f"Navigation to Sign Up page failed: {e}")

    # 1. Enter valid value of Full Name
    try:
        registration_page.enter_full_name(test_data["fullname"])
        logging.info("Valid Full Name entered successfully.")
    except Exception as e:
        logging.error(f"Full Name entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Val_07_FullName_Error")
        pytest.fail(f"Full Name entry failed: {e}")

    # 2. Enter valid value of Email
    try:
        registration_page.enter_email(test_data["email"])
        logging.info("Valid Email entered successfully.")
    except Exception as e:
        logging.error(f"Email entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Val_07_Email_Error")
        pytest.fail(f"Email entry failed: {e}")

    # 3. Enter Password
    try:
        registration_page.enter_password(test_data["password"])
        logging.info(f"Password '{test_data['password']}' entered successfully.")
    except Exception as e:
        logging.error(f"Password entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Val_07_Password_Error")
        pytest.fail(f"Password entry failed: {e}")

    # 4. Enter DIFFERENT Confirm Password
    try:
        registration_page.enter_confirm_password(test_data["confirm_password"])
        logging.info(f"Mismatched Confirm Password '{test_data['confirm_password']}' entered successfully.")
    except Exception as e:
        logging.error(f"Confirm Password entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Val_07_ConfirmPassword_Error")
        pytest.fail(f"Confirm Password entry failed: {e}")

    # Take screenshot before validation attempt
    capture_full_page_screenshot(driver, "TC_Val_07_Before_Submit")

    # 5. Click on the "Sign Up" button
    try:
        registration_page.click_signup_button()
        logging.info("Sign Up button clicked successfully.")
        time.sleep(2)  # Wait for validation message
    except Exception as e:
        logging.error(f"Sign Up button click failed: {e}")
        capture_full_page_screenshot(driver, "TC_Val_07_Submit_Error")
        pytest.fail(f"Sign Up button click failed: {e}")

    # Validate Error Message for password mismatch
    try:
        expected_error_message = test_data["expected_result"]

        # Try to get validation message from confirm password field first
        actual_error_message = registration_page.get_validation_error_message("ConfirmPassword")

        # If no validation message from confirm password field, check for general form errors
        if not actual_error_message:
            # Look for custom password mismatch messages
            try:
                password_error_elements = driver.find_elements(By.CSS_SELECTOR,
                                                               ".password-error, .password-mismatch, .error-message, .alert-danger")

                for element in password_error_elements:
                    if element.is_displayed() and element.text.strip():
                        actual_error_message = element.text.strip()
                        break

                if not actual_error_message:
                    # Check for JavaScript custom validation
                    actual_error_message = driver.execute_script("""
                        var confirmField = document.querySelector('input[name="confirmPassword"], input[placeholder*="Confirm"]');
                        if (confirmField) {
                            return confirmField.validationMessage || confirmField.title || '';
                        }
                        return '';
                    """)

            except Exception as e:
                logging.warning(f"Custom error message search failed: {e}")

        # Validation logic
        if actual_error_message and expected_error_message.lower() in actual_error_message.lower():
            logging.info("Test Passed. Expected Error Message matches with Actual Error Message.")
            logging.info(f"Expected: {expected_error_message}")
            logging.info(f"Actual: {actual_error_message}")
        else:
            logging.error("Test Failed. Expected Error Message does not match with Actual Error Message.")
            logging.error(f"Expected: {expected_error_message}")
            logging.error(f"Actual: {actual_error_message}")

            # Take screenshot of failure
            screenshot_path = capture_full_page_screenshot(driver, "TC_Val_07_Validation_Error")

            # Generate bug report
            bug_report = generate_bug_report(
                test_case=test_data,
                actual_message=actual_error_message,
                expected_message=expected_error_message,
                screenshot_path=screenshot_path,
                test_case_name="TC_Val_07"
            )

            # Save bug report
            save_bug_report(bug_report, "TC_Val_07")

            pytest.fail("Test Failed. Expected Error Message does not match with Actual Error Message.")

    except Exception as e:
        logging.error(f"Error message validation failed: {e}")
        capture_full_page_screenshot(driver, "TC_Val_07_Exception")
        pytest.fail(f"Error message validation failed: {e}")

    # Additional validation: Ensure registration did not proceed
    try:
        current_url = driver.current_url
        if "/en" == current_url.lower():
            logging.error("Registration unexpectedly succeeded with mismatched passwords")
            capture_full_page_screenshot(driver, "TC_Val_07_Unexpected_Success")
            pytest.fail("Registration unexpectedly succeeded with mismatched passwords")
        else:
            logging.info("Registration correctly prevented with mismatched passwords")
    except Exception as e:
        logging.warning(f"Additional validation failed: {e}")


    # Log test completion details
    logging.info(f"Password mismatch test completed:")
    logging.info(f"Password: {test_data['password']}")
    logging.info(f"Confirm Password: {test_data['confirm_password']}")
    logging.info("Registration correctly rejected due to password mismatch.")

    logging.info("TC_Val_07 Completed..")