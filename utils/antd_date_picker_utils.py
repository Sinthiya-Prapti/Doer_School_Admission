import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class AntdDatePickerUtils:
    """Utility class for handling Ant Design date picker interactions"""

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def select_antd_date(self, date_field_selector, date_string, selector_type="css"):
        """
        Universal function to select date in Ant Design date picker

        Args:
            date_field_selector (str): CSS selector or XPath for the date input field
            date_string (str): Date in format 'YYYY-MM-DD' or 'DD/MM/YYYY' or 'MM/DD/YYYY'
            selector_type (str): 'css' or 'xpath' to specify selector type

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Parse date string to standard format
            year, month, day = self._parse_date_string(date_string)

            # Find and click the date input field
            if selector_type.lower() == "css":
                date_field = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, date_field_selector))
                )
            else:
                date_field = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, date_field_selector))
                )

            # Clear any existing value first
            self._clear_date_field(date_field)

            # Click to open date picker
            date_field.click()
            logging.info(f"Date picker opened for selector: {date_field_selector}")
            time.sleep(1)

            # Try multiple methods to select the date
            methods = [
                self._method_direct_input,
                self._method_calendar_navigation,
                self._method_send_keys_formatted
            ]

            for i, method in enumerate(methods, 1):
                try:
                    success = method(date_field, year, month, day, date_string)
                    if success:
                        logging.info(f"Date selected successfully using method {i}")
                        return True
                except Exception as e:
                    logging.warning(f"Method {i} failed: {str(e)}")
                    continue

            logging.error("All date selection methods failed")
            return False

        except Exception as e:
            logging.error(f"Error in select_antd_date: {str(e)}")
            return False

    def _parse_date_string(self, date_string):
        """Parse various date formats to year, month, day integers"""
        try:
            # Handle YYYY-MM-DD format
            if "-" in date_string and len(date_string.split("-")[0]) == 4:
                year, month, day = date_string.split("-")
                return int(year), int(month), int(day)

            # Handle DD/MM/YYYY format
            elif "/" in date_string:
                parts = date_string.split("/")
                if len(parts[2]) == 4:  # DD/MM/YYYY
                    day, month, year = parts
                else:  # MM/DD/YYYY
                    month, day, year = parts
                return int(year), int(month), int(day)

            else:
                raise ValueError(f"Unsupported date format: {date_string}")

        except Exception as e:
            logging.error(f"Error parsing date string '{date_string}': {str(e)}")
            raise

    def _clear_date_field(self, date_field):
        """Clear the date field using multiple methods"""
        try:
            # Method 1: Select all and delete
            date_field.click()
            time.sleep(0.5)
            date_field.send_keys(Keys.CONTROL + "a")
            date_field.send_keys(Keys.DELETE)

            # Method 2: Clear using Selenium clear()
            date_field.clear()

            time.sleep(0.5)
        except Exception as e:
            logging.warning(f"Error clearing date field: {str(e)}")

    def _method_direct_input(self, date_field, year, month, day, original_date):
        """Method 1: Direct input with various formats"""
        formats_to_try = [
            f"{day:02d}/{month:02d}/{year}",  # DD/MM/YYYY
            f"{month:02d}/{day:02d}/{year}",  # MM/DD/YYYY
            f"{year}-{month:02d}-{day:02d}",  # YYYY-MM-DD
            f"{day}/{month}/{year}",  # D/M/YYYY
            original_date  # Original format
        ]

        for date_format in formats_to_try:
            try:
                date_field.clear()
                date_field.send_keys(date_format)
                date_field.send_keys(Keys.ENTER)
                time.sleep(1)

                # Check if date was accepted
                if self._verify_date_selection(date_field, year, month, day):
                    return True

            except Exception:
                continue

        return False

    def _method_calendar_navigation(self, date_field, year, month, day, original_date):
        """Method 2: Navigate through calendar UI"""
        try:
            # Navigate to correct year
            self._navigate_to_year(year)
            time.sleep(0.5)

            # Navigate to correct month
            self._navigate_to_month(month)
            time.sleep(0.5)

            # Select the day
            return self._select_day(day)

        except Exception as e:
            logging.warning(f"Calendar navigation failed: {str(e)}")
            return False

    def _method_send_keys_formatted(self, date_field, year, month, day, original_date):
        """Method 3: Send keys with tab navigation"""
        try:
            date_field.clear()
            time.sleep(0.5)

            # Try sending day, month, year with tabs
            date_field.send_keys(f"{day:02d}")
            date_field.send_keys(Keys.TAB)
            date_field.send_keys(f"{month:02d}")
            date_field.send_keys(Keys.TAB)
            date_field.send_keys(str(year))
            date_field.send_keys(Keys.ENTER)

            time.sleep(1)
            return self._verify_date_selection(date_field, year, month, day)

        except Exception:
            return False

    def _navigate_to_year(self, target_year):
        """Navigate to the target year in calendar"""
        try:
            # Click on year selector
            year_selectors = [
                "//button[contains(@class, 'ant-picker-year-btn')]",
                "//span[contains(@class, 'ant-picker-year-btn')]",
                "//div[contains(@class, 'ant-picker-header-year-btn')]"
            ]

            year_element = None
            for selector in year_selectors:
                try:
                    year_element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue

            if year_element:
                year_element.click()
                time.sleep(0.5)

                # Find and click the target year
                year_xpath = f"//div[contains(@class, 'ant-picker-year-panel')]//div[text()='{target_year}']"
                target_year_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, year_xpath))
                )
                target_year_element.click()
                time.sleep(0.5)

        except Exception as e:
            logging.warning(f"Year navigation failed: {str(e)}")

    def _navigate_to_month(self, target_month):
        """Navigate to the target month in calendar"""
        try:
            # Click on month selector
            month_selectors = [
                "//button[contains(@class, 'ant-picker-month-btn')]",
                "//span[contains(@class, 'ant-picker-month-btn')]",
                "//div[contains(@class, 'ant-picker-header-month-btn')]"
            ]

            month_element = None
            for selector in month_selectors:
                try:
                    month_element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue

            if month_element:
                month_element.click()
                time.sleep(0.5)

                # Month names in English (adjust if your app uses different language)
                month_names = [
                    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                ]

                month_name = month_names[target_month - 1]
                month_xpath = f"//div[contains(@class, 'ant-picker-month-panel')]//div[contains(text(), '{month_name}')]"

                target_month_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, month_xpath))
                )
                target_month_element.click()
                time.sleep(0.5)

        except Exception as e:
            logging.warning(f"Month navigation failed: {str(e)}")

    def _select_day(self, target_day):
        """Select the target day from calendar"""
        try:
            # Try different day selection approaches
            day_selectors = [
                f"//td[contains(@class, 'ant-picker-cell')]//div[text()='{target_day}' and not(ancestor::td[contains(@class, 'ant-picker-cell-disabled')])]",
                f"//div[contains(@class, 'ant-picker-cell-inner') and text()='{target_day}']",
                f"//td[@title and contains(@class, 'ant-picker-cell')]//div[text()='{target_day}']"
            ]

            for selector in day_selectors:
                try:
                    day_element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    day_element.click()
                    time.sleep(0.5)
                    return True
                except:
                    continue

            return False

        except Exception as e:
            logging.warning(f"Day selection failed: {str(e)}")
            return False

    def _verify_date_selection(self, date_field, year, month, day):
        """Verify if the date was successfully selected"""
        try:
            # Get the current value of the date field
            current_value = date_field.get_attribute("value")

            if not current_value:
                return False

            # Check if the date components are present in the field value
            date_components = [str(year), f"{month:02d}", f"{day:02d}", str(month), str(day)]

            # At least 3 components should be present (year, month, day in some format)
            matches = sum(1 for component in date_components if component in current_value)

            return matches >= 3

        except Exception:
            return False


# Convenience function for easy import
def select_antd_date(driver, wait, date_field_selector, date_string, selector_type="css"):
    """
    Convenience function to select date in Ant Design date picker

    Args:
        driver: WebDriver instance
        wait: WebDriverWait instance
        date_field_selector (str): CSS selector or XPath for the date input field
        date_string (str): Date in format 'YYYY-MM-DD'
        selector_type (str): 'css' or 'xpath'

    Returns:
        bool: True if successful, False otherwise
    """
    date_utils = AntdDatePickerUtils(driver, wait)
    return date_utils.select_antd_date(date_field_selector, date_string, selector_type)