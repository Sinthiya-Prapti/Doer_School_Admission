from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.screenshot_utils import capture_full_page_screenshot


class ApplicationReviewPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def check_confirmation_checkbox(self):
        # Wait for the label that toggles the checkbox
        checkbox_label = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-checkbox-label"))
        )

        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox_label)
        time.sleep(1)

        # Click the label to check the checkbox
        checkbox_label.click()
        time.sleep(1)

    def click_submit_button(self):
        submit_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ant-btn-primary"))
        )

        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)

        # Check if button is disabled
        is_disabled = submit_button.get_attribute("disabled")
        if is_disabled:
            # Scroll to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

            # Take screenshot
            capture_full_page_screenshot(self.driver, "admission_review_and_publish_validation_error")

            # Throw an exception
            raise Exception("Validation Error: Submit button is disabled. Please check the form.")

        # If not disabled, click the button
        submit_button.click()
        time.sleep(3)

    def get_completion_message(self):
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class='ant-message ant-message-top css-1rfzxih'] span:nth-child(2)"))
            )
            return success_message.text
        except:
            return None

    def is_proceed_to_payment_button_visible(self):
        try:
            # //button[@class='ant-btn css-1k708as ant-btn-primary ant-btn-color-primary ant-btn-variant-solid ant-btn-lg bg-[#1a5683] px-8 disabled:opacity-50 disabled:!text-white']
            proceed_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[@class='ant-btn css-1k708as ant-btn-primary ant-btn-color-primary ant-btn-variant-solid ant-btn-lg bg-[#1a5683] px-8 disabled:opacity-50 disabled:!text-white']"))
            )
            return proceed_button.is_displayed()
        except:
            return False

    def is_pay_later_button_visible(self):
        try:
            # body > div:nth-child(15) > div > div.ant-modal-wrap.ant-modal-centered > div > div:nth-child(1) > div > div > div > div.space-y-4.mb-6 > button.ant-btn.css-1k708as.ant-btn-primary.ant-btn-color-primary.ant-btn-variant-solid.w-full.h-14.bg-\[\#4a9b8e\].border-\[\#4a9b8e\].hover\:bg-\[\#3d8570\].hover\:border-\[\#3d8570\].text-white.font-semibold.text-lg.rounded-lg
            pay_later_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(15) > div > div.ant-modal-wrap.ant-modal-centered > div > div:nth-child(1) > div > div > div > div.space-y-4.mb-6 > button.ant-btn.css-1k708as.ant-btn-primary.ant-btn-color-primary.ant-btn-variant-solid.w-full.h-14.bg-\[\#4a9b8e\].border-\[\#4a9b8e\].hover\:bg-\[\#3d8570\].hover\:border-\[\#3d8570\].text-white.font-semibold.text-lg.rounded-lg"))
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