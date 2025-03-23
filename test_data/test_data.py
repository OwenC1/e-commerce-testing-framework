# test_data/test_data.py
import json
import os

class DataManager:  # Changed from TestDataManager to DataManager
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), 'test_data.json')
        self.test_data = self._load_test_data()

    def _load_test_data(self):
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def get_user_credentials(self, user_type):
        return self.test_data['users'].get(user_type, {})

    def get_product_details(self, product_key):
        return self.test_data['products'].get(product_key, {})

    def get_cart_scenario(self, scenario_type):
        return self.test_data['test_scenarios']['cart'].get(scenario_type, [])

    def get_sort_options(self):
        return self.test_data['test_scenarios']['sort_options']
    
    # test_data/test_data.py
    def get_data(self, category, key):
        """Get data from any category in the test data file"""
        return self.test_data.get(category, {}).get(key, {})