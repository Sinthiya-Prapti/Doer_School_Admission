from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


class PreviousSchoolPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def enter_school_name(self, school_name):
        school_name_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#previousSchoolName"))
        )
        school_name_field.clear()
        school_name_field.send_keys(str(school_name))

    def select_board_curriculum(self, board_curriculum):
        board_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#boardCurriculum"))
        )
        select = Select(board_dropdown)
        select.select_by_visible_text(board_curriculum)

    def select_last_class_completed(self, last_class):
        class_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#lastClassCompleted"))
        )
        select = Select(class_dropdown)
        select.select_by_visible_text(last_class)

    def enter_school_address(self, school_address):
        address_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#previousSchoolAddress"))
        )
        address_field.clear()
        address_field.send_keys(str(school_address))

    def click_save_continue_button(self):
        save_continue_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#previousSchoolSaveContinueBtn"))
        )
        save_continue_button.click()
        time.sleep(2)

    def get_success_message(self):
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#previousSchoolSuccessMessage"))
            )
            return success_message.text
        except:
            return None

    def is_document_upload_form_loaded(self):
        try:
            document_upload_form = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#documentUploadForm"))
            )
            return True
        except:
            return False