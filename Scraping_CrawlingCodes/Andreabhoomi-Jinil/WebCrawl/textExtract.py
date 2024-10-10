from bs4 import BeautifulSoup
import re
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


def crawl_data(link, max_retries=3, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            response = urllib.request.urlopen(link)
            if response.status == 200:
                return response.read()
            else:
                retries += 1
                time.sleep(retry_interval)
        except Exception as e:
            print(f"An error occurred while fetching data from {link}: {e}. Retrying...")
            retries += 1
            time.sleep(retry_interval)
    return None

def extract_data(html_content):
    extracted_data = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        main_div = soup.find('div', id='block-system-main')
        if main_div:
            p_elements = main_div.find_all('p')
            for p in p_elements:
                p_text = p.get_text(separator=' ').strip()
                extracted_data.append(p_text)
    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")

    return extracted_data

def process_link_and_write(link, text_file_path):
    html_content = crawl_data(link)
    if html_content:
        extracted_data = extract_data(html_content)
        if extracted_data:
            try:
                with open(text_file_path, 'a', encoding='utf-8') as text_file:
                    text_file.write('\n'.join(extracted_data) + '\n')
                return True
            except Exception as e:
                print(f"An error occurred while writing to file {text_file_path}: {e}")
    return False

# Function to process all CSV files in a directory
csv_folder_path = 'Links_csv/'
corpus_directory = 'Andhre_bhoomi_data/'
if not os.path.exists(corpus_directory):
    os.makedirs(corpus_directory)

csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
csv_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

count = 0
for csv_files_name in csv_files:
    csv_file_path = os.path.join(csv_folder_path, csv_files_name)
    text_file_path = os.path.join(corpus_directory, f"{os.path.splitext(csv_files_name)[0]}.txt")
    with open(csv_file_path, 'r', encoding='ISO-8859-1') as csv_file:
        count += 1
        if count%100 == 0:
            print(count)
        csv_reader = csv.reader(csv_file)

        links = [row[0] for row in csv_reader]
        for link in links:
            html_content = crawl_data(link)
            if html_content:
                extracted_data = extract_data(html_content)
                if extracted_data:
                    try:
                        with open(text_file_path, 'a', encoding='utf-8') as text_file:
                            text_file.write('\n'.join(extracted_data) + '\n')
                    except Exception as e:
                        print(f"An error occurred while writing to file {text_file_path}: {e}")