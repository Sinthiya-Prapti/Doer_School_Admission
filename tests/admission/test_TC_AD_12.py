import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.guardian_information_page import GuardianInformationPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data_admission.json"))
def test_tc_ad_12(browser_config, test_case):
    logging.info("TC_AD_12 Started..")
    logging.info(test_case["guardian_information"][0]["TC_AD_12"]["_comment"])

    driver, wait = browser_config

    # Create object for GuardianInformationPage class
    guardian_info_page = GuardianInformationPage(driver, wait)

    try:
        # Note: This test assumes user has already filled Student Information Form
        # and has navigated to the Guardian Information Form

        # Wait for guardian information form to load
        time.sleep(3)

        # Get test data
        test_data = test_case["guardian_information"][0]["TC_AD_12"]

        # Father Information Section
        # 1. Fill Father Full Name
        try:
            guardian_info_page.enter_father_fullname(test_data["father_fullname"])
            logging.info(f"Father Full Name '{test_data['father_fullname']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter father full name: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_father_name_error")
            pytest.fail(f"Test Failed. Failed to enter father full name: {str(e)}")

        # 2. Fill Father Contact Number
        try:
            guardian_info_page.enter_father_contact(test_data["father_contact"])
            logging.info(f"Father Contact '{test_data['father_contact']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter father contact: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_father_contact_error")
            pytest.fail(f"Test Failed. Failed to enter father contact: {str(e)}")

        # 3. Fill Father Occupation
        try:
            guardian_info_page.enter_father_occupation(test_data["father_occupation"])
            logging.info(f"Father Occupation '{test_data['father_occupation']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter father occupation: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_father_occupation_error")
            pytest.fail(f"Test Failed. Failed to enter father occupation: {str(e)}")

        # 4. Fill Father NID
        try:
            guardian_info_page.enter_father_nid(test_data["father_nid"])
            logging.info(f"Father NID '{test_data['father_nid']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter father NID: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_father_nid_error")
            pytest.fail(f"Test Failed. Failed to enter father NID: {str(e)}")

        # 5. Fill Father Current Address
        try:
            guardian_info_page.enter_father_address(test_data["father_address"])
            logging.info(f"Father Address '{test_data['father_address']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter father address: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_father_address_error")
            pytest.fail(f"Test Failed. Failed to enter father address: {str(e)}")

        # Mother Information Section
        # 6. Fill Mother Full Name
        try:
            guardian_info_page.enter_mother_fullname(test_data["mother_fullname"])
            logging.info(f"Mother Full Name '{test_data['mother_fullname']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter mother full name: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_mother_name_error")
            pytest.fail(f"Test Failed. Failed to enter mother full name: {str(e)}")

        # 7. Fill Mother Contact Number
        try:
            guardian_info_page.enter_mother_contact(test_data["mother_contact"])
            logging.info(f"Mother Contact '{test_data['mother_contact']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter mother contact: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_mother_contact_error")
            pytest.fail(f"Test Failed. Failed to enter mother contact: {str(e)}")

        # 8. Fill Mother Occupation
        try:
            guardian_info_page.enter_mother_occupation(test_data["mother_occupation"])
            logging.info(f"Mother Occupation '{test_data['mother_occupation']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter mother occupation: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_mother_occupation_error")
            pytest.fail(f"Test Failed. Failed to enter mother occupation: {str(e)}")

        # 9. Fill Mother NID
        try:
            guardian_info_page.enter_mother_nid(test_data["mother_nid"])
            logging.info(f"Mother NID '{test_data['mother_nid']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter mother NID: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_mother_nid_error")
            pytest.fail(f"Test Failed. Failed to enter mother NID: {str(e)}")

        # 10. Fill Mother Current Address
        try:
            guardian_info_page.enter_mother_address(test_data["mother_address"])
            logging.info(f"Mother Address '{test_data['mother_address']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter mother address: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_mother_address_error")
            pytest.fail(f"Test Failed. Failed to enter mother address: {str(e)}")

        # 11. Select Legal Guardian Information
        try:
            guardian_info_page.select_legal_guardian(test_data["legal_guardian"])
            logging.info(f"Legal Guardian '{test_data['legal_guardian']}' selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select legal guardian: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_legal_guardian_error")
            pytest.fail(f"Test Failed. Failed to select legal guardian: {str(e)}")

        # 12. Click Save&Continue Button
        try:
            guardian_info_page.click_save_continue_button()
            logging.info("Save & Continue button clicked successfully.")
            time.sleep(3)  # Wait for processing and navigation
        except Exception as e:
            logging.error(f"Failed to click Save & Continue button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_save_continue_error")
            pytest.fail(f"Test Failed. Failed to click Save & Continue button: {str(e)}")

        # Verify expected result
        expected_result = test_data["expected_result"]

        # Check if navigation to Previous School Information form occurred
        try:
            previous_school_loaded = guardian_info_page.is_previous_school_form_loaded()
            if previous_school_loaded:
                logging.info("Successfully navigated to Previous School Information form.")
            else:
                # Check for success message instead
                success_message = guardian_info_page.get_success_message()
                if success_message and "successfully" in success_message.lower():
                    logging.info(f"Guardian information saved with message: {success_message}")
                else:
                    logging.error("Neither navigation nor success message confirmed.")
                    capture_full_page_screenshot(driver, "TC_AD_12_no_confirmation")
                    pytest.fail("Test Failed. Neither navigation nor success message confirmed.")
        except Exception as e:
            logging.error(f"Error verifying form submission: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_12_verification_error")
            pytest.fail(f"Test Failed. Error verifying form submission: {str(e)}")

        logging.info(f"Test Passed. {expected_result}")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_12_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_12 Completed..")