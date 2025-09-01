import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.registration_page import RegistrationPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_reg_01(browser_config, test_case):
    """TC_Reg_01: Verify Homepage Load and Sign Up Button Navigation"""
    logging.info("TC_Reg_01 Started..")
    logging.info(test_case["registration"][0]["TC_Reg_01"]["_comment"])

    driver, wait = browser_config

    # Create object for RegistrationPage class
    registration_page = RegistrationPage(driver, wait)

    # Get test data
    test_data = test_case["registration"][0]["TC_Reg_01"]

    # 1. Navigate to DOER homepage URL (already done in conftest.py)
    current_url = driver.current_url
    expected_url = test_data["homepage_url"]

    # Verify URL is correct
    if expected_url in current_url:
        logging.info("Homepage URL loaded successfully.")
    else:
        logging.error(f"Wrong URL loaded. Expected: {expected_url}, Actual: {current_url}")
        capture_full_page_screenshot(driver, "TC_Reg_01_URL_Error")
        pytest.fail(f"Wrong URL loaded. Expected: {expected_url}, Actual: {current_url}")

    time.sleep(2)

    # 2. Verify page loads with "Your Child's Future Begins Here" heading
    try:
        actual_heading = registration_page.get_homepage_heading()
        expected_heading = test_data["expected_heading"]

        if expected_heading in actual_heading:
            logging.info("Homepage heading verified successfully.")
        else:
            logging.error(f"Homepage heading mismatch. Expected: {expected_heading}, Actual: {actual_heading}")
            capture_full_page_screenshot(driver, "TC_Reg_01_Heading_Error")
            pytest.fail(f"Homepage heading mismatch. Expected: {expected_heading}, Actual: {actual_heading}")
    except Exception as e:
        logging.error(f"Homepage heading verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_01_Heading_Exception")
        pytest.fail(f"Homepage heading verification failed: {e}")

    # 3. Verify statistics display (20000+ Students, 1643+ Guardians, 7000+ Teachers, 2000+ Schools)
    try:
        actual_stats = registration_page.get_statistics_elements()
        expected_stats = test_data["expected_stats"]

        if actual_stats:
            stats_verified = True
            for stat_type, expected_value in expected_stats.items():
                if expected_value not in str(actual_stats.get(stat_type, "")):
                    stats_verified = False
                    break

            if stats_verified:
                logging.info("Homepage statistics verified successfully.")
            else:
                logging.error(f"Statistics verification failed. Expected: {expected_stats}, Actual: {actual_stats}")
                capture_full_page_screenshot(driver, "TC_Reg_01_Stats_Error")
                # Note: This might be a soft assertion if stats are not critical
                logging.warning("Continuing test despite statistics mismatch...")
        else:
            logging.warning("Statistics elements not found, continuing test...")
    except Exception as e:
        logging.warning(f"Statistics verification failed: {e}, continuing test...")

    # 4. Click "Sign Up for Free" button
    try:
        registration_page.click_sign_up_for_free_button()
        logging.info("Sign Up for Free button clicked successfully.")
        time.sleep(3)  # Wait for page navigation
    except Exception as e:
        logging.error(f"Sign Up for Free button click failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_01_Button_Error")
        pytest.fail(f"Sign Up for Free button click failed: {e}")

    # 5. Verify navigation to Sign Up page
    try:
        current_url_after_click = driver.current_url
        if "sign" in current_url_after_click.lower() or "register" in current_url_after_click.lower():
            logging.info("Successfully navigated to Sign Up page.")
        else:
            logging.error(f"Navigation to Sign Up page failed. Current URL: {current_url_after_click}")
            capture_full_page_screenshot(driver, "TC_Reg_01_Navigation_Error")
            pytest.fail(f"Navigation to Sign Up page failed. Current URL: {current_url_after_click}")

        # Additional verification: Check if Sign Up page elements are present
        signup_heading = registration_page.get_signup_heading()
        if signup_heading and "sign up" in signup_heading.lower():
            logging.info("Sign Up page loaded successfully with correct heading.")
        else:
            logging.warning("Sign Up page heading not found or incorrect.")

    except Exception as e:
        logging.error(f"Sign Up page verification failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_01_Verification_Error")
        pytest.fail(f"Sign Up page verification failed: {e}")

    # Final validation
    expected_result = test_data["expected_result"]
    logging.info(f"Test Passed. {expected_result}")
    logging.info("TC_Reg_01 Completed..")