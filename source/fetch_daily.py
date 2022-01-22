import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

load_dotenv()
url = os.environ['URL2']
download_dir = os.path.join(os.getcwd().split("source")[0], "Newspapers")

options = webdriver.ChromeOptions()
options.binary_location = os.environ['BINARY_EXECUTABLE']
options.add_argument("--incognito")
options.headless = True
options.add_experimental_option("prefs", {
                                "download.default_directory": download_dir,
                                "download.prompt_for_download": False,
                                "download.directory_upgrade": True,
                                "safebrowsing.enabled": True
                                })

driver_path = os.environ['DRIVER_PATH']

with webdriver.Chrome(service=Service(executable_path=driver_path), options=options) as browser:
    browser.get(url)
    source = browser.page_source
    soup = BeautifulSoup(source, 'lxml')
    content = soup.find('div', class_="pdf")
    news = content.find_all('a')[0].get('href')
    browser.get(news)
    time.sleep(5)
    download = browser.find_element(By.XPATH, "//button[@id='download']")
    try:
        download.click()

    except Exception as e:
        print(f"Following error occured {e}")

    time.sleep(1)
    print("downloaded")
