import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

from selenium.webdriver.support.wait import WebDriverWait


class PreviousSchoolPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def enter_school_name(self, school_name):
        school_name_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#previous_school"))
        )
        # scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", school_name_field)
        time.sleep(3)
        school_name_field.clear()
        school_name_field.send_keys(str(school_name))

    def select_board_curriculum(self, board_curriculum):
        # Click dropdown
        board_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#previous_curriculum"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", board_dropdown)
        time.sleep(0.5)
        board_dropdown.click()

        # Click desired option
        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(text(),'{board_curriculum}')]")
            )
        )
        option.click()

    def select_last_class_completed(self, last_class):
        class_dropdown = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#previous_class"))
        )
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", class_dropdown)
        class_dropdown.clear()
        class_dropdown.send_keys(str(last_class))

    def enter_school_address(self, school_address):
        address_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#previous_school_address"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", address_field)
        time.sleep(0.5)
        address_field.clear()
        address_field.send_keys(str(school_address))

    def click_save_continue_button(self):
        save_continue_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'] span:nth-child(2)"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_continue_button)
        time.sleep(0.5)
        save_continue_button.click()
        time.sleep(2)

    def get_success_message(self):
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class='ant-message ant-message-top css-1rfzxih'] span:nth-child(2)"))
            )
            return success_message.text
        except:
            return None
