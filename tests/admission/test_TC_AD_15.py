import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.application_review_page import ApplicationReviewPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data_admission.json"))
def test_tc_ad_15(browser_config, test_case):
    logging.info("TC_AD_15 Started..")
    logging.info(test_case["application_submission"][0]["TC_AD_15"]["_comment"])

    driver, wait = browser_config

    # Create object for ApplicationReviewPage class
    application_review_page = ApplicationReviewPage(driver, wait)

    try:
        # Note: This test assumes user has already completed all previous sections
        # and has reached the Review Page. In a real scenario, we would need to
        # navigate through all previous forms or have a direct way to reach review page.

        # For this test, we'll assume we're already on the review page
        # In practice, you might need to fill all previous forms first

        # Wait for review page to load
        time.sleep(3)

        # Get test data
        test_data = test_case["application_submission"][0]["TC_AD_15"]

        # 1. Scroll down to the bottom of the Review Page
        try:
            application_review_page.scroll_to_bottom()
            logging.info("Scrolled to bottom of the Review Page successfully.")
        except Exception as e:
            logging.error(f"Failed to scroll to bottom: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_15_scroll_error")
            pytest.fail(f"Test Failed. Failed to scroll to bottom: {str(e)}")

        # 2. Tick/check the confirmation checkbox
        try:
            application_review_page.check_confirmation_checkbox()
            logging.info("Confirmation checkbox checked successfully.")
        except Exception as e:
            logging.error(f"Failed to check confirmation checkbox: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_15_checkbox_error")
            pytest.fail(f"Test Failed. Failed to check confirmation checkbox: {str(e)}")

        # 3. Click the Submit button
        try:
            application_review_page.click_submit_button()
            logging.info("Submit button clicked successfully.")
        except Exception as e:
            logging.error(f"Failed to click Submit button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_15_submit_error")
            pytest.fail(f"Test Failed. Failed to click Submit button: {str(e)}")

        # 4. Verify the expected results
        expected_result = test_data["expected_result"]

        # Check for completion message
        try:
            completion_message = application_review_page.get_completion_message()
            if completion_message and "Application Form Completed!" in completion_message:
                logging.info(f"Completion message displayed: {completion_message}")
            else:
                logging.error("Application Form Completed message not found.")
                capture_full_page_screenshot(driver, "TC_AD_15_no_completion_message")
                pytest.fail("Test Failed. Application Form Completed message not found.")
        except Exception as e:
            logging.error(f"Error checking completion message: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_15_completion_message_error")
            pytest.fail(f"Test Failed. Error checking completion message: {str(e)}")

        # Check for "Proceed to Payment" button
        try:
            proceed_button_visible = application_review_page.is_proceed_to_payment_button_visible()
            if proceed_button_visible:
                logging.info("'Proceed to Payment' button is visible.")
            else:
                logging.error("'Proceed to Payment' button is not visible.")
                capture_full_page_screenshot(driver, "TC_AD_15_no_proceed_button")
                pytest.fail("Test Failed. 'Proceed to Payment' button is not visible.")
        except Exception as e:
            logging.error(f"Error checking Proceed to Payment button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_15_proceed_button_error")
            pytest.fail(f"Test Failed. Error checking Proceed to Payment button: {str(e)}")

        # Check for "Pay Later" button
        try:
            pay_later_button_visible = application_review_page.is_pay_later_button_visible()
            if pay_later_button_visible:
                logging.info("'Pay Later' button is visible.")
            else:
                logging.error("'Pay Later' button is not visible.")
                capture_full_page_screenshot(driver, "TC_AD_15_no_pay_later_button")
                pytest.fail("Test Failed. 'Pay Later' button is not visible.")
        except Exception as e:
            logging.error(f"Error checking Pay Later button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_15_pay_later_button_error")
            pytest.fail(f"Test Failed. Error checking Pay Later button: {str(e)}")

        # Check for payment warning note
        try:
            warning_note = application_review_page.get_payment_warning_note()
            if warning_note and "application will not be reviewed until the fee is paid" in warning_note.lower():
                logging.info(f"Payment warning note displayed: {warning_note}")
            else:
                logging.error("Payment warning note not found or incorrect.")
                capture_full_page_screenshot(driver, "TC_AD_15_no_warning_note")
                pytest.fail("Test Failed. Payment warning note not found or incorrect.")
        except Exception as e:
            logging.error(f"Error checking payment warning note: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_15_warning_note_error")
            pytest.fail(f"Test Failed. Error checking payment warning note: {str(e)}")

        # If all checks pass
        logging.info("Test Passed. All expected elements are displayed correctly.")
        logging.info("✅ Application Form Completed popup displayed successfully")
        logging.info("✅ 'Proceed to Payment' button is visible")
        logging.info("✅ 'Pay Later' button is visible")
        logging.info("✅ Payment warning note is displayed")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_15_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_15 Completed..")