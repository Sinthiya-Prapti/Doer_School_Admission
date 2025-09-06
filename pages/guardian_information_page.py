from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


class GuardianInformationPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Father Information Methods
    def enter_father_fullname(self, fullname):
        father_name_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fatherFullName"))
        )
        father_name_field.clear()
        father_name_field.send_keys(str(fullname))

    def enter_father_contact(self, contact):
        father_contact_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fatherContact"))
        )
        father_contact_field.clear()
        father_contact_field.send_keys(str(contact))

    def enter_father_occupation(self, occupation):
        father_occupation_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fatherOccupation"))
        )
        father_occupation_field.clear()
        father_occupation_field.send_keys(str(occupation))

    def enter_father_nid(self, nid):
        father_nid_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fatherNID"))
        )
        father_nid_field.clear()
        father_nid_field.send_keys(str(nid))

    def enter_father_address(self, address):
        father_address_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#fatherAddress"))
        )
        father_address_field.clear()
        father_address_field.send_keys(str(address))

    # Mother Information Methods
    def enter_mother_fullname(self, fullname):
        mother_name_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#motherFullName"))
        )
        mother_name_field.clear()
        mother_name_field.send_keys(str(fullname))

    def enter_mother_contact(self, contact):
        mother_contact_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#motherContact"))
        )
        mother_contact_field.clear()
        mother_contact_field.send_keys(str(contact))

    def enter_mother_occupation(self, occupation):
        mother_occupation_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#motherOccupation"))
        )
        mother_occupation_field.clear()
        mother_occupation_field.send_keys(str(occupation))

    def enter_mother_nid(self, nid):
        mother_nid_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#motherNID"))
        )
        mother_nid_field.clear()
        mother_nid_field.send_keys(str(nid))

    def enter_mother_address(self, address):
        mother_address_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#motherAddress"))
        )
        mother_address_field.clear()
        mother_address_field.send_keys(str(address))

    # Legal Guardian Selection
    def select_legal_guardian(self, guardian_type):
        guardian_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#legalGuardian"))
        )
        select = Select(guardian_dropdown)
        select.select_by_visible_text(guardian_type)

    def click_save_continue_button(self):
        save_continue_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#guardianSaveContinueBtn"))
        )
        save_continue_button.click()
        time.sleep(2)

    # Validation and Navigation Methods
    def get_success_message(self):
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#guardianSuccessMessage"))
            )
            return success_message.text
        except:
            return None

    def is_previous_school_form_loaded(self):
        try:
            previous_school_form = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#previousSchoolForm"))
            )
            return True
        except:
            return False

    def get_validation_error_message(self, field_name):
        field_css_id = ""
        if field_name == "FatherFullName":
            field_css_id = "#fatherFullName"
        elif field_name == "FatherContact":
            field_css_id = "#fatherContact"
        elif field_name == "MotherFullName":
            field_css_id = "#motherFullName"
        elif field_name == "MotherContact":
            field_css_id = "#motherContact"

        field_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, field_css_id))
        )
        return field_element.get_attribute("validationMessage")