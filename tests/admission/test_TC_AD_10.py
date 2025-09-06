import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.admission_portal_page import AdmissionPortalPage
from pages.student_information_page import StudentInformationPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data_admission.json"))
def test_tc_ad_10(browser_config, test_case):
    logging.info("TC_AD_10 Started..")
    logging.info(test_case["student_information"][1]["TC_AD_10"]["_comment"])

    driver, wait = browser_config

    # Create objects for page classes
    admission_portal_page = AdmissionPortalPage(driver, wait)
    student_info_page = StudentInformationPage(driver, wait)

    try:
        # Wait for page to load completely
        time.sleep(3)

        # Navigate to Student Information form first
        try:
            admission_portal_page.click_apply_now_button()
            logging.info("Apply Now button clicked successfully.")
            time.sleep(2)
        except Exception as e:
            logging.error(f"Failed to click Apply Now button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_apply_now_error")
            pytest.fail(f"Test Failed. Failed to click Apply Now button: {str(e)}")

        # Get test data
        test_data = test_case["student_information"][1]["TC_AD_10"]

        # 1. Leave Full Name empty (invalid data)
        try:
            student_info_page.enter_fullname(test_data["fullname"])  # Empty string
            logging.info("Full Name left empty (invalid data).")
        except Exception as e:
            logging.error(f"Failed to handle full name field: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_fullname_error")
            pytest.fail(f"Test Failed. Failed to handle full name field: {str(e)}")

        # 2. Select Gender
        try:
            student_info_page.select_gender(test_data["gender"])
            logging.info(f"Gender '{test_data['gender']}' selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select gender: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_gender_error")
            pytest.fail(f"Test Failed. Failed to select gender: {str(e)}")

        # 3. Enter Date of Birth
        try:
            student_info_page.enter_date_of_birth(test_data["date_of_birth"])
            logging.info(f"Date of Birth '{test_data['date_of_birth']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter date of birth: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_dob_error")
            pytest.fail(f"Test Failed. Failed to enter date of birth: {str(e)}")

        # 4. Select Blood Group
        try:
            student_info_page.select_blood_group(test_data["blood_group"])
            logging.info(f"Blood Group '{test_data['blood_group']}' selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select blood group: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_blood_error")
            pytest.fail(f"Test Failed. Failed to select blood group: {str(e)}")

        # 5. Select Nationality
        try:
            student_info_page.select_nationality(test_data["nationality"])
            logging.info(f"Nationality '{test_data['nationality']}' selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select nationality: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_nationality_error")
            pytest.fail(f"Test Failed. Failed to select nationality: {str(e)}")

        # 6. Select Religion
        try:
            student_info_page.select_religion(test_data["religion"])
            logging.info(f"Religion '{test_data['religion']}' selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select religion: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_religion_error")
            pytest.fail(f"Test Failed. Failed to select religion: {str(e)}")

        # 7. Enter invalid contact number
        try:
            student_info_page.enter_contact_number(test_data["contact"])  # Invalid: "013"
            logging.info(f"Invalid contact number '{test_data['contact']}' entered.")
        except Exception as e:
            logging.error(f"Failed to enter contact number: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_contact_error")
            pytest.fail(f"Test Failed. Failed to enter contact number: {str(e)}")

        # 8. Enter invalid email format
        try:
            student_info_page.enter_email(test_data["email"])  # Invalid: "example.com"
            logging.info(f"Invalid email '{test_data['email']}' entered.")
        except Exception as e:
            logging.error(f"Failed to enter email: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_email_error")
            pytest.fail(f"Test Failed. Failed to enter email: {str(e)}")

        # 9. Enter Present Address
        try:
            student_info_page.enter_present_address(test_data["present_address"])
            logging.info(f"Present Address '{test_data['present_address']}' entered successfully.")
        except Exception as e:
            logging.error(f"Failed to enter present address: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_address_error")
            pytest.fail(f"Test Failed. Failed to enter present address: {str(e)}")

        # 10. Click Save&Continue Button
        try:
            student_info_page.click_save_continue_button()
            logging.info("Save & Continue button clicked.")
            time.sleep(2)  # Wait for validation
        except Exception as e:
            logging.error(f"Failed to click Save & Continue button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_10_save_error")
            pytest.fail(f"Test Failed. Failed to click Save & Continue button: {str(e)}")

        # Verify validation messages are displayed
        expected_result = test_data["expected_result"]

        # Check for validation errors (should be present for invalid data)
        validation_errors = student_info_page.are_validation_errors_displayed()

        # Also check specific field validation messages
        fullname_error = None
        email_error = None
        try:
            fullname_error = student_info_page.get_validation_error_message("FullName")
            email_error = student_info_page.get_validation_error_message("Email")
        except:
            pass  # Validation messages might not be available

        if validation_errors or fullname_error or email_error:
            logging.info(f"Test Passed. {expected_result}")
            if fullname_error:
                logging.info(f"Full Name validation error: {fullname_error}")
            if email_error:
                logging.info(f"Email validation error: {email_error}")
        else:
            logging.error("Test Failed. Validation errors were not displayed for invalid data.")
            capture_full_page_screenshot(driver, "TC_AD_10_no_validation")
            pytest.fail("Test Failed. Validation errors were not displayed for invalid data.")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_10_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_10 Completed..")