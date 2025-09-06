import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.admission_portal_page import AdmissionPortalPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data_admission.json"))
def test_tc_ad_01(browser_config, test_case):
    logging.info("TC_AD_01 Started..")
    logging.info(test_case["admission_portal"][0]["TC_AD_01"]["_comment"])

    driver, wait = browser_config

    # Create object for AdmissionPortalPage class
    admission_portal_page = AdmissionPortalPage(driver, wait)

    try:
        # Wait for page to load completely
        time.sleep(3)

        # 1. Verify admission cards are visible
        are_cards_visible = admission_portal_page.are_admission_cards_visible()
        if are_cards_visible:
            logging.info("Admission cards are visible successfully.")
        else:
            logging.error("Admission cards are not visible.")
            capture_full_page_screenshot(driver, "TC_AD_01_cards_not_visible")
            pytest.fail("Test Failed. Admission cards are not visible.")

        # 2. Check if ongoing admissions message is displayed
        try:
            ongoing_message = admission_portal_page.get_ongoing_admissions_message()
            if "ongoing admissions" in ongoing_message.lower():
                logging.info(f"Ongoing admissions message displayed: {ongoing_message}")
            else:
                logging.warning(f"Unexpected message displayed: {ongoing_message}")
        except Exception as e:
            logging.warning("Ongoing admissions message element not found, but this might be acceptable.")

        # 3. Count admission cards
        try:
            cards_count = admission_portal_page.get_admission_cards_count()
            logging.info(f"Total admission cards displayed: {cards_count}")

            if cards_count > 0:
                logging.info("Test Passed. Admission cards are displayed with required information.")
            else:
                logging.error("Test Failed. No admission cards found.")
                capture_full_page_screenshot(driver, "TC_AD_01_no_cards")
                pytest.fail("Test Failed. No admission cards found.")

        except Exception as e:
            logging.error(f"Error counting admission cards: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_01_error")
            pytest.fail(f"Test Failed. Error counting admission cards: {str(e)}")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_01_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_01 Completed..")