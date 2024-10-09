import os
import csv
from tqdm import tqdm

def process_text_file(file_path):
    """Reads a text file and separates the link and text content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # The first line contains the link (split by tab "\t")
            if len(lines) > 0:
                first_line = lines[0].split('\t')
                if len(first_line) >= 2:
                    link = first_line[1].strip()  # Extract link after tab
                else:
                    link = "No link"
                
                # Combine remaining lines as the text content
                text = ''.join(lines[1:]).strip()  # Join all lines after the first one
                return link, text
            else:
                return None, None
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None

def compile_to_csv(directory, output_csv):
    """Compile all .txt files in a directory into a CSV file with columns 'link' and 'text'."""
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['link', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Get list of all .txt files in the directory
        text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

        # Use tqdm to show progress
        for filename in tqdm(text_files, desc="Processing files", unit="file"):
            file_path = os.path.join(directory, filename)
            link, text = process_text_file(file_path)
            
            if link and text:
                writer.writerow({'link': link, 'text': text})
            else:
                print(f"Skipped {file_path} due to missing link or text")

if __name__ == '__main__':
    txt_directory = '../TeluguData/Tupaki'
    output_csv = 'Tupaki.csv'
    compile_to_csv(txt_directory, output_csv)
    print(f"CSV compilation complete. Output saved to {output_csv}")
