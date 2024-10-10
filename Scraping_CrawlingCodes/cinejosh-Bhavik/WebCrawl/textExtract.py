import os
import csv
import urllib.request
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
# from concurrent.futures import ThreadPoolExecutor, as_completed
import time
link_num=1
# Function to crawl data from a single link with retries
def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=3):
    # print(f"Attempting to fetch data from {link}")
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
def extract_data_from_html(html_content,link):
    # print("Extracting data from HTML content")
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        heading = soup.find_all('h1', class_='h1TelStyle')
        str=""
        if heading:
            str=heading[0].text.strip()
            str+="\n"+ link + "\n"
        extracted_data.append(str)
        # Find the div with the class 'left-cont leftSidebar'
        div = soup.find('div', class_='mobilePadding')
        if div:
            # Find all paragraphs inside the div
            paragraphs = div.find_all('p')
            for paragraph in paragraphs:
                # Check if the paragraph contains any Telugu text
                if is_telugu(paragraph.text):
                    extracted_data.append(paragraph.text.strip())
    except Exception as e:
        time.sleep(2)
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            heading = soup.find_all('h1', class_='h1TelStyle')
            str=""
            if heading:
                str=heading[0].text.strip()
                str+="\n"+ link + "\n"
            extracted_data.append(str)
            # Find the div with the class 'left-cont leftSidebar'
            div = soup.find('div', class_='mobilePadding')
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
# def process_link_and_write(link):
    


def process_csv_folder(csv_folder_path):
    csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
    print(f"Found CSV files: {csv_files}")
    link_num=1
    fail=0
    for csv_file_name in csv_files:
        df= pd.read_csv(csv_file_name)
        links = df['link']
        print(f"Found links in {csv_file_name}: {links}")
        for link in links:
            if link_num%100==0:
                print(f"{link_num} Links Processed")
                print(f"{fail} Links Failed")
            # print(f"Processing file: {csv_file_name}")
            # print(f"Processing link: {link}")
            html_content = crawl_data_from_link_with_retry(link)
            if html_content:
                extracted_data = extract_data_from_html(html_content,link)
                if extracted_data:
                    try:
                        # Store the extracted in a seperate text files each time
                        with open(f"textData/{link_num}.txt", 'w', encoding='utf-8') as text_file: 
                            text_file.write('\n'.join(extracted_data) + '\n')
                            link_num+=1
                        # print(f"Successfully wrote data to {text_file_path}")
                        
                    except Exception as e:
                        print(f"An error occurred while writing to file : {e}")
                else:
                    fail+=1
            else:
                fail+=1
# Folder containing the CSV files
csv_folder_path = './'  # Update with your CSV folder path
# Directory to save the text files
corpus_directory = './data'  # Update with your text data folder path


# Call the function with the provided path
print("Starting the processing of CSV files...")
process_csv_folder(csv_folder_path)
print("Processing complete.")
