import json
import os

def load_admission_test_data(file_path):
    """
    Load admission test data from JSON file
    """
    data_file = os.path.join(os.path.dirname(__file__), file_path)
    with open(data_file) as df:
        return json.load(df)

def get_test_data_by_section(file_path, section_name):
    """
    Get test data for a specific section (e.g., 'admission_portal', 'student_information')
    """
    all_data = load_admission_test_data(file_path)
    if all_data and len(all_data) > 0:
        return all_data[0].get(section_name, [])
    return []

def get_specific_test_case(file_path, section_name, test_case_id):
    """
    Get a specific test case by section and test case ID
    """
    section_data = get_test_data_by_section(file_path, section_name)
    for test_case in section_data:
        if test_case_id in test_case:
            return test_case[test_case_id]
    return None