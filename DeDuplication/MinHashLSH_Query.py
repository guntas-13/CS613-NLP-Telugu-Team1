import os
import csv
import re
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from datasketch import MinHash, MinHashLSH
import pandas as pd

def create_directory_if_not_exists(directory):
    """Create the specified directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_features(s):
    """Extract 3-character shingles from the string."""
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

def get_minhash(content, num_perm=128):
    """Convert features derived from content to a MinHash object for LSH comparison."""
    minhash = MinHash(num_perm=num_perm)
    features = get_features(content)
    for feature in features:
        minhash.update(feature.encode('utf-8'))
    return minhash

def load_filepaths_from_csv(csv_file):
    """Load the filepaths from a CSV file."""
    filepaths = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            filepath = row[0]  # Get the filepath
            filepaths.append(filepath)
    return filepaths

def process_file(filepath):
    """Process a single file to get its content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()  # Read content for MinHash calculation
    return filepath, get_minhash(content)

def save_chunk(data, output_file_path, index, iteration_index):
    """Save a chunk of data to a CSV file."""
    df = pd.DataFrame(data)  # Create a DataFrame from the data
    chunk_output_path = os.path.join(output_file_path, f"chunk_{index + 1}_{iteration_index}.csv")  # Updated naming convention
    df.to_csv(chunk_output_path, index=False)  # Save DataFrame to CSV
    print(f"Saved chunk {index + 1} to {chunk_output_path}")  # Notify which chunk was saved

def deduplicate_files(filepaths, threshold=0.8, output_file_path='similarity_results.csv'):
    """Deduplicate files by comparing their contents using MinHashLSH."""
    lsh = MinHashLSH(threshold=threshold, num_perm=128)
    duplicates = set()  # Track unique duplicate pairs
    duplicate_files = set()  # Track unique files that are marked as duplicates
    data = []
    index = 0
    iteration_index = 0
    no_of_files = 1000000  # Number of results to save at once
    total_duplicates = 0  # Counter for total duplicates found

    # Use multiprocessing to generate MinHashes for all files
    with Pool(cpu_count()) as pool:
        file_minhash_map = dict(tqdm(pool.imap(process_file, filepaths), total=len(filepaths), desc="Generating MinHash objects"))

    # Stage 1: Insert all MinHashes into LSH
    for file, minhash in tqdm(file_minhash_map.items(), desc="Inserting MinHashes into LSH"):
        lsh.insert(file, minhash)  # Insert MinHash into LSH for future queries

    # Stage 2: Query MinHashLSH and identify duplicates
    for file, minhash in tqdm(file_minhash_map.items(), desc="Finding duplicates"):
        result = lsh.query(minhash)
        for other_file in result:
            if file != other_file:  # Ensure we don't compare a file with itself
                similarity = minhash.jaccard(file_minhash_map[other_file])
                data.append({
                    'file1': file,
                    'hash1': str(minhash),
                    'file2': other_file,
                    'hash2': str(file_minhash_map[other_file]),
                    'similarity': similarity
                })
                duplicates.add((file, other_file))  # Add to the duplicates set
                iteration_index += 1
                duplicate_files.add(file)
                duplicate_files.add(other_file)
                if len(data) >= no_of_files:
                    save_chunk(data, output_file_path, index, iteration_index)
                    data.clear()  # Clear the data list to free memory

    # Save any remaining data to a CSV chunk
    if data:
        save_chunk(data, output_file_path, index, iteration_index)

    print(f"Total duplicates pairs found: {len(duplicates)}")
    print(f"Total unique files with duplicates: {len(duplicate_files)}")  # Files identified as duplicates
    print(f"Total unique files: {len(filepaths) - len(duplicate_files)}")  # Files that are not duplicates

def main(input_csv, output_file_path='similarity_results.csv', threshold=0.8):
    
    filepaths = load_filepaths_from_csv(input_csv)
    deduplicate_files(filepaths, threshold, output_file_path)
    print("Deduplication complete.")

if __name__ == "__main__":
    input_csv = '../TeluguData/filepaths.csv'
    output_file_path = '../TeluguData/Similarity'
    main(input_csv, output_file_path, threshold= 0.8)
