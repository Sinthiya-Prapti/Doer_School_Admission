import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_reg_12(browser_config, test_case):
    """TC_Reg_12: Verify Password Visibility Toggle"""
    logging.info("TC_Reg_12 Started..")
    logging.info(test_case["registration"][11]["TC_Reg_12"]["_comment"])

    driver, wait = browser_config

    # Create objects for page classes
    registration_page = RegistrationPage(driver, wait)
    login_page = LoginPage(driver, wait)

    # Get test data
    test_data = test_case["registration"][11]["TC_Reg_12"]

    # Navigate to Sign Up page first, then to Sign In page
    try:
        registration_page.click_sign_up_for_free_button()
        logging.info("Navigated to Sign Up page successfully.")
        time.sleep(2)

        # Navigate to Sign In page where password toggle is more common
        registration_page.click_signin_link_from_signup()
        logging.info("Navigated to Sign In page successfully.")
        time.sleep(2)
    except Exception as e:
        logging.error(f"Navigation to Sign In page failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_12_Navigation_Error")
        pytest.fail(f"Navigation to Sign In page failed: {e}")

    # 1. Enter password in password field
    try:
        login_page.enter_password(test_data["password"])
        logging.info("Password entered successfully.")
        time.sleep(1)
    except Exception as e:
        logging.error(f"Password entry failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_12_Password_Error")
        pytest.fail(f"Password entry failed: {e}")

    # Take screenshot before toggle
    capture_full_page_screenshot(driver, "TC_Reg_12_Before_Toggle")

    # 2. Get initial password field type (should be 'password')
    try:
        initial_field_type = login_page.get_password_field_type()
        if initial_field_type == "password":
            logging.info("Password field initially hidden (type='password').")
        else:
            logging.warning(f"Password field type unexpected: {initial_field_type}")
    except Exception as e:
        logging.error(f"Getting initial password field type failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_12_InitialType_Error")
        pytest.fail(f"Getting initial password field type failed: {e}")

    # 3. Click eye icon (👁) to show password
    try:
        login_page.click_password_visibility_view()
        logging.info("Password visibility toggle clicked successfully.")
        time.sleep(1)  # Wait for toggle effect
    except Exception as e:
        logging.error(f"Password visibility toggle click failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_12_Toggle_Error")
        pytest.fail(f"Password visibility toggle click failed: {e}")

    # 4. Verify password visibility changes (should become 'text')
    try:
        toggled_field_type = login_page.get_password_field_type()
        if toggled_field_type == "text":
            logging.info("Password is now visible (type='text').")
        else:
            logging.error(f"Password visibility toggle failed. Field type: {toggled_field_type}")
            capture_full_page_screenshot(driver, "TC_Reg_12_Toggle_Failed")
            pytest.fail(f"Password visibility toggle failed. Field type: {toggled_field_type}")
    except Exception as e:
        logging.error(f"Password visibility verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_12_Verification_Error")
        pytest.fail(f"Password visibility verification failed: {e}")

    # Take screenshot after first toggle
    capture_full_page_screenshot(driver, "TC_Reg_12_After_First_Toggle")

    # 5. Click eye icon again to hide password
    try:
        login_page.click_password_visibility_hide()
        logging.info("Password visibility toggle clicked again successfully.")
        time.sleep(1)  # Wait for toggle effect
    except Exception as e:
        logging.error(f"Second password visibility toggle click failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_12_Second_Toggle_Error")
        pytest.fail(f"Second password visibility toggle click failed: {e}")

    # 6. Verify password is hidden again (should be 'password')
    try:
        final_field_type = login_page.get_password_field_type()
        if final_field_type == "password":
            logging.info("Password is hidden again (type='password').")
        else:
            logging.error(f"Password hide toggle failed. Field type: {final_field_type}")
            capture_full_page_screenshot(driver, "TC_Reg_12_Hide_Failed")
            pytest.fail(f"Password hide toggle failed. Field type: {final_field_type}")
    except Exception as e:
        logging.error(f"Password hide verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_12_Hide_Verification_Error")
        pytest.fail(f"Password hide verification failed: {e}")

    # Take final screenshot
    capture_full_page_screenshot(driver, "TC_Reg_12_Final_State")

    # Final validation
    expected_result = test_data["expected_result"]

    # Verify complete toggle functionality
    if (initial_field_type == "password" and
            toggled_field_type == "text" and
            final_field_type == "password"):
        logging.info(f"Test Passed. {expected_result}")
        logging.info("Password visibility toggle functionality working correctly.")
    else:
        logging.error("Password toggle functionality incomplete.")
        pytest.fail("Password toggle functionality incomplete.")

    # Log test completion details
    logging.info(f"Password toggle test completed with password: {test_data['password'][:3]}***")
    logging.info("TC_Reg_12 Completed..")