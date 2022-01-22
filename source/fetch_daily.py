import os
import time
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

load_dotenv()
url = os.environ['URL2']
download_folder = url.split('.')[1].capitalize()
download_dir = os.path.join(os.getcwd().split("source")[0], "Newspapers", download_folder)

options = webdriver.ChromeOptions()
options.binary_location = os.environ['BINARY_EXECUTABLE']
options.add_argument("--incognito")
# options.headless = True
options.add_experimental_option("prefs", {
                                "download.default_directory": download_dir,
                                "download.prompt_for_download": False,
                                "download.directory_upgrade": True,
                                "safebrowsing.enabled": True
                                })

driver_path = os.environ['DRIVER_PATH']


def wait_and_rename(download_dir, browser, url):
    latest_file = ""
    browser.get('brave://downloads')
    while True:
        try:
            # get downloaded percentage
            percentage_download = browser.execute_script(
                "return document.querySelector('downloads-manager')"
                ".shadowRoot.querySelector('#downloadsList downloads-item')"
                ".shadowRoot.querySelector('#progress').value")
            print(f"{percentage_download}% downloaded")

            if percentage_download == 100:
                # ruturn the name of completely downloaded file
                latest_file = browser.execute_script(
                    "return document.querySelector('downloads-manager')"
                    ".shadowRoot.querySelector('#downloadsList downloads-item')"
                    ".shadowRoot.querySelector('div#content  #file-link').text")
                latest_file = os.path.join(download_dir, latest_file)
                break

        except Exception as e:
            print(f"Following error occured while checking download \n {e}")

        time.sleep(.5)

    file_name = url.split("/")[-1] + "-" + str(datetime.date.today()) + ".pdf"
    full_file_name = os.path.join(download_dir, file_name)

    if os.path.exists(full_file_name):
        os.remove(full_file_name)

    time.sleep(5)
    os.rename(latest_file, full_file_name)
    print(f"Finished downloading {os.path.split(full_file_name)[-1]}")


with webdriver.Chrome(service=Service(executable_path=driver_path), options=options) as browser:
    for i in range(1, 3):
        browser.get(url)
        browser.find_element(By.XPATH, f"//div[@class='epapercategory']//a[{i}]").click()
        name_url = browser.current_url
        source = browser.page_source
        soup = BeautifulSoup(source, 'lxml')
        content = soup.find('div', class_="pdf")
        news = content.find_all('a')[0].get('href')
        browser.get(news)
        time.sleep(5)
        download = browser.find_element(By.XPATH, "//button[@id='download']")

        try:
            download.click()
            wait_and_rename(download_dir, browser, name_url)

        except Exception as e:
            print(f"Following error occured \n {e}")
