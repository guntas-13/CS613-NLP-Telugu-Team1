import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os
from concurrent.futures import ThreadPoolExecutor

url = "https://vignanam.org/telugu.html"

links = pd.read_csv(r"./Links/vignanam_links.csv")["urls"].tolist()

failed_links = []

if not os.path.exists(r"/home/devil/Desktop/Texts/vignanam"):
    os.makedirs(r"/home/devil/Desktop/Texts/vignanam")

def fetch_and_save(link, index):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find(id="stitle").get_text(strip=True)
        text_elements = soup.find(id="stext").find_all("span")
        text = "\n".join([elem.get_text(strip=True) for elem in text_elements])
        
        with open(f"/home/devil/Desktop/Texts/vignanam/{index}.txt", 'w', encoding='utf-8') as f:
            f.write(f"{title}\n\n{text}")
        
        print(f"Done {index+1}/{len(links)}")
    except Exception as e:
        print(f"Failed {index+1}/{len(links)}: {e}")
        failed_links.append(link)

with ThreadPoolExecutor(max_workers=30) as executor:
    for i, link in enumerate(links):
        executor.submit(fetch_and_save, link, i)

if failed_links:
    with open(r"./Links/vignanam_failed.csv", 'w', newline='', encoding='utf-8') as failed_csv:
        writer = csv.writer(failed_csv)
        writer.writerow(["Failed Links"])
        writer.writerows([[link] for link in failed_links])
    print(f"Failed links saved to ./Links/vignanam_failed.csv")
