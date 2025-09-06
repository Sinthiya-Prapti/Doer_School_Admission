from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class ApplicationReviewPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def check_confirmation_checkbox(self):
        confirmation_checkbox = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#confirmationCheckbox"))
        )
        if not confirmation_checkbox.is_selected():
            confirmation_checkbox.click()
        time.sleep(1)

    def click_submit_button(self):
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#submitApplicationBtn"))
        )
        submit_button.click()
        time.sleep(3)  # Wait for popup to appear

    def get_completion_message(self):
        try:
            completion_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#completionMessage"))
            )
            return completion_message.text
        except:
            return None

    def is_proceed_to_payment_button_visible(self):
        try:
            proceed_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#proceedToPaymentBtn"))
            )
            return proceed_button.is_displayed()
        except:
            return False

    def is_pay_later_button_visible(self):
        try:
            pay_later_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#payLaterBtn"))
            )
            return pay_later_button.is_displayed()
        except:
            return False

    def get_payment_warning_note(self):
        try:
            warning_note = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#paymentWarningNote"))
            )
            return warning_note.text
        except:
            return None

    def click_proceed_to_payment_button(self):
        proceed_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#proceedToPaymentBtn"))
        )
        proceed_button.click()
        time.sleep(2)

    def click_pay_later_button(self):
        pay_later_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#payLaterBtn"))
        )
        pay_later_button.click()
        time.sleep(2)

    def is_payment_page_loaded(self):
        try:
            payment_page = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#paymentPage"))
            )
            return True
        except:
            return False

    def get_confirmation_popup_elements(self):
        popup_elements = {}

        try:
            popup_elements['completion_message'] = self.get_completion_message()
            popup_elements['proceed_to_payment_visible'] = self.is_proceed_to_payment_button_visible()
            popup_elements['pay_later_visible'] = self.is_pay_later_button_visible()
            popup_elements['warning_note'] = self.get_payment_warning_note()
        except Exception as e:
            popup_elements['error'] = str(e)

        return popup_elements