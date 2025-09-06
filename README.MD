run: 
pytest --browser=firefox --alluredir=allure_test_report 
allure serve allure_test_report 

allure generate .\allure_test_report\ --clean -o .\allure_html_report\ 


# Doer School Admission Test Automation

## Project Structure

```
E:\projects\Tasks\Doer_School_Admission\
├── conftest.py                    # Root level configuration
├── tests/                         # All test files
│   ├── __init__.py
│   ├── admission/                 # Admission specific test cases
│   │   ├── __init__.py
│   │   ├── test_TC_AD_01.py      # Verify All Available Admissions Display
│   │   ├── test_TC_AD_02.py      # Verify Search by School Name
│   │   ├── test_TC_AD_03.py      # Verify Filter by Campus
│   │   ├── test_TC_AD_04.py      # Verify Filter by Class
│   │   ├── test_TC_AD_05.py      # Verify Filter by Medium
│   │   ├── test_TC_AD_06.py      # Verify Clear All Filters
│   │   ├── test_TC_AD_07.py      # Verify Apply Now Button
│   │   ├── test_TC_AD_08.py      # Verify Download Circular
│   │   ├── test_TC_AD_09.py      # Verify Student Info Form (Valid Data)
│   │   ├── test_TC_AD_10.py      # Verify Student Info Form (Invalid Data)
│   │   ├── test_TC_AD_11.py      # Verify Additional Student Info
│   │   ├── test_TC_AD_12.py      # Verify Guardian Information
│   │   ├── test_TC_AD_13.py      # Verify Previous School Info
│   │   ├── test_TC_AD_14.py      # Verify Document Upload
│   │   ├── test_TC_AD_15.py      # Verify Application Submission
│   │   ├── test_TC_AD_16.py      # Verify Payment Prompt
│   │   └── test_TC_AD_18.py      # Verify View Voucher
│   └── registration/              # Existing registration tests
│       ├── __init__.py
│       ├── test_customer_registration.py
│       └── test_manager_registration.py
├── pages/                         # Page Object Models
│   ├── __init__.py
│   ├── customer_registration_page.py      # Existing
│   ├── manager_registration_page.py       # Existing
│   ├── admission_portal_page.py           # New - Main admission page
│   ├── student_information_page.py        # New - Student form
│   ├── guardian_information_page.py       # New - Guardian form
│   ├── previous_school_page.py            # New - Previous school form
│   ├── document_upload_page.py            # New - Document upload
│   ├── application_review_page.py         # New - Review & submit
│   └── payment_page.py                    # New - Payment & voucher
├── utils/
│   ├── __init__.py
│   ├── bug_report_template.py             # Existing
│   ├── data_loader.py                     # Existing - for registration
│   ├── admission_data_loader.py           # New - for admission tests
│   └── screenshot_utils.py                # Existing
├── logs/
├── Screenshots/
├── bug_reports/
├── test_files/                            # Test documents for upload
└── data/
    ├── data.json                          # Existing registration data
    └── data_admission.json                # New admission test data
```

## Setup Instructions

### 1. Create Folder Structure
Create the following folders if they don't exist:
- `tests/admission/`
- `test_files/` (for document upload test files)

### 2. Create __init__.py Files
Add empty `__init__.py` files to make directories Python packages:
- `tests/__init__.py`
- `tests/admission/__init__.py`
- `tests/registration/__init__.py` (if not exists)
- `pages/__init__.py` (if not exists)
- `utils/__init__.py` (if not exists)

### 3. Add Test Data File
Place the `data_admission.json` file in the `data/` directory.

### 4. Add Page Object Model Files
Add all the new page object files to the `pages/` directory:
- `admission_portal_page.py`
- `student_information_page.py`
- `guardian_information_page.py`
- `previous_school_page.py`
- `document_upload_page.py`
- `application_review_page.py`
- `payment_page.py`

### 5. Add Test Files
Add all test case files to the `tests/admission/` directory.

### 6. Create Test Files for Document Upload
For TC_AD_14, create sample test files in `test_files/` directory:
- `student_photo.jpg` (sample image file)
- `birth_certificate.pdf` (sample PDF file)
- `academic_records.pdf` (sample PDF file)

## Running Tests

### Run All Admission Tests
```bash
pytest tests/admission/ -v --browser=chrome
```

### Run Specific Test Case
```bash
pytest tests/admission/test_TC_AD_01.py -v --browser=chrome
```

### Run Tests with Different Browsers
```bash
pytest tests/admission/ -v --browser=firefox
pytest tests/admission/ -v --browser=edge
```

### Run Tests with Logging
```bash
pytest tests/admission/ -v --browser=chrome --log-cli-level=INFO
```

## Test Cases Coverage

### Admission Portal Tests (TC_AD_01 to TC_AD_08)
- ✅ Display verification
- ✅ Search functionality
- ✅ Filter functionality
- ✅ Navigation to application form
- ✅ Download functionality

### Student Information Tests (TC_AD_09 to TC_AD_11)
- ✅ Valid data entry
- ✅ Invalid data validation
- ✅ Additional information form

### Guardian Information Test (TC_AD_12)
- ✅ Complete guardian information form

### Previous School Test (TC_AD_13)
- ✅ Previous academic details

### Document Upload Test (TC_AD_14)
- ✅ File upload functionality

### Application Submission Tests (TC_AD_15, TC_AD_16)
- ✅ Final submission and confirmation
- ✅ Payment prompt verification

### Payment Test (TC_AD_18)
- ✅ Voucher generation and display

## Important Notes

1. **CSS Selectors**: The page object models use generic CSS selectors. You'll need to update these with the actual selectors from the Doer School admission portal.

2. **Test Data**: The test data in `data_admission.json` follows the same pattern as your existing registration tests. You can modify the data as needed.

3. **File Uploads**: For document upload tests, ensure you have valid test files in the `test_files/` directory.

4. **Navigation Flow**: Some tests assume previous forms are completed. In a real scenario, you might need to complete the entire flow or have specific test data setup.

5. **Error Handling**: All tests include comprehensive error handling and screenshot capture on failures.

6. **Logging**: Each test logs its progress and results to the log file specified in `conftest.py`.

## Extending the Framework

To add more test cases:
1. Add test data to `data_admission.json`
2. Create corresponding test file in `tests/admission/`
3. Add any new page object methods as needed
4. Follow the same pattern as existing test cases

## Maintenance

- Update CSS selectors when the application UI changes
- Add new test cases as requirements evolve
- Keep test data updated with valid information
- Review and update page object models regularly