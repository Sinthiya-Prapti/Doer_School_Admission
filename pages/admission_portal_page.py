from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


class AdmissionPortalPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # TC_AD_01 - Check admission cards display
    def get_admission_cards_count(self):
        admission_cards = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".admission-card"))
        )
        return len(admission_cards)

    def get_ongoing_admissions_message(self):
        message_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ongoing-admissions-message"))
        )
        return message_element.text

    def are_admission_cards_visible(self):
        try:
            admission_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".admission-card"))
            )
            return len(admission_cards) > 0
        except:
            return False

    # TC_AD_02 - Search by school name
    def enter_school_name_search(self, school_name):
        search_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#schoolNameSearch"))
        )
        search_field.clear()
        search_field.send_keys(str(school_name))

    def click_search_button(self):
        search_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-button"))
        )
        search_button.click()
        time.sleep(2)  # Wait for results to load

    def get_displayed_school_names(self):
        school_name_elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".school-name"))
        )
        return [element.text for element in school_name_elements]

    # TC_AD_03 - Filter by campus
    def select_campus_filter(self, campus_name):
        campus_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#campusFilter"))
        )
        select = Select(campus_dropdown)
        select.select_by_visible_text(campus_name)

    def get_displayed_campus_names(self):
        campus_elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".campus-name"))
        )
        return [element.text for element in campus_elements]

    # TC_AD_04 - Filter by class
    def select_class_filter(self, class_name):
        class_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#classFilter"))
        )
        select = Select(class_dropdown)
        select.select_by_visible_text(class_name)

    def get_displayed_classes(self):
        class_elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".class-name"))
        )
        return [element.text for element in class_elements]

    # TC_AD_05 - Filter by medium
    def select_medium_filter(self, medium_name):
        medium_dropdown = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mediumFilter"))
        )
        select = Select(medium_dropdown)
        select.select_by_visible_text(medium_name)

    def get_displayed_mediums(self):
        medium_elements = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".medium-name"))
        )
        return [element.text for element in medium_elements]

    # TC_AD_06 - Clear all filters
    def click_clear_filters_button(self):
        clear_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".clear-filters-button"))
        )
        clear_button.click()
        time.sleep(2)  # Wait for filters to reset

    def get_total_admissions_count(self):
        admission_cards = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".admission-card"))
        )
        return len(admission_cards)

    # TC_AD_07 - Apply Now button
    def click_apply_now_button(self):
        apply_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".apply-now-button"))
        )
        apply_button.click()
        time.sleep(3)  # Wait for navigation

    def is_student_information_form_loaded(self):
        try:
            student_form = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#studentInformationForm"))
            )
            return True
        except:
            return False

    # TC_AD_08 - Download circular
    def click_download_circular_button(self):
        download_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".download-circular-button"))
        )
        download_button.click()
        time.sleep(3)  # Wait for download to start

    def is_circular_downloaded(self, download_path="Downloads"):
        # This would need to check the downloads folder
        # Implementation depends on browser settings and OS
        import os
        import glob

        # Check for recent PDF downloads
        pdf_files = glob.glob(os.path.join(download_path, "*.pdf"))
        if pdf_files:
            # Check if any PDF was downloaded recently (within last 10 seconds)
            import time
            current_time = time.time()
            for pdf_file in pdf_files:
                if current_time - os.path.getmtime(pdf_file) < 10:
                    return True
        return False