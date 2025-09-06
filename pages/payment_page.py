from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class PaymentPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def select_offline_payment_method(self):
        offline_payment_radio = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#offlinePayment"))
        )
        offline_payment_radio.click()
        time.sleep(1)

    def click_view_voucher_button(self):
        view_voucher_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#viewVoucherBtn"))
        )
        view_voucher_button.click()
        time.sleep(3)  # Wait for voucher to load

    def is_payment_voucher_displayed(self):
        try:
            voucher = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#paymentVoucher"))
            )
            return voucher.is_displayed()
        except:
            return False

    def get_application_number_from_voucher(self):
        try:
            app_number = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#voucherApplicationNumber"))
            )
            return app_number.text
        except:
            return None

    def get_applicant_name_from_voucher(self):
        try:
            applicant_name = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#voucherApplicantName"))
            )
            return applicant_name.text
        except:
            return None

    def get_school_name_from_voucher(self):
        try:
            school_name = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#voucherSchoolName"))
            )
            return school_name.text
        except:
            return None

    def get_application_fee_from_voucher(self):
        try:
            fee_amount = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#voucherFeeAmount"))
            )
            return fee_amount.text
        except:
            return None

    def get_payment_instructions_from_voucher(self):
        try:
            instructions = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#voucherPaymentInstructions"))
            )
            return instructions.text
        except:
            return None

    def get_voucher_details(self):
        voucher_details = {}

        try:
            voucher_details['application_number'] = self.get_application_number_from_voucher()
            voucher_details['applicant_name'] = self.get_applicant_name_from_voucher()
            voucher_details['school_name'] = self.get_school_name_from_voucher()
            voucher_details['fee_amount'] = self.get_application_fee_from_voucher()
            voucher_details['payment_instructions'] = self.get_payment_instructions_from_voucher()
        except Exception as e:
            voucher_details['error'] = str(e)

        return voucher_details

    def is_voucher_page_opened(self):
        # Check if we're on a voucher page/document
        try:
            # This could be a new tab/window or a modal
            current_url = self.driver.current_url
            return "voucher" in current_url.lower() or "payment" in current_url.lower()
        except:
            return False