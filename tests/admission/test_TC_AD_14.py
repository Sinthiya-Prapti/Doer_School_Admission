import logging
import time
import pytest
import os
from utils.screenshot_utils import capture_full_page_screenshot
from pages.document_upload_page import DocumentUploadPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data_admission.json"))
def test_tc_ad_14(browser_config, test_case):
    logging.info("TC_AD_14 Started..")
    logging.info(test_case["document_upload"][0]["TC_AD_14"]["_comment"])

    driver, wait = browser_config

    # Create object for DocumentUploadPage class
    document_upload_page = DocumentUploadPage(driver, wait)

    try:
        # Note: This test assumes user has reached the Document Upload form
        # after completing all previous sections

        # Wait for document upload form to load
        time.sleep(3)

        # Get test data
        test_data = test_case["document_upload"][0]["TC_AD_14"]

        # Prepare test files (in a real scenario, you would have actual test files)
        # For this example, we'll assume test files exist in a test_files directory
        test_files_dir = os.path.join(os.getcwd(), "test_files")

        # Ensure test files directory exists (create if needed for demo)
        if not os.path.exists(test_files_dir):
            os.makedirs(test_files_dir)
            # In a real scenario, you would place actual test files here

        student_photo_path = os.path.join(test_files_dir, test_data["student_photo"])
        birth_certificate_path = os.path.join(test_files_dir, test_data["birth_certificate"])
        academic_records_path = os.path.join(test_files_dir, test_data["academic_records"])

        # Create dummy files for testing if they don't exist
        # In a real test environment, you would have pre-created valid test files
        if not os.path.exists(student_photo_path):
            logging.warning(f"Test file not found: {student_photo_path}. Creating dummy file for testing.")
            with open(student_photo_path, 'w') as f:
                f.write("dummy photo content")

        if not os.path.exists(birth_certificate_path):
            logging.warning(f"Test file not found: {birth_certificate_path}. Creating dummy file for testing.")
            with open(birth_certificate_path, 'w') as f:
                f.write("dummy certificate content")

        if not os.path.exists(academic_records_path):
            logging.warning(f"Test file not found: {academic_records_path}. Creating dummy file for testing.")
            with open(academic_records_path, 'w') as f:
                f.write("dummy records content")

        # 1. Upload Student's Recent Photo
        try:
            document_upload_page.upload_student_photo(student_photo_path)
            logging.info(f"Student photo '{test_data['student_photo']}' uploaded successfully.")

            # Verify upload success
            if document_upload_page.is_file_uploaded_successfully("photo"):
                logging.info("✅ Student photo upload confirmed.")
            else:
                logging.warning("⚠️ Student photo upload confirmation not available.")

        except Exception as e:
            logging.error(f"Failed to upload student photo: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_14_photo_upload_error")
            pytest.fail(f"Test Failed. Failed to upload student photo: {str(e)}")

        # 2. Upload Birth Certificate (PDF)
        try:
            document_upload_page.upload_birth_certificate(birth_certificate_path)
            logging.info(f"Birth certificate '{test_data['birth_certificate']}' uploaded successfully.")

            # Verify upload success
            if document_upload_page.is_file_uploaded_successfully("certificate"):
                logging.info("✅ Birth certificate upload confirmed.")
            else:
                logging.warning("⚠️ Birth certificate upload confirmation not available.")

        except Exception as e:
            logging.error(f"Failed to upload birth certificate: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_14_certificate_upload_error")
            pytest.fail(f"Test Failed. Failed to upload birth certificate: {str(e)}")

        # 3. Upload Academic records (PDF)
        try:
            document_upload_page.upload_academic_records(academic_records_path)
            logging.info(f"Academic records '{test_data['academic_records']}' uploaded successfully.")

            # Verify upload success
            if document_upload_page.is_file_uploaded_successfully("records"):
                logging.info("✅ Academic records upload confirmed.")
            else:
                logging.warning("⚠️ Academic records upload confirmation not available.")

        except Exception as e:
            logging.error(f"Failed to upload academic records: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_14_records_upload_error")
            pytest.fail(f"Test Failed. Failed to upload academic records: {str(e)}")

        # 4. Click Save&Continue Button
        try:
            document_upload_page.click_save_continue_button()
            logging.info("Save & Continue button clicked successfully.")
            time.sleep(3)  # Wait for processing and navigation
        except Exception as e:
            logging.error(f"Failed to click Save & Continue button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_14_save_continue_error")
            pytest.fail(f"Test Failed. Failed to click Save & Continue button: {str(e)}")

        # Verify expected result
        expected_result = test_data["expected_result"]

        # Check if navigation to review page occurred or success message displayed
        try:
            review_page_loaded = document_upload_page.is_review_page_loaded()
            success_message = document_upload_page.get_success_message()

            if review_page_loaded:
                logging.info("✅ Successfully navigated to Review Page.")
            elif success_message and "success" in success_message.lower():
                logging.info(f"✅ Document upload success message: {success_message}")
            else:
                # Check current URL for confirmation
                current_url = driver.current_url
                if "review" in current_url.lower() or "summary" in current_url.lower():
                    logging.info("✅ Navigation to review/summary page confirmed via URL.")
                else:
                    logging.error("Document upload completion not confirmed.")
                    capture_full_page_screenshot(driver, "TC_AD_14_no_confirmation")
                    pytest.fail("Test Failed. Document upload completion not confirmed.")

        except Exception as e:
            logging.error(f"Error verifying document upload completion: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_14_verification_error")
            pytest.fail(f"Test Failed. Error verifying document upload completion: {str(e)}")

        logging.info(f"Test Passed. {expected_result}")

        # Cleanup dummy test files (optional)
        try:
            if os.path.exists(student_photo_path):
                os.remove(student_photo_path)
            if os.path.exists(birth_certificate_path):
                os.remove(birth_certificate_path)
            if os.path.exists(academic_records_path):
                os.remove(academic_records_path)
            if os.path.exists(test_files_dir) and not os.listdir(test_files_dir):
                os.rmdir(test_files_dir)
        except Exception as e:
            logging.warning(f"Could not cleanup test files: {str(e)}")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_14_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_14 Completed..")