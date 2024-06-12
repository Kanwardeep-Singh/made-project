import os
import unittest
import subprocess
import sqlite3
from pipeline import download_and_process_emissions_dataset, download_and_process_temperature_dataset

class TestPipeline(unittest.TestCase):

    def setUp(self):
        
        # Adjust the base_dir to match your structure
        self.base_dir = os.path.dirname(os.path.abspath(__file__))  # This will be project directory
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.emission_db_path = os.path.join(self.data_dir, 'emission_data.sqlite')
        self.temperature_db_path = os.path.join(self.data_dir, 'temperature_data.sqlite')
        self.pipeline_script = os.path.join(self.base_dir, 'pipeline.py')

        # Ensure the data directory exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def test_pipeline_execution(self):

        # Define test URLs and paths
        emission_url = 'https://www.kaggle.com/api/v1/datasets/download/thedevastator/global-fossil-co2-emissions-by-country-2002-2022?datasetVersionNumber=4'
        temperature_url = 'https://www.kaggle.com/api/v1/datasets/download/mdazizulkabirlovlu/all-countries-temperature-statistics-1970-2021?datasetVersionNumber=1'
        
        # Define project directory
        project_dir = self.base_dir

        # Call the functions from pipeline.py
        download_and_process_emissions_dataset(emission_url, os.path.join(project_dir, 'emission_data'), os.path.join(self.data_dir, 'emission_data.sqlite'))
        download_and_process_temperature_dataset(temperature_url, os.path.join(project_dir, 'temperature_data'), os.path.join(self.data_dir, 'temperature_data.sqlite'))
        
        # Execute the pipeline
        result = subprocess.run(['python', self.pipeline_script], capture_output=True, text=True)

        # Print output for debugging
        print("Pipeline output:\n", result.stdout)
        print("Pipeline errors:\n", result.stderr)

        # Verify the paths
        print("Emission DB Path:", self.emission_db_path)
        print("Temperature DB Path:", self.temperature_db_path)

        # Check that the output files were created
        emission_exists = os.path.exists(self.emission_db_path)
        temperature_exists = os.path.exists(self.temperature_db_path)

        print("Emission DB Exists:", emission_exists)
        print("Temperature DB Exists:", temperature_exists)

        self.assertTrue(emission_exists, f"Expected output file {self.emission_db_path} does not exist.")
        self.assertTrue(temperature_exists, f"Expected output file {self.temperature_db_path} does not exist.")

        # Verify that the SQLite files contain the expected tables
        if emission_exists:
            with sqlite3.connect(self.emission_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emission_data';")
                self.assertIsNotNone(cursor.fetchone(), "Table 'emission_data' does not exist in the emissions database.")
        
        if temperature_exists:
            with sqlite3.connect(self.temperature_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='temperature_data';")
                self.assertIsNotNone(cursor.fetchone(), "Table 'temperature_data' does not exist in the temperature database.")

if __name__ == "__main__":
    unittest.main()
