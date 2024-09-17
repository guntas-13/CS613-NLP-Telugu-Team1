from bs4 import BeautifulSoup
import urllib.request
import csv
import os
import time

base_url = "https://telugustop.com/telugu/daily-update-categories/telugu-andhra-telangana-tollywood-latest-political-movie-celebrity-live-news-updates-mobile-website"
total_pages = 1050
completed_pages = 0


def get_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    main_div = soup.find('div', class_='band')
    anchors = main_div.find_all('a', class_="read-more", href=True)
    links = [a['href'] for a in anchors]
    return links


def write_to_csv(links, csv_path):
    if not os.path.isfile(csv_path):
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["links"])

    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for link in links:
            writer.writerow([link])


def crawl_data_from_link_with_retry(link, max_retries=3, retry_interval=5):
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


def load_page(url, csv_path):
    global completed_pages
    page_content = crawl_data_from_link_with_retry(url)
    if page_content is None:
        print(f"Skipping {url} due to repeated failures.")
        return

    links = get_links(page_content)
    write_to_csv(links, csv_path)

    completed_pages += 1
    print(f"Progress: {completed_pages}/{total_pages} pages completed")


urls = [base_url]  # Start with the base URL
for i in range(1, 1051):
    url = f"https://telugustop.com/telugu/daily-update-categories/telugu-andhra-telangana-tollywood-latest-political-movie-celebrity-live-news-updates-mobile-website/page/{i}?desktop=yes"
    urls.append(url)


def main_run(urls, csv_path):
    for url in urls:
        load_page(url, csv_path)


# if __name__ == "__main__":
#     main_run(urls, "./TeluguStop-GuntasNew.csv")
#     print("Done")