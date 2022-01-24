import os
import time
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = dotenv_values(".env")
urls = list(config.values())[1:4]
driver_path = config['DRIVER_PATH']

options = webdriver.ChromeOptions()
options.headless = True
options.binary_location = config['BINARY_EXECUTABLE']

options.add_argument("--disable-notifications")
options.add_argument("--incognito")
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("prefs", {
    # "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": False,
    "plugins.always_open_pdf_externally": True
},
    # "excludeSwitches", ['enable-logging']
)


def wait_and_rename(download, download_dir, url, second_source):
    """

        Waits for the file to be downloaded and rename it as per requirement
        uses request module to download file from the download button which
        has _target="blank" attribute

    """

    files = [os.path.join(download_dir, basename) for basename in os.listdir(download_dir)]
    old_file = max(files, key=os.path.getctime)

    try:
        if type(download) is str:
            resource = requests.get(download)
            with open(os.path.join(download_dir, "filename.pdf"), 'wb') as file:
                file.write(resource.content)

        else:
            download.click()

        while True:
            files = [os.path.join(download_dir, basename) for basename in os.listdir(download_dir)]
            latest_file = max(files, key=os.path.getctime)

            # checks if new files completely downloaded or not
            if not latest_file.endswith('.crdownload') and os.path.getctime(latest_file) > os.path.getctime(old_file):
                file_name = url.split("/")[-1] + "-" + str(datetime.date.today()) + ".pdf"
                full_file_name = os.path.join(download_dir, file_name)

                if not second_source:
                    if os.path.exists(full_file_name):
                        os.remove(full_file_name)

                    os.rename(latest_file, full_file_name)

                print(f"Finished downloading {os.path.split(full_file_name)[-1]}")
                break

            else:
                print("Waiting for file to be downloaded")
                time.sleep(5)

    except Exception as e:
        print(f"Following error occured while downloading \n {e}")


def first_news_source(browser, url, download_dir):
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
        wait_and_rename(download, download_dir, name_url, False)


def second_news_source(browser, url, download_dir):
    browser.get(url)
    browser.find_element(By.ID, "txtEmail").send_keys(config['USER'])
    browser.find_element(By.ID, "txtPassword").send_keys(config['KEY'])
    browser.find_element(By.ID, "login-btn").click()

    for i in range(1, 3):
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                     f"//div[@class='profile-userpic kantipur'][{i}]"))).click()  # //div[text()='Login successful']
        name_url = browser.current_url
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='drop-down-holder']")))
        download = browser.find_element(By.XPATH, f"//div[@class='drop-down-holder']")

        wait_and_rename(download, download_dir, name_url, True)
        browser.get(url)
        time.sleep(5)


def third_news_source(browser, url, download_dir):
    browser.get(url)
    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continue']")))
        browser.find_element(By.XPATH, "//p[text()='Continue']").click()
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='ext-layouttoolbaricon-16']")))
        browser.find_element(By.XPATH, "//div[@id='ext-layouttoolbaricon-16']").click()
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Select All']")))
        browser.find_element(By.XPATH, "//div[text()='Select All']").click()
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Download']")))
        browser.find_element(By.XPATH, "//div[text()='Download']").click()
        WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='button']")))
        browser.find_element(By.XPATH, "//input[@type='button']").click()
        browser.switch_to.window(browser.window_handles[1])
        download = WebDriverWait(browser, 300).until(EC.element_to_be_clickable((By.XPATH,
                                                                                 "//*[@id='divInfo']/div[1]/div[2]/p[3]/span/a")))

        if options.headless:
            download = download.get_attribute('href')

        wait_and_rename(download, download_dir, "/".join(url.split(".")[:2]), False)

    except:
        pass


procedures = [first_news_source, second_news_source, third_news_source]

if __name__ == "__main__":
    with webdriver.Chrome(service=Service(executable_path=driver_path), options=options) as browser:
        for url, procedure in zip(urls, procedures):
            download_folder = url.split('.')[1].capitalize()
            download_dir = os.path.join(os.getcwd().split("source")[0], "Newspapers", download_folder)
            params = {'behavior': 'allow', 'downloadPath': download_dir}
            browser.execute_cdp_cmd('Page.setDownloadBehavior', params)
            procedure(browser, url, download_dir)
