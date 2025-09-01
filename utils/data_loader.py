import json
import os


def load_all_test_data(file_path):
    data_file = os.path.join(os.path.dirname(__file__),file_path)
    with open(data_file) as df:
        return json.load(df)