import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.admission_portal_page import AdmissionPortalPage
from pages.student_information_page import StudentInformationPage
from utils.data_loader import load_all_test_data
from utils.login_utils import perform_login


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_ad_09_with_login(browser_config, test_case):
    """TC_AD_09: Test admission form filling with login prerequisite"""
    logging.info("TC_AD_09 with Login Started..")
    logging.info(test_case["student_information"][0]["TC_AD_09"]["_comment"])

    driver, wait = browser_config

    # Create objects for page classes
    admission_portal_page = AdmissionPortalPage(driver, wait)
    student_info_page = StudentInformationPage(driver, wait)

    try:
        # Get test data
        test_data = test_case["student_information"][0]["TC_AD_09"]
        login_data = test_case["registration"][5]["TC_Reg_06"]

        try:
            perform_login(driver, wait, login_data, "TC_AD_09")
            logging.info("Login completed successfully before admission form")
            time.sleep(2)
        except Exception as e:
            logging.error(f"Login failed before admission form: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_login_failed")
            pytest.fail(f"Test Failed. Login failed before admission form: {str(e)}")

        # Wait for page to load completely after login
        time.sleep(3)

        # goto admission page
        admission_portal_page.click_admission_navigation()

        # Navigate to Student Information form
        try:
            admission_portal_page.click_apply_now_button()
            logging.info("Apply Now button clicked successfully.")
            time.sleep(2)
        except Exception as e:
            logging.error(f"Failed to click Apply Now button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_apply_now_error")
            pytest.fail(f"Test Failed. Failed to click Apply Now button: {str(e)}")

        # Fill the admission form (same as original code)
        # 1. Fill Full Name
        try:
            student_info_page.enter_fullname(test_data["fullname"])
            logging.info(f"Full Name '{test_data['fullname']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter full name: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_fullname_error")
            pytest.fail(f"Test Failed. Failed to enter full name: {str(e)}")

        # 2. Select Gender
        try:
            student_info_page.select_gender(test_data["gender"])
            logging.info(f"Gender '{test_data['gender']}' selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select gender: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_gender_error")
            pytest.fail(f"Test Failed. Failed to select gender: {str(e)}")

        # 3. Enter Date of Birth
        try:
            student_info_page.enter_date_of_birth(test_data["date_of_birth"])
            logging.info(f"Date of Birth '{test_data['date_of_birth']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter date of birth: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_dob_error")
            pytest.fail(f"Test Failed. Failed to enter date of birth: {str(e)}")

        # # 4. Select Blood Group
        # try:
        #     student_info_page.select_blood_group(test_data["blood_group"])
        #     logging.info(f"Blood Group '{test_data['blood_group']}' selected successfully.")
        # except Exception as e:
        #     logging.error(f"Failed to select blood group: {str(e)}")
        #     capture_full_page_screenshot(driver, "TC_AD_09_blood_error")
        #     pytest.fail(f"Test Failed. Failed to select blood group: {str(e)}")

        # 5. Select Nationality
        try:
            student_info_page.select_nationality(test_data["nationality"])
            logging.info(f"Nationality '{test_data['nationality']}' selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select nationality: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_nationality_error")
            pytest.fail(f"Test Failed. Failed to select nationality: {str(e)}")

        # 6. Select Religion
        try:
            student_info_page.select_religion(test_data["religion"])
            logging.info(f"Religion '{test_data['religion']}' selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select religion: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_religion_error")
            pytest.fail(f"Test Failed. Failed to select religion: {str(e)}")

        # 7. Enter Student Contact
        try:
            student_info_page.enter_contact_number(test_data["contact"])
            logging.info(f"Contact number '{test_data['contact']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter contact number: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_contact_error")
            pytest.fail(f"Test Failed. Failed to enter contact number: {str(e)}")

        # 8. Enter Student Email
        try:
            student_info_page.enter_email(test_data["email"])
            logging.info(f"Email '{test_data['email']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter email: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_email_error")
            pytest.fail(f"Test Failed. Failed to enter email: {str(e)}")

        # 9. Enter Present Address
        try:
            student_info_page.enter_present_address(test_data["present_address"])
            logging.info(f"Present Address '{test_data['present_address']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter present address: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_address_error")
            pytest.fail(f"Test Failed. Failed to enter present address: {str(e)}")

        # 10. Click Save&Continue Button
        try:
            student_info_page.click_save_continue_button()
            logging.info("Save & Continue button clicked successfully.")
            time.sleep(3)  # Wait for processing
        except Exception as e:
            logging.error(f"Failed to click Save & Continue button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_09_save_error")
            pytest.fail(f"Test Failed. Failed to click Save & Continue button: {str(e)}")

        # Verify expected result
        expected_result = test_data["expected_result"]

        # Check for success (no validation errors and form progresses)
        validation_errors = student_info_page.are_validation_errors_displayed()

        if not validation_errors:
            logging.info(f"Test Passed. {expected_result}")
        else:
            logging.error("Test Failed. Validation errors were displayed despite valid data.")
            capture_full_page_screenshot(driver, "TC_AD_09_validation_error")
            pytest.fail("Test Failed. Validation errors were displayed despite valid data.")

            # https: // admission - test.doer.school / en / admission / apply / 15?draft = 77

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_09_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_09 with Login Completed..")