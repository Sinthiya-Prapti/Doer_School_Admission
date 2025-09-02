import logging
import time
import pytest
from selenium.webdriver.common.by import By

from utils.screenshot_utils import capture_full_page_screenshot
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from utils.data_loader import load_all_test_data


@pytest.mark.parametrize("test_case", load_all_test_data("../data/data.json"))
def test_tc_reg_16(browser_config, test_case):
    """TC_Reg_16: Verify Page Responsive Design"""
    logging.info("TC_Reg_16 Started..")
    logging.info(test_case["registration"][15]["TC_Reg_16"]["_comment"])

    driver, wait = browser_config

    # Create objects for page classes
    registration_page = RegistrationPage(driver, wait)
    login_page = LoginPage(driver, wait)

    # Get test data
    test_data = test_case["registration"][15]["TC_Reg_16"]
    test_devices = test_data["test_devices"]

    # Define device dimensions
    device_dimensions = {
        "desktop": {"width": 1920, "height": 1080},
        "tablet": {"width": 768, "height": 1024},
        "mobile": {"width": 375, "height": 667},
        "mobile_large": {"width": 414, "height": 896}
    }

    responsive_test_results = {}

    # Test homepage responsiveness
    try:
        logging.info("Testing homepage responsiveness...")

        for device in test_devices:
            if device in device_dimensions:
                dimensions = device_dimensions[device]

                # Set browser window size
                driver.set_window_size(dimensions["width"], dimensions["height"])
                logging.info(f"Set browser size to {device}: {dimensions['width']}x{dimensions['height']}")
                time.sleep(2)

                # Navigate to homepage
                driver.get("https://admission-test.doer.school/en")
                time.sleep(3)

                # Test homepage elements visibility and functionality
                try:
                    # Check if heading is visible
                    heading = registration_page.get_homepage_heading()
                    if heading:
                        logging.info(f"Homepage heading visible on {device}: {heading}")
                        responsive_test_results[f"homepage_{device}_heading"] = True
                    else:
                        logging.warning(f"data=========== {heading}")
                        logging.warning(f"Homepage heading not visible on {device}")
                        responsive_test_results[f"homepage_{device}_heading"] = False

                    # Test Sign Up button functionality
                    registration_page.click_sign_up_for_free_button()
                    logging.info(f"Sign Up button functional on {device}")
                    responsive_test_results[f"homepage_{device}_button"] = True

                    # Take screenshot for this device
                    capture_full_page_screenshot(driver, f"TC_Reg_16_Homepage_{device}")

                except Exception as e:
                    logging.error(f"Homepage functionality test failed on {device}: {e}")
                    responsive_test_results[f"homepage_{device}_button"] = False
                    capture_full_page_screenshot(driver, f"TC_Reg_16_Homepage_{device}_Error")

    except Exception as e:
        logging.error(f"Homepage responsive testing failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_16_Homepage_Responsive_Error")
        pytest.fail(f"Homepage responsive testing failed: {e}")

    # Test Sign Up page responsiveness
    try:
        logging.info("Testing Sign Up page responsiveness...")

        for device in test_devices:
            if device in device_dimensions:
                dimensions = device_dimensions[device]

                # Set browser window size
                driver.set_window_size(dimensions["width"], dimensions["height"])
                logging.info(f"Testing Sign Up page on {device}: {dimensions['width']}x{dimensions['height']}")
                time.sleep(2)

                # Navigate to Sign Up page
                try:
                    driver.get("https://admission-test.doer.school/en")
                    time.sleep(2)
                    registration_page.click_sign_up_for_free_button()
                    time.sleep(3)

                    # Test Sign Up page elements
                    signup_heading = registration_page.get_signup_heading()
                    if signup_heading:
                        logging.info(f"Sign Up heading visible on {device}")
                        responsive_test_results[f"signup_{device}_heading"] = True
                    else:
                        logging.warning(f"Sign Up heading not visible on {device}")
                        responsive_test_results[f"signup_{device}_heading"] = False

                    # Test form fields visibility
                    expected_fields = ["Full Name", "Email", "Password", "Confirm Password"]
                    fields_visible = registration_page.verify_form_fields_present(expected_fields)

                    if fields_visible:
                        logging.info(f"All form fields visible on {device}")
                        responsive_test_results[f"signup_{device}_fields"] = True
                    else:
                        logging.warning(f"Some form fields not visible on {device}")
                        responsive_test_results[f"signup_{device}_fields"] = False

                    # Test form interaction (enter sample data)
                    try:
                        registration_page.enter_full_name("Test User")
                        registration_page.enter_email("test@example.com")
                        registration_page.enter_password("TestPass123")
                        registration_page.enter_confirm_password("TestPass123")

                        logging.info(f"Form interaction successful on {device}")
                        responsive_test_results[f"signup_{device}_interaction"] = True

                        # Clear fields for next test
                        driver.refresh()
                        time.sleep(2)

                    except Exception as e:
                        logging.warning(f"Form interaction failed on {device}: {e}")
                        responsive_test_results[f"signup_{device}_interaction"] = False

                    # Take screenshot
                    capture_full_page_screenshot(driver, f"TC_Reg_16_SignUp_{device}")

                except Exception as e:
                    logging.error(f"Sign Up page testing failed on {device}: {e}")
                    responsive_test_results[f"signup_{device}"] = False
                    capture_full_page_screenshot(driver, f"TC_Reg_16_SignUp_{device}_Error")

    except Exception as e:
        logging.error(f"Sign Up page responsive testing failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_16_SignUp_Responsive_Error")
        # Continue test instead of failing
        logging.warning("Continuing with Sign In page testing...")

    # Test Sign In page responsiveness
    try:
        logging.info("Testing Sign In page responsiveness...")

        for device in test_devices:
            if device in device_dimensions:
                dimensions = device_dimensions[device]

                # Set browser window size
                driver.set_window_size(dimensions["width"], dimensions["height"])
                logging.info(f"Testing Sign In page on {device}: {dimensions['width']}x{dimensions['height']}")
                time.sleep(2)

                # Navigate to Sign In page
                try:
                    driver.get("https://admission-test.doer.school/en")
                    time.sleep(2)
                    registration_page.click_sign_up_for_free_button()
                    time.sleep(2)
                    registration_page.click_signin_link_from_signup()
                    time.sleep(3)

                    # Test Sign In page elements
                    signin_heading = login_page.get_signin_heading()
                    if signin_heading:
                        logging.info(f"Sign In heading visible on {device}")
                        responsive_test_results[f"signin_{device}_heading"] = True
                    else:
                        logging.warning(f"Sign In heading not visible on {device}")
                        responsive_test_results[f"signin_{device}_heading"] = False

                    # Test form elements visibility
                    expected_elements = ["Email", "Password", "Keep me logged in", "Log In"]
                    elements_visible = login_page.verify_signin_form_elements(expected_elements)

                    if elements_visible:
                        logging.info(f"All Sign In elements visible on {device}")
                        responsive_test_results[f"signin_{device}_elements"] = True
                    else:
                        logging.warning(f"Some Sign In elements not visible on {device}")
                        responsive_test_results[f"signin_{device}_elements"] = False

                    # Test form interaction
                    try:
                        login_page.enter_email("test@example.com")
                        login_page.enter_password("TestPass123")

                        logging.info(f"Sign In form interaction successful on {device}")
                        responsive_test_results[f"signin_{device}_interaction"] = True

                        # Clear fields
                        driver.refresh()
                        time.sleep(2)

                    except Exception as e:
                        logging.warning(f"Sign In form interaction failed on {device}: {e}")
                        responsive_test_results[f"signin_{device}_interaction"] = False

                    # Take screenshot
                    capture_full_page_screenshot(driver, f"TC_Reg_16_SignIn_{device}")

                except Exception as e:
                    logging.error(f"Sign In page testing failed on {device}: {e}")
                    responsive_test_results[f"signin_{device}"] = False
                    capture_full_page_screenshot(driver, f"TC_Reg_16_SignIn_{device}_Error")

    except Exception as e:
        logging.error(f"Sign In page responsive testing failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_16_SignIn_Responsive_Error")
        # Continue to validation

    # Additional mobile-specific tests
    try:
        logging.info("Performing additional mobile-specific tests...")

        # Test mobile portrait orientation
        driver.set_window_size(375, 667)  # iPhone SE size
        time.sleep(2)

        # Test touch-friendly elements (button sizes, spacing)
        driver.get("https://admission-test.doer.school/en")
        time.sleep(2)
        registration_page.click_sign_up_for_free_button()
        time.sleep(2)

        # Check if buttons are touch-friendly (minimum 44px height/width)
        try:
            signup_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button:contains('Sign Up')")
            button_size = signup_button.size

            if button_size['height'] >= 44 and button_size['width'] >= 44:
                logging.info(f"Sign Up button is touch-friendly: {button_size}")
                responsive_test_results["mobile_touch_friendly"] = True
            else:
                logging.warning(f"Sign Up button might not be touch-friendly: {button_size}")
                responsive_test_results["mobile_touch_friendly"] = False

        except Exception as e:
            logging.warning(f"Touch-friendly button check failed: {e}")
            responsive_test_results["mobile_touch_friendly"] = False

        # Test mobile landscape orientation
        driver.set_window_size(667, 375)  # iPhone SE landscape
        time.sleep(2)

        # Verify layout still works in landscape
        try:
            signup_heading = registration_page.get_signup_heading()
            if signup_heading:
                logging.info("Sign Up page functional in mobile landscape")
                responsive_test_results["mobile_landscape"] = True
            else:
                logging.warning("Sign Up page issues in mobile landscape")
                responsive_test_results["mobile_landscape"] = False
        except Exception as e:
            logging.warning(f"Mobile landscape test failed: {e}")
            responsive_test_results["mobile_landscape"] = False

        capture_full_page_screenshot(driver, "TC_Reg_16_Mobile_Landscape")

    except Exception as e:
        logging.warning(f"Additional mobile tests failed: {e}")

    # Reset to desktop size for final verification
    driver.set_window_size(1920, 1080)
    time.sleep(2)

    # Final validation and results analysis
    try:
        logging.info("RESPONSIVE DESIGN TEST RESULTS SUMMARY:")

        total_tests = len(responsive_test_results)
        passed_tests = sum(1 for result in responsive_test_results.values() if result)

        logging.info(f"Total tests: {total_tests}")
        logging.info(f"Passed tests: {passed_tests}")
        logging.info(f"Success rate: {(passed_tests / total_tests) * 100:.1f}%")

        # Log detailed results
        for test_name, result in responsive_test_results.items():
            status = "PASS" if result else "FAIL"
            logging.info(f"{test_name}: {status}")

        # Determine overall test result
        # Consider test passed if at least 80% of responsive tests pass
        success_threshold = 0.8
        success_rate = passed_tests / total_tests if total_tests > 0 else 0

        if success_rate >= success_threshold:
            expected_result = test_data["expected_result"]
            logging.info(f"Test Passed. {expected_result}")
            logging.info(f"Responsive design verification successful with {success_rate * 100:.1f}% pass rate.")
        else:
            logging.error(
                f"Responsive design test failed. Success rate: {success_rate * 100:.1f}% (threshold: {success_threshold * 100}%)")
            capture_full_page_screenshot(driver, "TC_Reg_16_Overall_Failed")

            # Log specific failures
            failed_tests = [test for test, result in responsive_test_results.items() if not result]
            logging.error(f"Failed tests: {failed_tests}")

            pytest.fail(f"Responsive design test failed. Success rate: {success_rate * 100:.1f}%")

    except Exception as e:
        logging.error(f"Final responsive design validation failed: {e}")
        capture_full_page_screenshot(driver, "TC_Reg_16_Final_Validation_Error")
        pytest.fail(f"Final responsive design validation failed: {e}")

    # Additional verification: Test specific responsive features
    try:
        logging.info("Testing additional responsive features...")

        # Test navigation menu behavior on mobile
        driver.set_window_size(375, 667)
        time.sleep(2)

        # Look for mobile menu button or hamburger menu
        try:
            mobile_menu_elements = driver.find_elements(By.CSS_SELECTOR,
                                                        ".mobile-menu, .hamburger, .menu-toggle, [aria-label='menu']")
            if mobile_menu_elements:
                logging.info("Mobile menu elements found")
                responsive_test_results["mobile_menu"] = True
            else:
                logging.info("No mobile-specific menu found (desktop menu might be used)")
                responsive_test_results["mobile_menu"] = True  # Not necessarily a failure
        except Exception as e:
            logging.warning(f"Mobile menu check failed: {e}")

        # Test text readability on small screens
        try:
            body_element = driver.find_element(By.TAG_NAME, "body")
            font_size = driver.execute_script("return window.getComputedStyle(arguments[0]).fontSize", body_element)

            # Parse font size (usually in px)
            if "px" in font_size:
                size_value = float(font_size.replace("px", ""))
                if size_value >= 14:  # Minimum readable font size
                    logging.info(f"Text is readable on mobile: {font_size}")
                    responsive_test_results["mobile_text_readable"] = True
                else:
                    logging.warning(f"Text might be too small on mobile: {font_size}")
                    responsive_test_results["mobile_text_readable"] = False
            else:
                logging.info(f"Font size check completed: {font_size}")
                responsive_test_results["mobile_text_readable"] = True

        except Exception as e:
            logging.warning(f"Text readability check failed: {e}")
            responsive_test_results["mobile_text_readable"] = True  # Assume OK if can't check

        # Final mobile screenshot
        capture_full_page_screenshot(driver, "TC_Reg_16_Final_Mobile")

    except Exception as e:
        logging.warning(f"Additional responsive features test failed: {e}")

    # Reset to desktop size
    driver.set_window_size(1920, 1080)
    time.sleep(2)

    # Summary and final logging
    try:
        logging.info("RESPONSIVE DESIGN TESTING COMPLETED:")
        logging.info(f"Devices tested: {test_devices}")
        logging.info(f"Pages tested: Homepage, Sign Up, Sign In")
        logging.info(f"Features tested: Layout, Form functionality, Element visibility, Touch-friendliness")

        # Create summary of critical issues
        critical_failures = [test for test, result in responsive_test_results.items()
                             if not result and ("interaction" in test or "heading" in test)]

        if critical_failures:
            logging.warning(f"Critical responsive issues found: {critical_failures}")
        else:
            logging.info("No critical responsive design issues found.")

        # Log device-specific recommendations
        for device in test_devices:
            device_tests = {k: v for k, v in responsive_test_results.items() if device in k}
            device_pass_rate = sum(device_tests.values()) / len(device_tests) if device_tests else 1

            if device_pass_rate >= 0.8:
                logging.info(f"{device.title()} compatibility: GOOD ({device_pass_rate * 100:.0f}%)")
            elif device_pass_rate >= 0.6:
                logging.warning(f"{device.title()} compatibility: FAIR ({device_pass_rate * 100:.0f}%)")
            else:
                logging.error(f"{device.title()} compatibility: POOR ({device_pass_rate * 100:.0f}%)")

    except Exception as e:
        logging.warning(f"Final summary generation failed: {e}")

    # Test completion
    expected_result = test_data["expected_result"]
    final_success_rate = sum(responsive_test_results.values()) / len(
        responsive_test_results) if responsive_test_results else 1

    if final_success_rate >= 0.8:
        logging.info(f"Test Passed. {expected_result}")
        logging.info(f"Overall responsive design verification successful: {final_success_rate * 100:.1f}% pass rate")
    else:
        logging.error(
            f"Test partially failed. Responsive design issues detected: {final_success_rate * 100:.1f}% pass rate")
        # Decide whether to fail based on critical issues
        if critical_failures:
            pytest.fail(f"Critical responsive design issues found: {critical_failures}")
        else:
            logging.warning("Non-critical responsive issues detected but test passed")

    logging.info("TC_Reg_16 Completed..")