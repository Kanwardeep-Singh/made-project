import os
import pandas as pd
import requests
import zipfile
import sqlite3
import io

def ensure_directory(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Created directory: {path}")
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
            exit(1)

def download_and_process_emissions_dataset(url, output_folder, db_path):
    try:
        ensure_directory(output_folder)
        print(f"Downloading emissions dataset from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(output_folder)
        csv_filename = os.path.join(output_folder, zip_file.namelist()[1])
        print(f"Processing file: {csv_filename}")
        df = pd.read_csv(csv_filename, on_bad_lines='skip')
        df = df.loc[~(df==0).all(axis=1)]
        df.dropna(inplace=True)
        ensure_directory(os.path.dirname(db_path))
        conn = sqlite3.connect(db_path)
        df.to_sql('emission_data', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Saved emissions data to database: {db_path}")
    except Exception as e:
        print(f"Error processing emissions dataset: {e}")

def download_and_process_temperature_dataset(url, output_folder, db_path):
    try:
        ensure_directory(output_folder)
        print(f"Downloading temperature dataset from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(output_folder)
        csv_filename = os.path.join(output_folder, zip_file.namelist()[0])
        print(f"Processing file: {csv_filename}")
        df = pd.read_csv(csv_filename, on_bad_lines='skip')
        df.drop(columns=['Unit'], inplace=True)
        df = df.loc[~(df==0).all(axis=1)]
        df.dropna(inplace=True)
        ensure_directory(os.path.dirname(db_path))
        conn = sqlite3.connect(db_path)
        df.to_sql('temperature_data', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Saved temperature data to database: {db_path}")
    except Exception as e:
        print(f"Error processing temperature dataset: {e}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    project_dir = base_dir

    emission_url = 'https://www.kaggle.com/api/v1/datasets/download/thedevastator/global-fossil-co2-emissions-by-country-2002-2022?datasetVersionNumber=4'
    temperature_url = 'https://www.kaggle.com/api/v1/datasets/download/mdazizulkabirlovlu/all-countries-temperature-statistics-1970-2021?datasetVersionNumber=1'

    print(f"Data directory: {data_dir}")
    print(f"Project directory: {project_dir}")

    download_and_process_emissions_dataset(emission_url, os.path.join(project_dir, 'emission_data'), os.path.join(data_dir, 'emission_data.sqlite'))
    download_and_process_temperature_dataset(temperature_url, os.path.join(project_dir, 'temperature_data'), os.path.join(data_dir, 'temperature_data.sqlite'))

if __name__ == "__main__":
    main()
