from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
url = "https://vignanam.org/telugu.html"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
anchors = [li.find_elements(By.TAG_NAME, "a") for li in driver.find_elements(By.CLASS_NAME, "aq3bullet")]
len(anchors)
links = [a.get_attribute("href") for anchor in anchors for a in anchor]
df = pd.DataFrame(links, columns=["urls"])
df.head()
df.to_csv("./Links/vignanam_links.csv", index=False)
