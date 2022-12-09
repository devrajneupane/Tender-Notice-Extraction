import datetime
import os
import sys
import time
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from log import Logger
from utils import config

# enable browser logging
sys.stdout = Logger()

path = Path(__file__).parent.parent
webdriver_logs = path / "logs" / "ChromeDriver" / f"chromedriver-{str(datetime.date.today())}-.log"
urls = [config[key] for key in config.keys() if key.startswith('URL')]
wait_time = 60

options = webdriver.ChromeOptions()
options.headless = True

options.binary_location = config["BINARY_EXECUTABLE"]
options.add_argument("--disable-notifications")
options.add_argument("--incognito")
options.add_argument("--log-level=3")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": str(path / "Newspapers" / urls[0].split('.')[-2].capitalize()),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        # "download.open_pdf_in_system_reader": False,
        # "profile.default_content_settings.popups": 0,
        "safebrowsing.enabled": False,
        "plugins.always_open_pdf_externally": True,
    })
options.add_experimental_option("excludeSwitches", ['enable-logging'])

if len(sys.argv) >= 2 and sys.argv[1] == "--debug":
    if not sys.argv[-2].startswith("-p"):
        sys.argv.append(9222)
    options.add_argument(f"--remote-debugging-port={sys.argv[-1]}")
    # access debugged browser from external machine
    options.add_argument("--remote-debugging-address=0.0.0.0")


def wait_and_rename(download, download_dir, url, *args):
    sys.stdout = Logger()
    """

    Waits for the file to be downloaded and rename it as per requirement
    uses requests module to download file from the download button which
    has _target="blank" attribute

    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    files = [os.path.join(download_dir, basename) for basename in os.listdir(download_dir)]
    if files:
        old_file = max(files, key=os.path.getctime)
        old_file_ctime = os.path.getctime(old_file)

    else:
        old_file = None
        old_file_ctime = 0

    try:
        if type(download) is str:
            resource = requests.get(download)
            with open(os.path.join(download_dir, "filename.pdf"), "wb") as file:
                file.write(resource.content)

        else:
            download.click()
            time.sleep(1)

        while True:
            files = [os.path.join(download_dir, basename) for basename in os.listdir(download_dir)]
            if files:
                latest_file = max(files, key=os.path.getctime)
                latest_file_ctime = os.path.getctime(latest_file)
            else:
                latest_file = str(None)
                latest_file_ctime = 0

            if len(sys.argv) > 1 and sys.argv[1] == "--debug":
                png_path = os.path.join(sys.path[0].split("source")[0], "Screenshots")

                if not os.path.exists(png_path):
                    os.makedirs(png_path)

                args[0].save_screenshot(os.path.join(png_path, f"{download_dir.split('/')[-1]}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"))
                print(f"{latest_file.endswith('.crdownload') = }\n{latest_file = }\n{old_file = }")

            # checks if new file completely downloaded or not
            if not latest_file.endswith(".crdownload") and latest_file_ctime > old_file_ctime:
                file_name = url.split("/")[-1] + "-" + str(datetime.date.today()) + ".pdf"
                full_file_name = os.path.join(download_dir, file_name)

                if not args[-1]:
                    if os.path.exists(full_file_name):
                        os.remove(full_file_name)

                    os.rename(latest_file, full_file_name)

                print(f"Finished downloading {os.path.split(full_file_name)[-1]}")
                break

            else:
                print("Waiting for file to be downloaded")
                time.sleep(5)

    except Exception as e:
        print(f"Following error occured while downloading from {url}\n {e}")


def first_news_source(browser, url, download_dir):
    sys.stdout = Logger()
    for i in range(1, 3):
        browser.get(url)
        browser.find_element(By.XPATH, f"//div[@class='epapercategory']//a[{i}]").click()
        name_url = browser.current_url
        browser.find_element(By.XPATH, f"//div[@class='papersection']//div[1]").click()
        browser.switch_to.window(browser.window_handles[-1])
        WebDriverWait(browser, wait_time * 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="download"]')) # //div[@class='textLayer']
        )
        download = browser.find_element(By.XPATH, "//button[@id='download']")
        wait_and_rename(download, download_dir, name_url, browser, False)


def second_news_source(browser, url, download_dir):
    sys.stdout = Logger()
    browser.get(url)

    browser.find_element(By.ID, "txtEmail").send_keys(config["USER"])
    browser.find_element(By.ID, "txtPassword").send_keys(config["KEY"])
    browser.find_element(By.ID, "login-btn").click()

    for i in range(1, 3):
        WebDriverWait(browser, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='profile-userpic kantipur'][{i}]"))
        ).click()  # //div[text()='Login successful']
        name_url = browser.current_url
        WebDriverWait(browser, wait_time * 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='drop-down-holder']")))
        download = browser.find_element(By.XPATH, f"//div[@class='drop-down-holder']")

        wait_and_rename(download, download_dir, name_url, browser, True)
        browser.get(url)
        time.sleep(5)


def third_news_source(browser, url, download_dir):
    sys.stdout = Logger()
    browser.get(url)
    try:
        WebDriverWait(browser, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='Continue']"))
        ).click()
        WebDriverWait(browser, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='ext-layouttoolbaricon-17']"))
        ).click()
        WebDriverWait(browser, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Select All']"))
        ).click()
        WebDriverWait(browser, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Download']"))
        ).click()
        WebDriverWait(browser, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button']"))
        ).click()
        browser.switch_to.window(browser.window_handles[-1])
        download = WebDriverWait(browser, wait_time * 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='divInfo']/div[1]/div[2]/p[3]/span/a")))

        if options.headless:
            download = download.get_attribute("href")

        wait_and_rename(download, download_dir, "/".join(url.split(".")[:2]), browser, False)

    except Exception as e:
        print(f"Fowllowing error occured while downloading pdf from f{url}\n{e}")
        pass


procedures = [first_news_source, second_news_source, third_news_source]


def get_resource():
    sys.stdout = Logger()

    print("\n========Downloading PDF from newsportals=======\n")
    with webdriver.Chrome(service=Service(executable_path=config["DRIVER_PATH"], log_path=str(webdriver_logs)), options=options) as browser:
        for url, procedure in zip(urls, procedures):
            now = datetime.datetime.now()
            download_folder = url.split(".")[1].capitalize()
            download_dir = os.path.join(sys.path[0].split("source")[0], "Newspapers", download_folder)
            params = {"behavior": "allow", "downloadPath": download_dir}
            browser.execute_cdp_cmd("Page.setDownloadBehavior", params)
            # if now.hour >= 11:
            #     if procedure == procedures[1]:
            #         procedure(browser, url, download_dir)
            #         break
            #     else:
            #         continue
            # elif procedure != procedures[1]:
            #     procedure(browser, url, download_dir)
            procedure(browser, url, download_dir)


if __name__ == "__main__":
    sys.stdout = Logger(datetime.datetime.now())
    get_resource()
