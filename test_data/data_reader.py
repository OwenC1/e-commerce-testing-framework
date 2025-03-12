# test_data/data_reader.py
import json
import os

class DataReader:
    @staticmethod
    def load_data(file_path):
        """
        Loads test data from a JSON file.
        
        Args:
            file_path: Path to the JSON data file
            
        Returns:
            The loaded data as a Python object
        """
        # Construct absolute path relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        absolute_path = os.path.join(base_dir, file_path)
        
        # Read and parse the JSON file
        with open(absolute_path, 'r') as file:
            return json.load(file)