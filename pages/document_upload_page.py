from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os


class DocumentUploadPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def upload_student_photo(self, photo_path):
        # Ensure the file path is absolute
        if not os.path.isabs(photo_path):
            photo_path = os.path.abspath(photo_path)

        photo_upload_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#studentPhotoUpload"))
        )
        photo_upload_field.send_keys(photo_path)
        time.sleep(1)

    def upload_birth_certificate(self, certificate_path):
        # Ensure the file path is absolute
        if not os.path.isabs(certificate_path):
            certificate_path = os.path.abspath(certificate_path)

        certificate_upload_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#birthCertificateUpload"))
        )
        certificate_upload_field.send_keys(certificate_path)
        time.sleep(1)

    def upload_academic_records(self, records_path):
        # Ensure the file path is absolute
        if not os.path.isabs(records_path):
            records_path = os.path.abspath(records_path)

        records_upload_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#academicRecordsUpload"))
        )
        records_upload_field.send_keys(records_path)
        time.sleep(1)

    def click_save_continue_button(self):
        save_continue_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#documentSaveContinueBtn"))
        )
        save_continue_button.click()
        time.sleep(2)

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