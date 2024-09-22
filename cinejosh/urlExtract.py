import requests
from bs4 import BeautifulSoup
import csv
import os
import threading

# Function to extract links from the HTML content
def extract_links(html_content):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    articles = soup.find_all('div', class_='col-xs-12 col-sm-12 col-md-8')
    for article in articles:
        a_tags = article.find_all('a', href=True)
        for a_tag in a_tags:
            link = a_tag['href']
            if link not in links:
                # Prepend base URL to each link
                full_link = f"https://www.cinejosh.com{link}"
                links.append(full_link)
    return links

# Function to write links to CSV and remove duplicates
def write_links_to_csv(links, csv_file_path):
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['link'])

    existing_links = set()
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                existing_links.add(row[0])

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            if link not in existing_links:
                writer.writerow([link])
                existing_links.add(link)

# Function to load content from a specific page
def load_page_content(url, csv_file_path):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        links = extract_links(html_content)
        write_links_to_csv(links, csv_file_path)
    else:
        print(f"Failed to retrieve page: {url}")

# Function to process a single category
def process_category(category, base_url, max_pages, base_directory):
    try:
        print(f"Processing category: {category}")
        csv_file_path = os.path.join(base_directory, f"{category}.csv")
        
        for page in range(1, max_pages + 1):
            page_url = f"{base_url}/{page}.html"
            print(f"Processing page {page} of {category}")
            load_page_content(page_url, csv_file_path)
            print(f"Links from page {page} saved to {csv_file_path}")

    except Exception as e:
        print(f"An error occurred while processing {category}: {e}")

# Main function to process each category concurrently
def main(base_urls, max_pages_list, base_directory):
    threads = []
    for idx, (category, url) in enumerate(base_urls.items()):
        max_pages = max_pages_list[idx]
        thread = threading.Thread(target=process_category, args=(category, url, max_pages, base_directory))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# URLs for different categories with their respective max pages
base_urls = {
    "gossips": "https://www.cinejosh.com/telugu-list/4",
    "movies": "https://www.cinejosh.com/telugu-list/2", 
}

# Maximum pages for each category
max_pages_list = [1218, 366]

# Base directory to save CSV files
base_directory = './'

# Ensure the base directory exists
os.makedirs(base_directory, exist_ok=True)

# Run the main function
main(base_urls, max_pages_list, base_directory)