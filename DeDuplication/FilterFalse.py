import os
import pandas as pd
from tqdm import tqdm

def filter_similarities_in_directory(directory, threshold=0.8):
    """Filter CSV files in the specified directory to keep only rows with similarity above the threshold."""
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    total_duplicates_remaining = 0

    for filename in tqdm(csv_files, desc="Processing CSV files"):
        file_path = os.path.join(directory, filename)

        df = pd.read_csv(file_path)

        filtered_df = df[df['similarity'] > threshold]

        total_duplicates_remaining += len(filtered_df)

        filtered_df.to_csv(file_path, index=False)

        print(f"Overwritten {file_path} with filtered results.")

    print(f"\nTotal duplicates remaining across all files: {total_duplicates_remaining}")

if __name__ == "__main__":
    directory = '../TeluguData/Similarity'
    threshold = 0.8
    filter_similarities_in_directory(directory, threshold)
