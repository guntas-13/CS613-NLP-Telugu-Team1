import os
import csv
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def process_file(file_path):
    """Returns the file_path"""
    return file_path

def calculate_simhashes_and_save(folder_paths, output_csv):
    """Compiles the file_paths of the files given folder paths and save to a CSV file."""
    file_paths = []
    for folder in folder_paths:
        for root, _, files in os.walk(folder):
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_paths.append(os.path.join(root, file_name))

    total_files = len(file_paths)

    with ThreadPoolExecutor() as executor:
        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['filepath'])
                
            for file_path in tqdm(executor.map(process_file, file_paths), total=len(file_paths)):
                writer.writerow([file_path])

    print(f"Total number of articles: {total_files}")

if __name__ == '__main__':
    folder_paths = ['../TeluguData/TeluguPost', '../TeluguData/Tupaki', '../TeluguData/TeluguStop']
    output_csv = '../TeluguData/filepaths.csv'
    calculate_simhashes_and_save(folder_paths, output_csv)
