from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os

from utils.screenshot_utils import capture_full_page_screenshot


class DocumentUploadPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

        # --- Check if form is loaded ---
        def is_document_upload_form_loaded(self):
            try:
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "h2[class='text-xl font-semibold text-[#1a5683] mb-6']"))
                )
                return True
            except:
                return False

        # --- Upload documents ---
        def upload_student_documents(self, photo_path, birth_certificate_path, previous_records_path):
            if not self.is_document_upload_form_loaded():
                raise Exception("Document upload form not loaded!")

            # --- Student Photo ---
            photo_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "div[id='student_photo_url'] div[class='p-4 flex flex-col items-center justify-center h-full']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", photo_input)
            time.sleep(0.5)
            photo_input.send_keys(os.path.abspath(r"C:\Users\sinth\Documents\photo.jpg"))

            # --- Birth Certificate ---
            birth_cert_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "body > div:nth-child(14) > div:nth-child(1) > main:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > form:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > div:nth-child(1) > span:nth-child(1) > div:nth-child(2) > div:nth-child(1)"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", birth_cert_input)
            time.sleep(0.5)
            birth_cert_input.send_keys(os.path.abspath(r"C:\Users\sinth\Documents\photo.jpg"))

            # --- Previous Academic Records ---
            previous_records_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "body > div:nth-child(14) > div:nth-child(1) > main:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > form:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > div:nth-child(1) > span:nth-child(1) > div:nth-child(2) > div:nth-child(1)"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", previous_records_input)
            time.sleep(0.5)
            previous_records_input.send_keys(os.path.abspath(r"C:\Users\sinth\Documents\photo.jpg"))

            # --- Submit Button ---
            submit_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "body > div:nth-child(14) > div:nth-child(1) > main:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > form:nth-child(2) > div:nth-child(2) > button:nth-child(2) > span:nth-child(2)"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(0.5)
            submit_btn.click()

            # --- Verify Upload Success ---
            try:
                success_msg = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#uploadSuccessMessage"))
                )
                print("Documents uploaded successfully!")
                return True
            except:
                print("Document upload failed!")
                return False

    def upload_student_photo(self, photo_path):
        if not os.path.isabs(photo_path):
            photo_path = os.path.abspath(photo_path)

        # Scroll the visible wrapper into view
        wrapper = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#student_photo_url"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", wrapper)
        time.sleep(1)

        # Wait for the file input to be present
        photo_upload_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#student_photo_url input[type='file']"))
        )

        # Upload file
        photo_upload_field.send_keys(photo_path)

        # Optional: wait until some element appears indicating upload success
        time.sleep(3)

    def upload_birth_certificate(self, certificate_path):
        # Ensure the file path is absolute
        if not os.path.isabs(certificate_path):
            certificate_path = os.path.abspath(certificate_path)

        # Scroll the visible wrapper into view
        wrapper = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#birth_certificate_url"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", wrapper)
        time.sleep(1)

        certificate_upload_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#birth_certificate_url > span > div > span > input[type=file]"))
        )

        certificate_upload_field.send_keys(certificate_path)
        time.sleep(1)

    def upload_academic_records(self, records_path):
        # Ensure the file path is absolute
        if not os.path.isabs(records_path):
            records_path = os.path.abspath(records_path)

        # Scroll the visible wrapper into view
        wrapper = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#academic_records_url"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", wrapper)
        time.sleep(1)

        records_upload_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#academic_records_url > span > div > span > input[type=file]"))
        )

        records_upload_field.send_keys(records_path)
        time.sleep(3)

    def click_save_continue_button(self):
        # Wait for the submit button to be clickable
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
            capture_full_page_screenshot(self.driver, "validation_error_admission_form_final_submission")

            # Throw an exception
            raise Exception("Validation Error: Submit button is disabled. Please check the form.")

        # If not disabled, click the button
        submit_button.click()
        time.sleep(3)  # Wait for popup to appear

    def get_success_message(self):
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#documentSuccessMessage"))
            )
            return success_message.text
        except:
            return None

    def is_review_page_loaded(self):
        try:
            review_page = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#reviewPage"))
            )
            return True
        except:
            return False

    def get_upload_error_message(self, document_type):
        error_css_id = ""
        if document_type == "photo":
            error_css_id = "#photoUploadError"
        elif document_type == "certificate":
            error_css_id = "#certificateUploadError"
        elif document_type == "records":
            error_css_id = "#recordsUploadError"

        try:
            error_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, error_css_id))
            )
            return error_element.text
        except:
            return None

    def is_file_uploaded_successfully(self, document_type):
        success_indicator_css = ""
        if document_type == "photo":
            success_indicator_css = "#photoUploadSuccess"
        elif document_type == "certificate":
            success_indicator_css = "#certificateUploadSuccess"
        elif document_type == "records":
            success_indicator_css = "#recordsUploadSuccess"

        try:
            success_indicator = self.driver.find_element(By.CSS_SELECTOR, success_indicator_css)
            return success_indicator.is_displayed()
        except:
            return False





















