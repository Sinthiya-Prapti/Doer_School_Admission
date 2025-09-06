import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.admission_portal_page import AdmissionPortalPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data_admission.json"))
def test_tc_ad_02(browser_config, test_case):
    logging.info("TC_AD_02 Started..")
    logging.info(test_case["admission_portal"][1]["TC_AD_02"]["_comment"])

    driver, wait = browser_config

    # Create object for AdmissionPortalPage class
    admission_portal_page = AdmissionPortalPage(driver, wait)

    try:
        # Wait for page to load completely
        time.sleep(3)

        # 1. Enter school name in search field
        school_name = test_case["admission_portal"][1]["TC_AD_02"]["school_name"]
        try:
            admission_portal_page.enter_school_name_search(school_name)
            logging.info(f"School name '{school_name}' entered successfully in search field.")
        except Exception as e:
            logging.error(f"Failed to enter school name: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_02_search_field_error")
            pytest.fail(f"Test Failed. Failed to enter school name: {str(e)}")

        # 2. Click search button
        try:
            admission_portal_page.click_search_button()
            logging.info("Search button clicked successfully.")
        except Exception as e:
            logging.error(f"Failed to click search button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_02_search_button_error")
            pytest.fail(f"Test Failed. Failed to click search button: {str(e)}")

        # 3. Verify search results
        try:
            displayed_schools = admission_portal_page.get_displayed_school_names()
            logging.info(f"Displayed schools after search: {displayed_schools}")

            # Check if all displayed schools contain the searched school name
            search_successful = True
            for school in displayed_schools:
                if school_name.lower() not in school.lower():
                    search_successful = False
                    break

            expected_result = test_case["admission_portal"][1]["TC_AD_02"]["expected_result"]

            if search_successful and len(displayed_schools) > 0:
                logging.info(f"Test Passed. {expected_result}")
            else:
                logging.error("Test Failed. Search results do not match expected criteria.")
                capture_full_page_screenshot(driver, "TC_AD_02_search_results_mismatch")
                pytest.fail("Test Failed. Search results do not match expected criteria.")

        except Exception as e:
            logging.error(f"Error verifying search results: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_02_verification_error")
            pytest.fail(f"Test Failed. Error verifying search results: {str(e)}")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_02_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_02 Completed..")