import os
import csv
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import json

def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            link = urllib.parse.quote(link, safe=':/')
            req = urllib.request.Request(
                link, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            response = urllib.request.urlopen(req)
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

def extract_data_from_html(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        scripts = soup.find_all('script', {'type': 'application/ld+json'})
        extracted_data = json.loads(scripts[0].text)["articleBody"]

    except Exception as e:
        print(f"An error occurred while extracting Telugu data: {e}")

    return extracted_data

def process_link_and_write(index, link, text_file_path):
    html_content = crawl_data_from_link_with_retry(link)
    if html_content:
        extracted_data = extract_data_from_html(html_content)
        if extracted_data:
            try:
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    title = df["title"][index] if 'title' in df.columns else "No Title"
                    text_file.write(f"{title}\t{link}\n")
                    text_file.write(extracted_data)
                return True
            except Exception as e:
                print(f"An error occurred while writing to file {text_file_path}: {e}")
                return False
    return False

def process_all_links(df, output_folder, failed_csv_path):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    failed_links = []
    total_links = len(df)
    processed_count = 0

    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = []
        for i in range(len(df)):
            link = df["links"][i]
            text_file_path = os.path.join(output_folder, f"{i}.txt")
            futures.append(executor.submit(process_link_and_write, i, link, text_file_path))
        for future in as_completed(futures):
            try:
                success = future.result()
                processed_count += 1
                print(f"Processed: {processed_count}/{total_links} links")
                if not success:
                    failed_links.append(link)
            except Exception as e:
                print(f"An error occurred while processing a link: {e}")
                failed_links.append(link)

    if failed_links:
        with open(failed_csv_path, 'w', newline='', encoding='utf-8') as failed_csv:
            writer = csv.writer(failed_csv)
            writer.writerow(["Failed Links"])
            writer.writerows([[link] for link in failed_links])
        print(f"Failed links saved to {failed_csv_path}")


csv_path = "./TeluguPost-Guntas/LinkScrape/TeluguPostLinks.csv"

df = pd.read_csv(csv_path)

if __name__ == "__main__":
    output_folder = "../TeluguData/TeluguPost"
    failed_csv_path = "./failed_links_tePost.csv"

    print("Starting the processing of all links...")
    process_all_links(df, output_folder, failed_csv_path)
    print("Processing complete.")
