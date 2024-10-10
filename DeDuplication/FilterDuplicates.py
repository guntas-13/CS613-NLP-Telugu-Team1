import os
import pandas as pd
from tqdm import tqdm

output_dir = "../TeluguData/Similarity"
removed_files_path = "../TeluguData/Logs/removed_files.txt"

def process_row(row, remaining_files, removed_files):
    """Process each row to determine which file should be removed."""
    file1 = row['file1']
    file2 = row['file2']
    similarity = row['similarity']

    # Determine which file to keep based on similarity
    if similarity > 0.8:
        # Keep file1 if similarity is greater, otherwise mark file2 for removal
        if file1 not in removed_files:
            remaining_files.add(file1)
        if file2 not in remaining_files:
            removed_files.add(file2)
    else:
        if file2 not in removed_files:
            remaining_files.add(file2)
        if file1 not in remaining_files:
            removed_files.add(file1)

def process_csv(csv_file_path, remaining_files, removed_files):
    """Process the CSV file to determine remaining and removed files."""
    df = pd.read_csv(csv_file_path)
    print(f"Reading {csv_file_path}...")
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Processing {os.path.basename(csv_file_path)}"):
        process_row(row, remaining_files, removed_files)


if __name__ == "__main__":
    csv_files = [os.path.join(output_dir, file_name) for file_name in os.listdir(output_dir) if file_name.endswith('.csv')]
    print(f"Total number of CSV files: {len(csv_files)}")
    
    remaining_files = set()
    removed_files = set()

    for csv_file in tqdm(csv_files, desc="Processing CSVs"):
        process_csv(csv_file, remaining_files, removed_files)
        
    final_remaining_files = remaining_files - removed_files

    print(f"Total number of remaining files: {len(final_remaining_files)}")
    print(f"Total number of removed files: {len(removed_files)}")
    print(f"Total files: {len(final_remaining_files) + len(removed_files)}")
    
    with open(removed_files_path, 'w') as f:
        for file in removed_files:
            f.write(f"{file}\n")

    print(f"Removed files saved to {removed_files_path}")
