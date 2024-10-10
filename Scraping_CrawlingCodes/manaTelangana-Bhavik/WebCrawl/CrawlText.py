import os
import csv
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to crawl data from a single link with retries
def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=3):
    retries = 0
    while retries < max_retries:
        try:
            response = urllib.request.urlopen(link)
            if response.status == 200:
                return response.read()
            else:
                print(f"Failed to fetch data from {link}. Retrying... ({retries + 1}/{max_retries})")
                retries += 1
                time.sleep(retry_interval)
        except Exception as e:
            print(f"An error occurred while fetching data from {link}: {e}. Retrying... ({retries + 1}/{max_retries})")
            retries += 1
            time.sleep(retry_interval)
    print(f"Failed to fetch data from {link} after {max_retries} retries.")
    return None

# Function to check if the text contains Telugu characters
def is_telugu(text):
    telugu_range = r'[\u0C00-\u0C7F]+'
    return re.search(telugu_range, text)

# Function to extract Telugu data from HTML content
def extract_data_from_html(html_content, link):
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.find('h1', class_='tdb-title-text')
        divs = soup.find_all('div', class_='tdb-block-inner td-fix-index')
        text = ""
        if title:
            text += title.text.strip() + "\n" + link + "\n"
        extracted_data.append(text)
        for div in divs:
            paragraphs = div.find_all('p')
            for paragraph in paragraphs:
                if is_telugu(paragraph.text):
                    extracted_data.append(paragraph.text.strip())
    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")
    return extracted_data

# Function to process a single link and write to the text file immediately
def process_link_and_write(link, link_num, fail, base_directory):
    html_content = crawl_data_from_link_with_retry(link)
    if html_content:
        extracted_data = extract_data_from_html(html_content, link)
        if extracted_data:
            try:
                with open(f"{base_directory}/{link_num}.txt", 'w', encoding='utf-8') as text_file:
                    text_file.write('\n'.join(extracted_data) + '\n')
                if link_num % 10 == 0:
                    print(f"{link_num} links processed\n{fail} links failed")
                return link_num, fail
            except Exception as e:
                print(f"An error occurred while writing to file: {e}")
                fail += 1
        else:
            fail += 1
    else:
        fail += 1
    return link_num, fail

# Function to process all CSV files in a directory
def process_csv_folder(csv_folder_path, corpus_directory):
    print(f"Processing CSV folder: {csv_folder_path}")
    start=int(input("Enter the starting link number: "))
    end=int(input("Enter the ending link number(inclusive): "))
    corpus_directory+=f"_{start}_{end}"
    if not os.path.exists(corpus_directory):
        os.makedirs(corpus_directory)
        print(f"Created directory: {corpus_directory}")

    if not os.path.exists(csv_folder_path):
        print(f"CSV folder path does not exist: {csv_folder_path}")
        return

    csv_files = ['links.csv']  # Update with the CSV file names
    print(f"Found CSV files: {csv_files}")

    link_num = 1
    fail = 0

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for csv_file_name in csv_files:
            csv_file_path = os.path.join(csv_folder_path, csv_file_name)
            df = pd.read_csv(csv_file_path)
            print(f"Processing file: {csv_file_path}")
            links = df['link']
            
            for i,link in enumerate(links):
                if i+1<start:
                    continue
                if i+1>end:
                    break
                link_num=i+1
                futures.append(executor.submit(process_link_and_write, link, link_num, fail,corpus_directory))
                # link_num += 1

        # Collect results
        for future in as_completed(futures):
            try:
                link_num, fail = future.result()
            except Exception as e:
                print(f"An error occurred in thread execution: {e}")

# Folder containing the CSV files
csv_folder_path = '../LinkScrape'  # Update with your CSV folder path
# Directory to save the text files
corpus_directory = '../textData'  # Update with your text data folder path

print(os.getcwd())
print("Starting the processing of CSV files...")
process_csv_folder(csv_folder_path, corpus_directory)
print("Processing complete.")
