import csv
import re
import os
import pickle

csv.field_size_limit(10000000000)

def extract_english_segments(text):
    # Regular expression to find segments of English text, numbers, and symbols including spaces
    segments = re.findall(r'[a-zA-Z0-9»!@#$%^&*()_+={}\[\]:;"\'|\\<,>.?/~\s\n%+^-]+', text)
    
    remove_list = []
    remove_this = ""
    detect = False
    
    for i in segments:
        if i != " ":
            remove_this += i
            detect = True
        else:
            if detect:
                remove_list.append(remove_this)
                remove_this = ""
            detect = False
            
    # Adding the last segment if it exists
    if remove_this:
        remove_list.append(remove_this)

    return remove_list

def process_csv(input_file, output_log):
    results = {}

    with open(input_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        with open(output_log, mode='w', encoding='utf-8') as log_file:
            for row in csv_reader:
                content = row['text']  # Changed to 'text' for the single column
                english_segments = extract_english_segments(content)
                
                # Write to log file
                if english_segments:
                    log_file.write(f"Original Text: {content}\n")
                    segment_list = []

                    for segment in english_segments:
                        if len(segment.replace(" ", "")) > 6:
                            is_alp = re.findall(r'[a-zA-Z]+', segment)
                            if len(is_alp) > 0:
                                log_file.write(f"English Text: {segment}\n")
                                segment_list.append(segment)

                    log_file.write("\n")
                    if segment_list:
                        results[content] = segment_list  # Storing based on original content

    return results

def remove_strings_from_row(content, strings_to_remove):
    if len(strings_to_remove) > 0 and (("https" in strings_to_remove) or ("www" in strings_to_remove) or ("http" in strings_to_remove) or ("http://" in strings_to_remove)):
        if strings_to_remove[-1] == " " or strings_to_remove[-1] == "\n" or strings_to_remove[-1] == "»":
            content = content.replace(strings_to_remove[:-1], ' <|hyperlink|> ')
        else:
            content = content.replace(strings_to_remove, ' <|hyperlink|> ')
    return content

def modify_csv(input_file, pickle_file, output_file):
    """
    Modify the input CSV by removing unwanted strings based on the extracted data.
    """
    # Load the extracted removal strings from the pickle file
    with open(pickle_file, 'rb') as f:
        removal_dict = pickle.load(f)

    # Open the input CSV and output CSV files
    with open(input_file, mode='r', encoding='utf-8') as csv_file, open(output_file, mode='w', encoding='utf-8') as out_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        modified_count = 0  # Counter for modified rows
        total_rows = 0  # Counter for total rows

        # Process each row in the input CSV
        for row in csv_reader:
            content = row['text']  # Accessing the text column
            total_rows += 1  # Increment total rows count
            for i in removal_dict.get(content, []):  # Get removal strings based on content
                for j in range(15):
                    rem_content = remove_strings_from_row(content, i[:len(i) - j])
                    rem_content2 = remove_strings_from_row(content, i[j:len(i)])
                
                if len(content) != len(rem_content):
                    content = rem_content
                    modified_count += 1  # Increment modified count
                    break
                elif len(content) != len(rem_content2):
                    content = rem_content2
                    modified_count += 1  # Increment modified count
                    break
            
            row['text'] = content  # Update the content in the row
            csv_writer.writerow(row)  # Write the modified row

    print(f"Modified {modified_count} rows.")
    print(f"Total remaining rows in the cleaned CSV: {total_rows}")

if __name__ == "__main__":
    name = "Tupaki_clean_articles"
    input_file = '../TeluguData/Tupaki_clean_articles.csv'  # Path to the input CSV file
    output_log = f'../TeluguData/{name}.txt'  # Path for the log file
    results = process_csv(input_file, output_log)
    
    # Save the results dictionary to a pickle file
    pickle_folder = "../TeluguData"
    pickle_file = os.path.join(pickle_folder, f'{name}.pkl')

    with open(pickle_file, 'wb') as f:
        pickle.dump(results, f)
    
    print(f"Results dictionary saved to {pickle_file}")

    # Modify the CSV using the results from the previous step
    output_file = f'../TeluguData/cleaned_{name}.csv'  # Path for the output CSV file
    modify_csv(input_file, pickle_file, output_file)
    
    print(f"Modified CSV saved to {output_file}")
