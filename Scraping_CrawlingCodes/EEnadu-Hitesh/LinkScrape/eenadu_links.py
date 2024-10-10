import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

today = datetime.today()
dates = [(today - timedelta(days=i)).strftime('%d-%m-%Y') for i in range(1, 7)]
urls = ["https://eenadu.net/archives/home/" + date for date in dates]

def fetch_links(url):
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pages = soup.find('div', class_='two-col-left-block').find_all('a', class_='more2')
    page_urls = [page['href'] for page in pages]

    for page_url in page_urls:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find('ul', class_='article-box-list').find_all('a')
        for article in articles:
            links.append(article['href'])
    return links

all_links = []
with ThreadPoolExecutor(max_workers=30) as executor:
    results = executor.map(fetch_links, urls)
    for result in results:
        all_links.extend(result)

df = pd.DataFrame(all_links, columns=['urls'])
df.to_csv('./Links/eenadu_links.csv', index=False)
