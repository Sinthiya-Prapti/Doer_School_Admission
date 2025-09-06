import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.admission_portal_page import AdmissionPortalPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data_admission.json"))
def test_tc_ad_07(browser_config, test_case):
    logging.info("TC_AD_07 Started..")
    logging.info(test_case["admission_portal"][6]["TC_AD_07"]["_comment"])

    driver, wait = browser_config
    # Create object for AdmissionPortalPage class
    admission_portal_page = AdmissionPortalPage(driver, wait)

    try:
        # Wait for page to load completely
        time.sleep(3)

        # goto admission page
        admission_portal_page.click_admission_navigation()

        # 1. Click "Apply Now" button on any admission card
        try:
            admission_portal_page.click_apply_now_button()
            logging.info("Apply Now button clicked successfully.")
            time.sleep(3)  # Wait for navigation
        except Exception as e:
            logging.error(f"Failed to click Apply Now button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_07_apply_now_error")
            pytest.fail(f"Test Failed. Failed to click Apply Now button: {str(e)}")

        # 2. Verify navigation to login page (for non-logged in users)
        expected_login_url = "https://admission-test.doer.school/en/sign-in"
        expected_result = test_case["admission_portal"][6]["TC_AD_07"]["expected_result"]

        try:
            current_url = driver.current_url
            logging.info(f"Current URL after clicking Apply Now: {current_url}")

            # Check if redirected to login page
            if "sign-in" in current_url:
                logging.info(f"Test Passed. {expected_result}")
                logging.info("✅ Successfully redirected to login page for non-logged in user.")
            else:
                logging.error("Navigation to login page failed.")
                logging.error(f"Expected URL: {expected_login_url}")
                logging.error(f"Current URL: {current_url}")
                capture_full_page_screenshot(driver, "TC_AD_07_login_redirect_failed")
                pytest.fail(f"Test Failed. Expected redirect to login page but got: {current_url}")

        except Exception as e:
            logging.error(f"Error verifying navigation to login page: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_07_verification_error")
            pytest.fail(f"Test Failed. Error verifying navigation: {str(e)}")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_07_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_07 Completed..")