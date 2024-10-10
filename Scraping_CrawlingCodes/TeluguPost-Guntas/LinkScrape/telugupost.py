from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

urls = [
    'https://www.telugupost.com/politics/', 
    'https://www.telugupost.com/sports/',
    'https://www.telugupost.com/andhra-pradesh',
    'https://www.telugupost.com/telangana/',
    'https://www.telugupost.com/health-lifestyle',
    'https://www.telugupost.com/opinion/',
    'https://www.telugupost.com/crime',
    'https://www.telugupost.com/movie-news',
    'https://www.telugupost.com/hyderabad',
    'https://www.telugupost.com/visakhapatnam',
    'https://www.telugupost.com/national',
    'https://www.telugupost.com/international',
    'https://www.telugupost.com/special-story'
]

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
except:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    print("Running in headless mode.")

file = open('./Links/telugupost.txt', 'a' )
failed = open('./Links/failed_telugupost.txt', 'a')

for url in urls:
    driver.get(url)
    print("Getting links from", driver.current_url)
    i = 0;
    fc = 0
    while True:
        try:
            articles = driver.find_elements(By.TAG_NAME, 'article')
            next_button = driver.find_element(By.CLASS_NAME, 'nav-links').find_elements(By.TAG_NAME, 'a')
            for article in articles:
                file.write(article.find_element(By.TAG_NAME, 'figure').find_element(By.TAG_NAME, 'a').get_attribute('href') + '\n')
            next_button[-1].click()
            if i != 0 and len(next_button) == 1:
                break
            i += 1
        except:
            fc+=1
            if fc == 3:
                try:
                    next_button = driver.find_element(By.CLASS_NAME, 'nav-links').find_elements(By.TAG_NAME, 'a')
                    next_button[-1].click()
                    fc = 0
                except:
                    break
            print(f"Failed to get links from {driver.current_url}")
            failed.write(driver.current_url + '\n')
        if i%100 == 0:
            print(f"Done {i} pages")

file.close()
failed.close()
driver.close()

        

