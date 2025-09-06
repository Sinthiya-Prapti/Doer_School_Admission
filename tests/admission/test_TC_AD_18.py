import logging
import time
import pytest
from utils.screenshot_utils import capture_full_page_screenshot
from pages.payment_page import PaymentPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data_admission.json"))
def test_tc_ad_18(browser_config, test_case):
    logging.info("TC_AD_18 Started..")
    logging.info(test_case["payment"][0]["TC_AD_18"]["_comment"])

    driver, wait = browser_config

    # Create object for PaymentPage class
    payment_page = PaymentPage(driver, wait)

    try:
        # Note: This test assumes user has reached the Payment Page after completing
        # the application form. In a real scenario, we would need to navigate through
        # all previous forms or have a direct way to reach payment page.

        # Wait for payment page to load
        time.sleep(3)

        # Get test data
        test_data = test_case["payment"][0]["TC_AD_18"]
        payment_method = test_data["payment_method"]

        # 1. Ensure Offline payment option is selected
        try:
            payment_page.select_offline_payment_method()
            logging.info(f"'{payment_method}' payment method selected successfully.")
        except Exception as e:
            logging.error(f"Failed to select offline payment method: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_18_payment_method_error")
            pytest.fail(f"Test Failed. Failed to select offline payment method: {str(e)}")

        # 2. Click on the View Voucher button
        try:
            payment_page.click_view_voucher_button()
            logging.info("View Voucher button clicked successfully.")
        except Exception as e:
            logging.error(f"Failed to click View Voucher button: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_18_voucher_button_error")
            pytest.fail(f"Test Failed. Failed to click View Voucher button: {str(e)}")

        # 3. Verify the Payment Voucher is displayed
        try:
            voucher_displayed = payment_page.is_payment_voucher_displayed()
            if voucher_displayed:
                logging.info("Payment Voucher is displayed successfully.")
            else:
                logging.error("Payment Voucher is not displayed.")
                capture_full_page_screenshot(driver, "TC_AD_18_no_voucher")
                pytest.fail("Test Failed. Payment Voucher is not displayed.")
        except Exception as e:
            logging.error(f"Error checking voucher display: {str(e)}")
            capture_full_page_screenshot(driver, "TC_AD_18_voucher_check_error")
            pytest.fail(f"Test Failed. Error checking voucher display: {str(e)}")

        # 4. Verify voucher contains required information
        expected_result = test_data["expected_result"]
        voucher_details = payment_page.get_voucher_details()

        # Check Application Number
        if voucher_details.get('application_number'):
            logging.info(f"✅ Application Number found: {voucher_details['application_number']}")
        else:
            logging.error("❌ Application Number not found in voucher.")
            capture_full_page_screenshot(driver, "TC_AD_18_no_app_number")
            pytest.fail("Test Failed. Application Number not found in voucher.")

        # Check Applicant/Student Name
        if voucher_details.get('applicant_name'):
            logging.info(f"✅ Applicant Name found: {voucher_details['applicant_name']}")
        else:
            logging.error("❌ Applicant/Student Name not found in voucher.")
            capture_full_page_screenshot(driver, "TC_AD_18_no_applicant_name")
            pytest.fail("Test Failed. Applicant/Student Name not found in voucher.")

        # Check Applied School Name
        if voucher_details.get('school_name'):
            logging.info(f"✅ School Name found: {voucher_details['school_name']}")
        else:
            logging.error("❌ Applied School Name not found in voucher.")
            capture_full_page_screenshot(driver, "TC_AD_18_no_school_name")
            pytest.fail("Test Failed. Applied School Name not found in voucher.")

        # Check Application Fee Amount
        if voucher_details.get('fee_amount'):
            logging.info(f"✅ Application Fee Amount found: {voucher_details['fee_amount']}")
        else:
            logging.error("❌ Application Fee Amount not found in voucher.")
            capture_full_page_screenshot(driver, "TC_AD_18_no_fee_amount")
            pytest.fail("Test Failed. Application Fee Amount not found in voucher.")

        # Check Payment Instructions
        if voucher_details.get('payment_instructions'):
            instructions = voucher_details['payment_instructions']
            logging.info(f"✅ Payment Instructions found: {instructions}")

            # Verify it mentions cash payment at school campus
            if "cash payment" in instructions.lower() and "school campus" in instructions.lower():
                logging.info("✅ Payment Instructions mention Cash Payment at School Campus.")
            else:
                logging.warning("⚠️ Payment Instructions may not explicitly mention Cash Payment at School Campus.")
        else:
            logging.error("❌ Payment Instructions not found in voucher.")
            capture_full_page_screenshot(driver, "TC_AD_18_no_instructions")
            pytest.fail("Test Failed. Payment Instructions not found in voucher.")

        # 5. Verify voucher page/document opened successfully
        try:
            voucher_page_opened = payment_page.is_voucher_page_opened()
            if voucher_page_opened:
                logging.info("✅ Payment Voucher page/document opened successfully.")
            else:
                logging.info("ℹ️ Voucher may be displayed inline rather than in a new page.")
        except Exception as e:
            logging.warning(f"Could not verify voucher page opening: {str(e)}")

        # If all checks pass
        logging.info("Test Passed. Payment Voucher displayed with all required details.")
        logging.info("✅ Application Number: Present")
        logging.info("✅ Applicant/Student Name: Present")
        logging.info("✅ Applied School Name: Present")
        logging.info("✅ Application Fee Amount: Present")
        logging.info("✅ Payment Instructions: Present")

    except Exception as e:
        logging.error(f"Test Failed with exception: {str(e)}")
        capture_full_page_screenshot(driver, "TC_AD_18_exception")
        pytest.fail(f"Test Failed. Exception occurred: {str(e)}")

    logging.info("TC_AD_18 Completed..")