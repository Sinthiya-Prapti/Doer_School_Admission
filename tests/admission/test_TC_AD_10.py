import logging
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
import os
import re

from pages.previous_school_page import PreviousSchoolPage
from utils.screenshot_utils import capture_full_page_screenshot
from pages.admission_portal_page import AdmissionPortalPage
from pages.student_information_page import StudentInformationPage
from pages.guardian_information_page import GuardianInformationPage
from pages.document_upload_page import DocumentUploadPage
from pages.application_review_page import ApplicationReviewPage
from utils.data_loader import load_all_test_data
from utils.login_utils import perform_login


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_admission_complete_flow(browser_config, test_case, self=None):
    """
    Comprehensive test covering the entire admission form flow:
    - Login (if required)
    - Student Information (TC_AD_09/TC_AD_10)
    - Guardian Information (TC_AD_12)
    - Document Upload (TC_AD_14)
    - Application Review & Submission (TC_AD_15)
    """
    logging.info("=== ADMISSION COMPLETE FLOW TEST STARTED ===")

    driver, wait = browser_config
    draft_id = None  # Track draft_id throughout the flow

    # Initialize page objects
    admission_portal_page = AdmissionPortalPage(driver, wait)
    student_info_page = StudentInformationPage(driver, wait)
    guardian_info_page = GuardianInformationPage(driver, wait)
    previous_school_page = PreviousSchoolPage(driver, wait)
    document_upload_page = DocumentUploadPage(driver, wait)
    application_review_page = ApplicationReviewPage(driver, wait)

    try:
        # =============================================
        # STEP 1: LOGIN (if login data is provided)
        # =============================================
        if "registration" in test_case and len(test_case["registration"]) > 5:
            logging.info("STEP 1: Performing Login...")
            login_data = test_case["registration"][5]["TC_Reg_06"]

            try:
                perform_login(driver, wait, login_data, "ADMISSION_FLOW")
                logging.info("✅ Login completed successfully")
                time.sleep(2)
            except Exception as e:
                logging.error(f"❌ Login failed: {str(e)}")
                capture_full_page_screenshot(driver, "admission_flow_login_failed")
                pytest.fail(f"Login failed: {str(e)}")

        # =============================================
        # STEP 2: NAVIGATE TO ADMISSION FORM
        # =============================================
        logging.info("STEP 2: Navigating to Admission Form...")
        time.sleep(3)

        try:
            # Navigate to admission page if not already there
            admission_portal_page.click_admission_navigation()
            time.sleep(2)


            admission_portal_page.click_apply_now_button()
            logging.info("✅ Successfully navigated to admission form")
            time.sleep(2)
        except Exception as e:
            logging.error(f"❌ Failed to navigate to admission form: {str(e)}")
            capture_full_page_screenshot(driver, "admission_flow_navigation_failed")
            pytest.fail(f"Failed to navigate to admission form: {str(e)}")

        # =============================================
        # STEP 3: STUDENT INFORMATION FORM
        # =============================================
        logging.info("STEP 3: Filling Student Information Form...")

        # Use valid data (TC_AD_09) or invalid data (TC_AD_10) based on test case
        if "student_information" in test_case and len(test_case["student_information"]) > 0:
            # Try TC_AD_09 first (valid data), fallback to TC_AD_10 (invalid data)
            student_data = None
            test_type = "valid"

            if "TC_AD_09" in test_case["student_information"][0]:
                student_data = test_case["student_information"][0]["TC_AD_09"]
                test_type = "valid"
            elif len(test_case["student_information"]) > 1 and "TC_AD_10" in test_case["student_information"][1]:
                student_data = test_case["student_information"][1]["TC_AD_10"]
                test_type = "invalid"

            if student_data:
                logging.info(f"Using {test_type} student data: {student_data.get('_comment', '')}")

                # Fill student information form
                try:
                    # Full Name
                    student_info_page.enter_fullname(student_data["fullname"])
                    logging.info(f"Full Name: '{student_data['fullname']}'")

                    # Gender
                    student_info_page.select_gender(student_data["gender"])
                    logging.info(f"Gender: '{student_data['gender']}'")

                    # Date of Birth
                    student_info_page.enter_date_of_birth(student_data["date_of_birth"])
                    logging.info(f"Date of Birth: '{student_data['date_of_birth']}'")

                    # Blood Group (if available)
                    # if "blood_group" in student_data:
                    #     student_info_page.select_blood_group(student_data["blood_group"])
                    #     logging.info(f"Blood Group: '{student_data['blood_group']}'")

                    # Nationality
                    student_info_page.select_nationality(student_data["nationality"])
                    logging.info(f"Nationality: '{student_data['nationality']}'")

                    # Religion
                    student_info_page.select_religion(student_data["religion"])
                    logging.info(f"Religion: '{student_data['religion']}'")

                    # Contact
                    student_info_page.enter_contact_number(student_data["contact"])
                    logging.info(f"Contact: '{student_data['contact']}'")

                    # Email
                    student_info_page.enter_email(student_data["email"])
                    logging.info(f"Email: '{student_data['email']}'")

                    # Present Address
                    student_info_page.enter_present_address(student_data["present_address"])
                    logging.info(f"Present Address: '{student_data['present_address']}'")

                    # Click Save & Continue
                    student_info_page.click_save_continue_button()
                    logging.info("Save & Continue button clicked")
                    time.sleep(3)

                    # Check for validation errors
                    validation_errors = student_info_page.are_validation_errors_displayed()

                    if test_type == "valid":
                        if validation_errors:
                            logging.error("❌ Unexpected validation errors for valid data")
                            capture_full_page_screenshot(driver, "admission_flow_unexpected_validation")
                            pytest.fail("Validation errors appeared for valid student data")
                        else:
                            logging.info("✅ Student information saved successfully (valid data)")
                    else:
                        if not validation_errors:
                            logging.error("❌ Expected validation errors not displayed for invalid data")
                            capture_full_page_screenshot(driver, "admission_flow_missing_validation")
                            pytest.fail("Expected validation errors for invalid student data")
                        else:
                            logging.info("✅ Validation errors correctly displayed for invalid data")
                            # For invalid data, we stop here as form won't progress
                            logging.info("=== ADMISSION FLOW TEST COMPLETED (Invalid Data Validation) ===")
                            return

                    # Extract draft_id from URL after successful submission
                    current_url = driver.current_url
                    draft_match = re.search(r'draft[_=](\d+)', current_url)
                    if draft_match:
                        draft_id = draft_match.group(1)
                        logging.info(f"🔑 Draft ID captured: {draft_id}")

                except Exception as e:
                    logging.error(f"❌ Error filling student information: {str(e)}")
                    capture_full_page_screenshot(driver, "admission_flow_student_info_error")
                    pytest.fail(f"Failed to fill student information: {str(e)}")

        # =============================================
        # STEP 4: GUARDIAN INFORMATION FORM
        # =============================================
        logging.info("STEP 4: Filling Guardian Information Form...")

        if "guardian_information" in test_case and len(test_case["guardian_information"]) > 0:
            guardian_data = test_case["guardian_information"][0]["TC_AD_12"]
            logging.info(f"Guardian data: {guardian_data.get('_comment', '')}")

            try:
                # Wait for guardian form to load
                time.sleep(1)

                # Father Information
                guardian_info_page.enter_father_fullname(guardian_data["father_fullname"])
                logging.info(f"Father Full Name: '{guardian_data['father_fullname']}'")

                guardian_info_page.enter_father_contact(guardian_data["father_contact"])
                logging.info(f"Father Contact: '{guardian_data['father_contact']}'")

                guardian_info_page.enter_father_occupation(guardian_data["father_occupation"])
                logging.info(f"Father Occupation: '{guardian_data['father_occupation']}'")

                guardian_info_page.enter_father_nid(guardian_data["father_nid"])
                logging.info(f"Father NID: '{guardian_data['father_nid']}'")

                guardian_info_page.enter_father_address(guardian_data["father_address"])
                logging.info(f"Father Address: '{guardian_data['father_address']}'")

                # Mother Information
                guardian_info_page.enter_mother_fullname(guardian_data["mother_fullname"])
                logging.info(f"Mother Full Name: '{guardian_data['mother_fullname']}'")

                guardian_info_page.enter_mother_contact(guardian_data["mother_contact"])
                logging.info(f"Mother Contact: '{guardian_data['mother_contact']}'")

                guardian_info_page.enter_mother_occupation(guardian_data["mother_occupation"])
                logging.info(f"Mother Occupation: '{guardian_data['mother_occupation']}'")

                guardian_info_page.enter_mother_nid(guardian_data["mother_nid"])
                logging.info(f"Mother NID: '{guardian_data['mother_nid']}'")

                guardian_info_page.enter_mother_address(guardian_data["mother_address"])
                logging.info(f"Mother Address: '{guardian_data['mother_address']}'")

                # Legal Guardian
                guardian_info_page.select_legal_guardian(guardian_data["legal_guardian"])
                logging.info(f"Legal Guardian: '{guardian_data['legal_guardian']}'")

                # Click Save & Continue
                guardian_info_page.click_save_continue_button()
                logging.info("Save & Continue button clicked")

                time.sleep(1)

                success_message = guardian_info_page.get_success_message()
                if success_message == "Family information added successfully.":
                    logging.info("Family information added successfully.")
                else:
                    logging.error(f"Previous school information error: {success_message}")
                    pytest.fail(f"Previous school information error: {success_message}")


            except Exception as e:
                logging.error(f"❌ Error filling guardian information: {str(e)}")
                capture_full_page_screenshot(driver, "admission_flow_guardian_error")
                pytest.fail(f"Failed to fill guardian information: {str(e)}")

        # =============================================
        # STEP 5: PREVIOUS SCHOOL INFORMATION FORM
        # =============================================
        logging.info("STEP 5: Filling Previous School Information Form...")

        if "previous_school" in test_case and len(test_case["previous_school"]) > 0:
            previous_school_data = test_case["previous_school"][0]["TC_AD_13"]
            logging.info(f"Previous School data: {previous_school_data.get('_comment', '')}")

            try:
                # Wait for previous school form to load
                time.sleep(3)

                # School Information
                previous_school_page.enter_school_name(previous_school_data["school_name"])
                logging.info(f"School Name: '{previous_school_data['school_name']}'")

                previous_school_page.select_board_curriculum(previous_school_data["board_curriculum"])
                logging.info(f"Board Curriculum: '{previous_school_data['board_curriculum']}'")

                previous_school_page.select_last_class_completed(previous_school_data["last_class"])
                logging.info(f"Last Class Completed: '{previous_school_data['last_class']}'")

                previous_school_page.enter_school_address(previous_school_data["school_address"])
                logging.info(f"School Address: '{previous_school_data['school_address']}'")

                # Click Save & Continue
                previous_school_page.click_save_continue_button()
                logging.info("Save & Continue button clicked")
                time.sleep(1)

                # Verify success message and navigation
                success_message = previous_school_page.get_success_message()
                # success_message = guardian_info_page.get_success_message()
                if success_message == "Previous school information added successfully.":
                    logging.info("Previous school information added successfully.")
                else:
                    logging.error(f"Previous school information error: {success_message}")
                    pytest.fail(f"Previous school information error: {success_message}")



            except Exception as e:
                logging.error(f"❌ Error filling previous school information: {str(e)}")
                capture_full_page_screenshot(driver, "admission_flow_previous_school_error")
                pytest.fail(f"Failed to fill previous school information: {str(e)}")

        # =============================================
        # STEP 5: DOCUMENT UPLOAD
        # =============================================
        logging.info("STEP 5: Document Upload...")

        if "document_upload" in test_case and len(test_case["document_upload"]) > 0:
            document_data = test_case["document_upload"][0]["TC_AD_14"]
            logging.info(f"Document data: {document_data.get('_comment', '')}")

            try:
                # Wait for document upload form
                time.sleep(3)

                # Prepare test files directory
                test_files_dir = os.path.join(os.getcwd(), "test_files")
                if not os.path.exists(test_files_dir):
                    os.makedirs(test_files_dir)

                # Create/verify test files
                files_to_upload = {
                    "student_photo": os.path.join(test_files_dir, document_data["student_photo"]),
                    "birth_certificate": os.path.join(test_files_dir, document_data["birth_certificate"]),
                    "academic_records": os.path.join(test_files_dir, document_data["academic_records"])
                }

                for file_type, file_path in files_to_upload.items():
                    if not os.path.exists(file_path):
                        logging.warning(f"Creating dummy test file: {file_path}")
                        with open(file_path, 'w') as f:
                            f.write(f"dummy {file_type} content for testing")

                # Upload files
                document_upload_page.upload_student_photo(files_to_upload["student_photo"])
                logging.info("✅ Student photo uploaded")

                document_upload_page.upload_birth_certificate(files_to_upload["birth_certificate"])
                logging.info("✅ Birth certificate uploaded")

                document_upload_page.upload_academic_records(files_to_upload["academic_records"])
                logging.info("✅ Academic records uploaded")

                # Save & Continue
                document_upload_page.click_save_continue_button()
                logging.info("Document Upload Save & Continue clicked")
                time.sleep(3)

            except Exception as e:
                logging.error(f"❌ Error uploading documents: {str(e)}")
                capture_full_page_screenshot(driver, "admission_flow_document_error")
                pytest.fail(f"Failed to upload documents: {str(e)}")

        # =============================================
        # STEP 6: APPLICATION REVIEW & SUBMISSION
        # =============================================
        logging.info("STEP 6: Application Review & Submission...")

        if "application_submission" in test_case and len(test_case["application_submission"]) > 0:
            submission_data = test_case["application_submission"][0]["TC_AD_15"]
            logging.info(f"Submission data: {submission_data.get('_comment', '')}")

            try:
                # Wait for review page
                time.sleep(1)

                # Check confirmation checkbox
                application_review_page.check_confirmation_checkbox()
                logging.info("✅ Confirmation checkbox checked")

                # Submit application
                application_review_page.click_submit_button()
                logging.info("✅ Submit button clicked")
                time.sleep(1)

                # Verify completion
                completion_message = application_review_page.get_completion_message()
                if completion_message and "success" in completion_message:
                    logging.info("✅ Application completion confirmed")
                else:
                    logging.warning("⚠️ Completion message not found, checking other indicators")

                # Check for payment buttons
                proceed_button_visible = application_review_page.is_proceed_to_payment_button_visible()
                pay_later_visible = application_review_page.is_pay_later_button_visible()

                if proceed_button_visible and pay_later_visible:
                    logging.info("✅ Payment options displayed correctly")
                else:
                    logging.warning("⚠️ Payment options not fully visible")

                # Final URL check
                final_url = driver.current_url
                logging.info(f"Final URL: {final_url}")

                if draft_id and draft_id in final_url:
                    logging.info(f"✅ Draft ID {draft_id} maintained throughout flow")

            except Exception as e:
                logging.error(f"❌ Error in application submission: {str(e)}")
                capture_full_page_screenshot(driver, "admission_flow_submission_error")
                pytest.fail(f"Failed to submit application: {str(e)}")

        # =============================================
        # FINAL SUCCESS
        # =============================================

        capture_full_page_screenshot(driver, "admission_flow_submission_success")
        logging.info("ADMISSION COMPLETE FLOW TEST PASSED")
        logging.info("All steps completed successfully:")
        logging.info("Login (if required)")
        logging.info("Student Information")
        logging.info("Guardian Information")
        logging.info("Document Upload")
        logging.info("Application Review & Submission")
        if draft_id:
            logging.info(f"  ✓ Draft ID tracked: {draft_id}")

    except Exception as e:
        logging.error(f"❌ ADMISSION FLOW FAILED: {str(e)}")
        capture_full_page_screenshot(driver, "admission_flow_general_error")
        pytest.fail(f"Admission flow failed: {str(e)}")

    finally:
        logging.info("=== ADMISSION COMPLETE FLOW TEST COMPLETED ===")

