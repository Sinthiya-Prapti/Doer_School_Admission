import logging

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
        # first locate the container
        container = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "body > div:nth-child(13) > div:nth-child(1) > main:nth-child(2) > div:nth-child(1) > section:nth-child(3) > div:nth-child(1) > div:nth-child(2)"
            ))
        )

        # now find all child elements inside container
        admission_cards = container.find_elements(By.XPATH, "./*")  # all direct children
        # OR if they are all divs: container.find_elements(By.CSS_SELECTOR, "div")

        return len(admission_cards)

    def get_ongoing_admissions_message(self):
        message_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ongoing-admissions-message"))
        )
        return message_element.text

    def are_admission_cards_visible(self):
        try:
            admission_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body > div:nth-child(13) > div:nth-child(1) > main:nth-child(2) > div:nth-child(1) > section:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"))
            )
            return len(admission_cards) > 0
        except:
            return False

    def enter_school_name_search(self, school_name):
        """
        Fixed method for handling Ant Design dropdown with better error handling
        """
        try:
            # Step 1: Click dropdown selector to open it
            dropdown_selector = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-select-selector"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_selector)
            time.sleep(0.5)
            dropdown_selector.click()
            logging.info("Dropdown selector clicked successfully")

            # Step 2: Wait for dropdown to be in open state
            time.sleep(1)

            # Step 3: Instead of waiting for .ant-select-dropdown, directly find the input
            # The input should be available immediately after clicking
            try:
                # Try to find the search input directly
                search_input = self.driver.find_element(By.CSS_SELECTOR, "#rc_select_8")

                # Clear and enter text
                search_input.clear()
                time.sleep(0.3)
                search_input.send_keys(str(school_name))
                logging.info(f"Successfully typed '{school_name}' in search input")

            except Exception as input_error:
                logging.warning(f"Direct input method failed: {input_error}")
                # Fallback: Use JavaScript to set the input value
                js_script = f"""
                const input = document.querySelector('#rc_select_8');
                if (input) {{
                    input.value = '{school_name}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return 'Success';
                }}
                return 'Input not found';
                """
                result = self.driver.execute_script(js_script)
                logging.info(f"JavaScript input method result: {result}")

            # Step 4: Wait for options to load
            time.sleep(2)

            # Step 5: Try multiple approaches to find and click the first option
            option_found = False

            # Approach 1: Try the standard selector
            try:
                first_option = self.driver.find_element(By.CSS_SELECTOR, "div.ant-select-item-option-content")
                first_option.click()
                logging.info("Option selected using standard selector")
                option_found = True
            except:
                logging.warning("Standard option selector failed")

            # Approach 2: Try alternative selectors if first approach failed
            if not option_found:
                alternative_selectors = [
                    ".ant-select-item-option",
                    ".ant-select-item",
                    "[class*='ant-select-item']",
                    "[role='option']"
                ]

                for selector in alternative_selectors:
                    try:
                        option = self.driver.find_element(By.CSS_SELECTOR, selector)
                        option.click()
                        logging.info(f"Option selected using selector: {selector}")
                        option_found = True
                        break
                    except:
                        continue

            # Approach 3: Use JavaScript as final fallback
            if not option_found:
                js_click_script = """
                const options = document.querySelectorAll('[class*="ant-select-item"]');
                if (options.length > 0) {
                    options[0].click();
                    return 'Option clicked via JS';
                }
                return 'No options found';
                """
                result = self.driver.execute_script(js_click_script)
                logging.info(f"JavaScript option click result: {result}")
                option_found = "clicked" in result.lower()

            if not option_found:
                raise Exception("Could not find or click any dropdown option")

            # Step 6: Wait for dropdown to close
            time.sleep(1)

            logging.info("Dropdown interaction completed successfully")

        except Exception as e:
            logging.error(f"Error in dropdown selection: {str(e)}")

            # Enhanced debugging information
            try:
                # Check dropdown state
                dropdown = self.driver.find_element(By.CSS_SELECTOR, ".ant-select")
                dropdown_classes = dropdown.get_attribute("class")
                logging.error(f"Dropdown classes: {dropdown_classes}")

                # Check if input exists
                try:
                    input_element = self.driver.find_element(By.CSS_SELECTOR, "#rc_select_8")
                    logging.error(f"Input found: {input_element.is_displayed()}")
                except:
                    logging.error("Input element not found")

                # Check for dropdown options
                options = self.driver.find_elements(By.CSS_SELECTOR, "[class*='ant-select-item']")
                logging.error(f"Number of options found: {len(options)}")

            except Exception as debug_error:
                logging.error(f"Debug information gathering failed: {debug_error}")

            raise e


    def click_search_button(self):
        search_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='ant-btn css-1k708as ant-btn-primary ant-btn-color-primary ant-btn-variant-solid ant-btn-lg flex-1 bg-blue-600 hover:bg-blue-700 border-blue-600 hover:border-blue-700'] span[class='ant-btn-icon']"))
        )
        search_button.click()
        time.sleep(2)  # Wait for results to load

    def click_admission_navigation(self):
        search_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(13) > div:nth-child(1) > header:nth-child(1) > div:nth-child(1) > div:nth-child(1) > nav:nth-child(2) > a:nth-child(2)"))
        )
        search_button.click()
        time.sleep(2)  # Wait for results to load

    def get_displayed_school_names(self):
        try:
            # wait for container
            container = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/main/section/div[3]"))
            )

            # get all direct children of the container
            admission_cards = container.find_elements(By.XPATH, "./*")

            return len(admission_cards)
        except Exception as e:
            return 0

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
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='ant-btn css-1k708as ant-btn-default ant-btn-color-default ant-btn-variant-outlined ant-btn-lg text-gray-600 border-gray-300 hover:border-gray-400'] span"))
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
        """
        Enhanced method with multiple fallback strategies for clicking the Apply Now button
        """
        apply_button_selector = "body > div:nth-child(13) > div:nth-child(1) > main:nth-child(2) > section:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(3) > button:nth-child(2) > span:nth-child(2)"

        try:
            # Method 1: Wait and scroll to element first
            apply_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, apply_button_selector))
            )

            # Scroll the element into view
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                       apply_button)
            time.sleep(2)

            # Try normal click
            apply_button.click()
            print("Successfully clicked Apply Now button using normal click")

        except Exception as e1:
            print(f"Normal click failed: {e1}")

            try:
                # Method 2: JavaScript click
                apply_button = self.driver.find_element(By.CSS_SELECTOR, apply_button_selector)
                self.driver.execute_script("arguments[0].click();", apply_button)
                print("Successfully clicked Apply Now button using JavaScript click")

            except Exception as e2:
                print(f"JavaScript click failed: {e2}")

                try:
                    # Method 3: Click the parent button element instead of span
                    parent_button_selector = "body > div:nth-child(13) > div:nth-child(1) > main:nth-child(2) > section:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(3) > button:nth-child(2)"
                    parent_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, parent_button_selector))
                    )
                    parent_button.click()
                    print("Successfully clicked Apply Now button using parent button")

                except Exception as e3:
                    print(f"Parent button click failed: {e3}")

                    try:
                        # Method 4: Use ActionChains for more precise clicking
                        from selenium.webdriver.common.action_chains import ActionChains
                        apply_button = self.driver.find_element(By.CSS_SELECTOR, apply_button_selector)
                        ActionChains(self.driver).move_to_element(apply_button).click().perform()
                        print("Successfully clicked Apply Now button using ActionChains")

                    except Exception as e4:
                        print(f"ActionChains click failed: {e4}")
                        raise Exception("All click methods failed for Apply Now button")

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