import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os
from concurrent.futures import ThreadPoolExecutor

links = pd.read_csv(r"./Links/suryaa_failed.csv")["urls"].tolist()

failed_links = []

if not os.path.exists(r"/home/devil/Desktop/Texts/suryaa"):
    os.makedirs(r"/home/devil/Desktop/Texts/suryaa")

def fetch_and_save(link, index):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find("h1").get_text(strip=True)
        text_elements = soup.find("div", class_="col-md-12").find_all("p")
        text = "\n".join([elem.get_text(strip=True) for elem in text_elements])
        
        with open(f"/home/devil/Desktop/Texts/suryaa/{index}.txt", 'w', encoding='utf-8') as f:
            f.write(f"{title}\n\n{text}")
        
        print(f"Done {index+1}/{len(links)}")
    except Exception as e:
        print(f"Failed {index+1}/{len(links)}: {e}")
        failed_links.append(link)

with ThreadPoolExecutor(max_workers=30) as executor:
    for i, link in enumerate(links):
        executor.submit(fetch_and_save, link, i)

if failed_links:
    with open(r"./Links/surya.csv", 'w', newline='', encoding='utf-8') as failed_csv:
        writer = csv.writer(failed_csv)
        writer.writerow(["urls"])
        writer.writerows([[link] for link in failed_links])
    print(f"Failed links saved to ./Links/suryaa_failed.csv")
