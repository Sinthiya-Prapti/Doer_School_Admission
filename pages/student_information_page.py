import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from utils.antd_date_picker_utils import select_antd_date



class StudentInformationPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # Student Personal Information Form Methods
    def enter_fullname(self, fullname):
        fullname_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#full_name"))
        )
        fullname_field.clear()
        fullname_field.send_keys(str(fullname))

    def select_gender(self, gender):
        # 1. Click dropdown to open gender list
        dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#gender"))
            # <-- এখানে আপনার আসল gender dropdown field এর selector দিতে হবে
        )
        dropdown.click()

        # 2. Wait for list and select based on given gender
        gender = gender.lower()
        if gender == "male":
            option = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[title='Male'] div.ant-select-item-option-content"))
            )
        elif gender == "female":
            option = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[title='Female'] div.ant-select-item-option-content"))
            )
        else:
            option = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[title='Others'] div.ant-select-item-option-content"))
            )

        option.click()
    #select date of birth......................
    def enter_date_of_birth(self, dob):
        """
        Select date from calendar picker using the common utility
        dob format: 'YYYY-MM-DD' e.g., '2010-09-15'
        """
        fullname_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#date_of_birth"))
        )
        fullname_field.clear()
        fullname_field.send_keys(str(dob))

    def navigate_to_year_month(self, target_year, target_month):
        """
        Navigate calendar to specific year and month
        """
        target_year = int(target_year)

        try:
            # Click on month/year header to open year/month selector
            month_year_header = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-picker-header-view button"))
            )
            month_year_header.click()
            time.sleep(0.5)

            # Select year first
            self.select_year(target_year)

            # Select month
            self.select_month(target_month)

        except Exception as e:
            logging.error(f"Error navigating to year/month: {str(e)}")
            # Try using navigation arrows as fallback
            self.navigate_with_arrows(target_year, target_month)

    def select_year(self, target_year):
        """
        Select specific year from year picker
        """
        try:
            # Look for year in the year grid
            year_selector = f"//td[@title='{target_year}']/div"
            year_cell = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, year_selector))
            )
            year_cell.click()
            logging.info(f"Selected year: {target_year}")
            time.sleep(0.5)

        except:
            # If year not visible, try clicking year decade selector
            try:
                decade_selector = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-picker-decade-btn"))
                )
                decade_selector.click()
                time.sleep(0.5)

                # Find and click the decade containing target year
                decade_start = (target_year // 10) * 10
                decade_selector_xpath = f"//td[@title='{decade_start}-{decade_start + 9}']/div"
                decade_cell = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, decade_selector_xpath))
                )
                decade_cell.click()
                time.sleep(0.5)

                # Now select the year
                year_selector = f"//td[@title='{target_year}']/div"
                year_cell = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, year_selector))
                )
                year_cell.click()
                logging.info(f"Selected year: {target_year}")

            except Exception as e:
                logging.error(f"Error selecting year {target_year}: {str(e)}")
                raise e

    def select_month(self, target_month):
        """
        Select specific month from month picker
        """
        try:
            # Month names mapping
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            month_name = months[target_month - 1]

            # Look for month cell
            month_selector = f"//td[@title='{month_name}']/div"
            month_cell = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, month_selector))
            )
            month_cell.click()
            logging.info(f"Selected month: {month_name}")
            time.sleep(0.5)

        except Exception as e:
            logging.error(f"Error selecting month {target_month}: {str(e)}")
            raise e

    def navigate_with_arrows(self, target_year, target_month):
        """
        Fallback method: Use navigation arrows to reach target date
        """
        try:
            # Get current displayed month/year
            current_header = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-picker-header-view"))
            ).text

            # This is a simplified approach - you might need to adjust based on actual header format
            # Click prev/next arrows until we reach target month/year
            max_attempts = 50
            attempts = 0

            while attempts < max_attempts:
                current_header = self.driver.find_element(By.CSS_SELECTOR, ".ant-picker-header-view").text

                if str(target_year) in current_header and str(target_month).zfill(2) in current_header:
                    break

                # Click next or prev arrow based on comparison
                if target_year > int(current_header.split()[-1]):  # Assuming year is last
                    next_button = self.driver.find_element(By.CSS_SELECTOR, ".ant-picker-header-next-btn")
                    next_button.click()
                else:
                    prev_button = self.driver.find_element(By.CSS_SELECTOR, ".ant-picker-header-prev-btn")
                    prev_button.click()

                time.sleep(0.3)
                attempts += 1

            logging.info(f"Navigated to target month/year using arrows")

        except Exception as e:
            logging.error(f"Error navigating with arrows: {str(e)}")
            raise e

    # def select_blood_group(self, blood_group):
    #     blood_dropdown = self.wait.until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "#bloodGroup"))
    #     )
    #     select = Select(blood_dropdown)
    #     select.select_by_visible_text(blood_group)

    def select_nationality(self, nationality):
        # 1. Click dropdown to open nationality list
        dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#nationality"))
        )
        dropdown.click()

        # 2. Select the option by visible title/text
        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"div[title='{nationality}'] div.ant-select-item-option-content")
            )
        )
        option.click()

    def select_religion(self, religion):
        # 1. Click religion dropdown
        dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#religion"))
        )
        dropdown.click()

        # 2. Select option from opened list based on test data
        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"div[title='{religion}'] div.ant-select-item-option-content")
            )
        )
        option.click()

    def enter_contact_number(self, contact):
        contact_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#phone"))
        )
        contact_field.clear()
        contact_field.send_keys(str(contact))

    def enter_email(self, email):
        email_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#email"))
        )
        email_field.clear()
        email_field.send_keys(str(email))

    def enter_present_address(self, address):
        address_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#present_address_line"))
        )
        address_field.clear()
        address_field.send_keys(str(address))

    def click_save_continue_button(self):
        save_continue_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit'] span:nth-child(2)"))
        )

        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_continue_button)
        time.sleep(1)

        # Wait until clickable & then click
        clickable_btn = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit'] span:nth-child(2)")
        ))
        clickable_btn.click()
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