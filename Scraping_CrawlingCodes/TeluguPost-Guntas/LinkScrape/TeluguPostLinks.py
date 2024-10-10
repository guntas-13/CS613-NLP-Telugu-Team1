from bs4 import BeautifulSoup
import urllib.request
import csv
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

base_url = "https://www.telugupost.com/crime"
csv_lock = threading.Lock()
progress_lock = threading.Lock()
total_pages = 253
completed_pages = 0


def get_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    articles = soup.find_all('article')
    links = []
    for article in articles:
        link = "https://www.telugupost.com" + article.find('a')['href']
        links.append(link)
    return links


def write_to_csv(links, csv_path):
    with csv_lock:
        if not os.path.isfile(csv_path):
            with open(csv_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["links"])

        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            for link in links:
                writer.writerow([link])


def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            
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


def load_page(url, csv_path):
    global completed_pages
    page_content = crawl_data_from_link_with_retry(url)
    if page_content is None:
        print(f"Skipping {url} due to repeated failures.")
        return

    links = get_links(page_content)
    write_to_csv(links, csv_path)

    with progress_lock:
        completed_pages += 1
        print(f"Progress: {completed_pages}/{total_pages} pages completed")


urls = [base_url]
for i in range(2, 254):
    url = f"https://www.telugupost.com/crime/{i}"
    urls.append(url)


def main_run(urls, csv_path):
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(load_page, url, csv_path): url for url in urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred when processing {url}: {e}")


if __name__ == "__main__":
    main_run(urls, "./TeluguPostCrimeLinks.csv")
    print("Done")