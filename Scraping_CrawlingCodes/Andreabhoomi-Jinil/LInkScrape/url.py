#code with threading
from bs4 import BeautifulSoup
import requests
import csv
import os
import pandas as pd
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add random delay to avoid request timeout
def random_delay(min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    # print(f"Waiting for {delay:.2f} seconds...")
    time.sleep(delay)

# Function to extract links from the specific HTML content section
def extract_links(html_content, base_url):
    links = []
    soup = BeautifulSoup(html_content, "html.parser")
    # print("Title:", soup.title.get_text())

    # Find the specific div section
    main_content_div = soup.find("div", class_="view-content")
    if main_content_div:
        rows = main_content_div.find_all("div", class_="views-row")
        for row in rows:
            link_tag = row.find("span", class_="field-content").find("a", href=True)
            if link_tag:
                link = link_tag['href']
                full_link = f"{base_url}{link}"
                links.append(full_link)
    # else:
        # print("Main content div not found.")
    return links

def fetch_html(url, max_retries=3, delay=1):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
            else:
                # print(f"Failed to fetch HTML from {url} with status code {response.status_code}")
                return None
        except Exception as e:
            # print(f"An error occurred while fetching HTML from {url}: {e}")
            retries += 1
            # print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
    # print(f"Max retries exceeded for {url}.")
    return None

def save_links_to_csv(links, csv_file_path):
    if links:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for link in links:
                writer.writerow([link])
        # print(f"Links saved to {csv_file_path}")

        # Remove duplicates within the CSV file
        df = pd.read_csv(csv_file_path, header=None)
        df.drop_duplicates(inplace=True)
        df.to_csv(csv_file_path, index=False, header=False)
    # else:
        # print(f"No links found to save for {csv_file_path}")

def process_page(page_num, base_url, corpus_dir, link_base_url):
    if page_num == 1:
        url = base_url
    else:
        url = f"{base_url}?page={page_num - 1}"

    csv_file_path = os.path.join(corpus_dir, f"{page_num}.csv")

    # Fetch HTML content
    html_content = fetch_html(url)
    if html_content:
        links = extract_links(html_content, link_base_url)
        save_links_to_csv(links, csv_file_path)
    else:
        # print(f"Failed to fetch HTML content for page {page_num}")
        random_delay(50, 60)
        return url
    return None

def main(base_url, corpus_dir, num_pages, max_workers=10):
    failed_urls = []
    link_base_url = "http://www.andhrabhoomi.net"

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_page = {executor.submit(process_page, page_num, base_url, corpus_dir, link_base_url): page_num for page_num in range(26229, num_pages + 1)}

        for future in as_completed(future_to_page):
            page_num = future_to_page[future]
            try:
                failed_url = future.result()
                if failed_url:
                    failed_urls.append(failed_url)
            except Exception as exc:
                # print(f"Page {page_num} generated an exception: {exc}")
                failed_urls.append(f"http://www.andhrabhoomi.net/category?page={page_num - 1}")

    failed_csv_path = os.path.join(corpus_dir, "failed_urls.csv")

    if failed_urls:
        # print("----------------------------------------")
        # print(f"Saving Failed URLs to {failed_csv_path}")
        # print("----------------------------------------")
        if not os.path.isfile(failed_csv_path):
            with open(failed_csv_path, 'w', newline='', encoding='utf-8') as failed_csv:
                fieldnames = ['failed_url']
                writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
                writer.writeheader()

        with open(failed_csv_path, 'a', newline='', encoding='utf-8') as failed_csv:
            fieldnames = ['failed_url']
            writer = csv.DictWriter(failed_csv, fieldnames=fieldnames)
            for url in failed_urls:
                writer.writerow({'failed_url': url})
        # print("Failed URLs appended to:", failed_csv_path)

base_url = "http://www.andhrabhoomi.net/category"
corpus_dir = 'Links_csv/'
num_pages = 27003

main(base_url, corpus_dir, num_pages, max_workers=10)