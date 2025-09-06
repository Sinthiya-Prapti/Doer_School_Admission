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

        # 1. Click "Apply Now" button on any admission card
        try:
            admission_portal_page.click_apply_now_button()
            logging.info("Apply Now button clicked successfully.")
            time.sleep(3)  # Wait for navigation
        except Exception as e:
            logging.error(f"Failed to click Apply Now button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_07_apply_now_error")
            pytest.fail(f"Test Failed. Failed to click Apply Now button: {str(e)}")

        # 2. Verify navigation to Student Information form
        expected_result = test_case["admission_portal"][6]["TC_AD_07"]["expected_result"]

        try:
            student_form_loaded = admission_portal_page.is_student_information_form_loaded()

            if student_form_loaded:
                logging.info(f"Test Passed. {expected_result}")
                logging.info("✅ Successfully navigated to Student Information form.")
            else:
                # Additional check: verify URL contains expected path
                current_url = driver.current_url
                if "student" in current_url.lower() or "information" in current_url.lower() or "form" in current_url.lower():
                    logging.info("Navigation successful based on URL check.")
                    logging.info(f"Current URL: {current_url}")
                else:
                    logging.error("Navigation to Student Information form failed.")
                    logging.error(f"Current URL: {current_url}")
                    capture_full_page_screenshot(driver, "TC_AD_07_navigation_failed")
                    pytest.fail("Test Failed. Navigation to Student Information form failed.")

        except Exception as e:
            logging.error(f"Error verifying navigation: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_07_verification_error")
            pytest.fail(f"Test Failed. Error verifying navigation: {str(e)}")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_07_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_07 Completed..")