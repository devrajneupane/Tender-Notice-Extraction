import os
import base64
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

url_list = []
url = "aHR0cHM6Ly9nb3JraGFwYXRyYS5vcmcubnAvbm90aWNlcyZmaWx0ZXJfY2F0ZWdvcnlfaWQ9Ngo="
url = str(base64.b64decode(url), "utf-8")
download_dir = "Downloads"
request_adapter = HTTPAdapter(max_retries=3)


def grep_url(url):
    with requests.Session() as session:  # session will be released after use
        # use request_adapter for all request that starts with url
        session.mount(url.split('notices')[0], request_adapter)
        try:
            source = session.get(url)
            soup = BeautifulSoup(source.text, 'lxml')

            ul_tag = soup.find('ul', class_="list list-icons list-primary")

            for li_tag in ul_tag.find_all('li'):
                a_tag = li_tag.find('a')
                link = a_tag.get('href')

                if link.startswith('download'):
                    full_url = (url.split('notices')[0] + link).replace(' ', '%20')
                    url_list.append(full_url)

            next_content = soup.find_all(class_="page-item")

            for item in next_content:
                if item.string == '>':
                    next_link = item.a.get('href').replace('6_&', '6&')
                    break

            grep_url(next_link)

        except Exception as err:
            if len(url_list) < 80:
                print(f"Following error occured\n {err}")
                os._exit(0)
            return


grep_url(url)
os.chdir("..")  # Switch to parent working directory

try:
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)

    os.chdir(download_dir)

    with requests.Session() as session:
        session.mount(url.split('notices')[0], request_adapter)

        for url in url_list:
            filename = url.split('/')[-1].replace('%20', ' ')  # grab the filename

            if not os.path.exists(filename):  # download file if it doesn't exist already
                with open(filename, 'wb') as output_file:
                    request_file = session.get(url)
                    output_file.write(request_file.content)
                    print(f"{filename} Downloaded!")
            else:
                print(f"{filename} already exist!")

except Exception as err:
    # Permission denied or Connection Error
    print(f"Error occured!!!\n {err}")
