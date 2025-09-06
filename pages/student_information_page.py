from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


class StudentInformationPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Student Personal Information Form Methods
    def enter_fullname(self, fullname):
        fullname_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#studentFullName"))
        )
        fullname_field.clear()
        fullname_field.send_keys(str(fullname))

    def select_gender(self, gender):
        if gender.lower() == "male":
            gender_radio = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#genderMale"))
            )
        else:
            gender_radio = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#genderFemale"))
            )
        gender_radio.click()

    def enter_date_of_birth(self, dob):
        dob_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#dateOfBirth"))
        )
        dob_field.clear()
        dob_field.send_keys(str(dob))

    def select_blood_group(self, blood_group):
        blood_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#bloodGroup"))
        )
        select = Select(blood_dropdown)
        select.select_by_visible_text(blood_group)

    def select_nationality(self, nationality):
        nationality_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#nationality"))
        )
        select = Select(nationality_dropdown)
        select.select_by_visible_text(nationality)

    def select_religion(self, religion):
        religion_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#religion"))
        )
        select = Select(religion_dropdown)
        select.select_by_visible_text(religion)

    def enter_contact_number(self, contact):
        contact_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#studentContact"))
        )
        contact_field.clear()
        contact_field.send_keys(str(contact))

    def enter_email(self, email):
        email_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#studentEmail"))
        )
        email_field.clear()
        email_field.send_keys(str(email))

    def enter_present_address(self, address):
        address_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#presentAddress"))
        )
        address_field.clear()
        address_field.send_keys(str(address))

    def click_save_continue_button(self):
        save_continue_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#saveContinueBtn"))
        )
        save_continue_button.click()
        time.sleep(2)

    # Additional Information Form Methods (TC_AD_11)
    def select_siblings_in_school(self, has_siblings):
        if has_siblings.lower() == "yes":
            siblings_radio = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#siblingsYes"))
            )
        else:
            siblings_radio = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#siblingsNo"))
            )
        siblings_radio.click()

    def enter_sibling_name(self, sibling_name):
        sibling_name_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#siblingName"))
        )
        sibling_name_field.clear()
        sibling_name_field.send_keys(str(sibling_name))

    def enter_relationship(self, relationship):
        relationship_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#relationship"))
        )
        relationship_field.clear()
        relationship_field.send_keys(str(relationship))

    def select_current_class(self, current_class):
        class_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#currentClass"))
        )
        select = Select(class_dropdown)
        select.select_by_visible_text(current_class)

    def enter_roll_number(self, roll_number):
        roll_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#rollNumber"))
        )
        roll_field.clear()
        roll_field.send_keys(str(roll_number))

    def enter_admission_year(self, admission_year):
        year_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#admissionYear"))
        )
        year_field.clear()
        year_field.send_keys(str(admission_year))

    # Validation Methods
    def get_validation_error_message(self, field_name):
        field_css_id = ""
        if field_name == "FullName":
            field_css_id = "#studentFullName"
        elif field_name == "Contact":
            field_css_id = "#studentContact"
        elif field_name == "Email":
            field_css_id = "#studentEmail"

        field_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, field_css_id))
        )
        return field_element.get_attribute("validationMessage")

    def get_success_message(self):
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#successMessage"))
            )
            return success_message.text
        except:
            return None

    def is_guardian_information_form_loaded(self):
        try:
            guardian_form = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#guardianInformationForm"))
            )
            return True
        except:
            return False

    def are_validation_errors_displayed(self):
        try:
            # Check for common validation error indicators
            error_messages = self.driver.find_elements(By.CSS_SELECTOR, ".error-message, .invalid-feedback")
            return len(error_messages) > 0
        except:
            return False