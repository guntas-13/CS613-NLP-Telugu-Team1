import os
import csv
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to crawl data from a single link with retries
def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=5):
    print(f"Attempting to fetch data from {link}")
    retries = 0
    while retries < max_retries:
        try:
            response = urllib.request.urlopen(link)
            if response.status == 200:
                # print(f"Successfully fetched data from {link}")
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
def extract_data_from_html(html_content):
    # print("Extracting data from HTML content")
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        # Find the div with the class 'left-cont leftSidebar'
        div = soup.find('div', class_='left-cont leftSidebar')
        str=""
        if div:
            # Find all paragraphs inside the div
            paragraphs = div.find_all('p')
            for paragraph in paragraphs:
                # Check if the paragraph contains any Telugu text
                if is_telugu(paragraph.text):
                    extracted_data.append(paragraph.text.strip())
    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")

    return extracted_data

# Function to process a single link and write to the text file immediately
def process_link_and_write(link, link_num):
    # print(f"Processing link: {link}")
    html_content = crawl_data_from_link_with_retry(link)
    if html_content:
        extracted_data = extract_data_from_html(html_content)
        text_file_path = f"./textData/{link_num}.txt"
        if extracted_data:
            try:
                # Filter out duplicate entries
                # extracted_data = list(set(extracted_data))
                with open(text_file_path, 'a', encoding='utf-8') as text_file:
                    text_file.write('\n'.join(extracted_data) + '\n')
                print(f"Successfully wrote data to {text_file_path}")
                return True
            except Exception as e:
                print(f"An error occurred while writing to file {text_file_path}: {e}")
    return False

# Function to process all CSV files in a directory
def process_csv_folder(csv_folder_path, corpus_directory, failed_csv_path):
    print(f"Processing CSV folder: {csv_folder_path}")
    if not os.path.exists(corpus_directory):
        os.makedirs(corpus_directory)
        print(f"Created directory: {corpus_directory}")

    # Ensure the CSV folder path is correct
    if not os.path.exists(csv_folder_path):
        print(f"CSV folder path does not exist: {csv_folder_path}")
        return

    # csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
    csv_files=["links.csv"]
    print(f"Found CSV files: {csv_files}")    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures=[]
        for csv_file_name in csv_files:
            csv_file_path = os.path.join(csv_folder_path, csv_file_name)
            # text_file_path = os.path.join(corpus_directory, f"{os.path.splitext(csv_file_name)[0]}.txt")
            print(f"Processing file: {csv_file_path}")
            df=pd.read_csv(csv_file_path)
            links=df['link']
        for i,link in enumerate(links):
            link_num=i+1
            future_to_link = {executor.submit(process_link_and_write, link, link_num)}
        

# Folder containing the CSV files
csv_folder_path = './LinkScrape'  # Update with your CSV folder path
# Directory to save the text files
corpus_directory = './textData'  # Update with your text data folder path

# Provide the path for the failed.csv file
failed_csv_path = './failed_urls.csv'

# Call the function with the provided path
print("Starting the processing of CSV files...")
process_csv_folder(csv_folder_path, corpus_directory, failed_csv_path)
print("Processing complete.")