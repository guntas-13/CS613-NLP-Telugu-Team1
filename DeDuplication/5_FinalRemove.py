import os
from tqdm import tqdm

removed_files_path = "../TeluguData/Logs/removed_files.txt"

def remove_files(removed_files):
    """Remove the files listed for deletion."""
    for file in tqdm(removed_files, desc="Removing files"):
        try:
            if os.path.exists(file):
                os.remove(file)
            else:
                print(f"File not found: {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

def main():
    # Check if the removed_files.txt exists
    if not os.path.exists(removed_files_path):
        print(f"File {removed_files_path} not found!")
        return
    
    # Read the file containing the list of files to be removed
    with open(removed_files_path, 'r') as f:
        removed_files = [line.strip() for line in f.readlines()]
    
    print(f"Total files to remove: {len(removed_files)}")

    # Remove the files listed in removed_files.txt
    remove_files(removed_files)

if __name__ == "__main__":
    main()
