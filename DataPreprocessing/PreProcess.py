import os
import json
import re
import pandas as pd
from tqdm import tqdm

with open('badwords.json', 'r', encoding='utf-8') as f:
    bad_words = json.load(f)['te']


bad_words = "|".join(bad_words)
email_pattern = r"\S+@\S+"
phone_pattern = r'[\+\(]?[0-9][0-9 .\-\(\)]{5,}[0-9]'
correct_phone_pattern = r"\s?\d{4}-\d{4}\s?$"


input_csv_path = '../TeluguData/Tupaki.csv'
clean_output_path = '../TeluguData/Tupaki_clean_articles.csv'
bad_output_path = '../TeluguData/Tupaki_bad_articles.csv'


def contains_only_english(text):
    return all(re.match(r'^[a-zA-Z0-9\s.,!?\'"-]*$', line) for line in text.splitlines())


def check_for_bad_content(text):
    matches = []
    
    # Check for bad words
    bad_word_match = re.search(bad_words, text, re.IGNORECASE)
    if bad_word_match:
        matches.append(bad_word_match.group(0))
    
    # Check for email addresses
    email_match = re.search(email_pattern, text)
    if email_match:
        matches.append(email_match.group(0))
    
    # Check for phone numbers
    phone_match = re.search(phone_pattern, text)
    if phone_match and not re.search(correct_phone_pattern, text):
        matches.append(phone_match.group(0))
    
    return matches if matches else None


def preprocess_data(input_csv, clean_output, bad_output):
    df = pd.read_csv(input_csv)
    
    clean_rows = []
    bad_rows = []
    
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        text = row['text']
        
        filtered_lines = [line for line in text.splitlines() if not contains_only_english(line)]
        
        filtered_text = "\n".join(filtered_lines)

        if not filtered_text.strip():
            continue

        matches = check_for_bad_content(filtered_text)
        if matches:
            row['matches'] = ', '.join(matches)
            bad_rows.append(row)
        else:
            clean_rows.append(row)
    
    clean_df = pd.DataFrame(clean_rows)
    bad_df = pd.DataFrame(bad_rows)

    os.makedirs(os.path.dirname(clean_output), exist_ok=True)
    os.makedirs(os.path.dirname(bad_output), exist_ok=True)

    clean_df.to_csv(clean_output, index=False)
    bad_df.to_csv(bad_output, index=False)

    print(f"Number of rows in clean articles: {len(clean_df)}")
    print(f"Number of rows in bad articles: {len(bad_df)}")


preprocess_data(input_csv_path, clean_output_path, bad_output_path)