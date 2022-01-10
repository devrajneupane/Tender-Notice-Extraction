import os
import base64
import requests
from bs4 import BeautifulSoup

url_list = []
url = "aHR0cHM6Ly9nb3JraGFwYXRyYS5vcmcubnAvbm90aWNlcyZmaWx0ZXJfY2F0ZWdvcnlfaWQ9Ngo="
url = str(base64.b64decode(url), "utf-8")
download_dir = "Downloads"


def grep_url(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    ul_tag = soup.find('ul', class_="list list-icons list-primary")
    for li_tag in ul_tag.find_all('li'):
        a_tag = li_tag.find('a')
        link = a_tag.get('href')
        if link.startswith('download'):
            full_url = (url.split('notices')[0] + link).replace(' ', '%20')
            url_list.append(full_url)

    try:
        next_content = soup.find_all(class_="page-item")

        for item in next_content:
            if item.string == '>':
                next_link = item.a.get('href')

        grep_url(next_link)

    except:
        return


grep_url(url)
os.chdir("..")  # Switch to parent working directory
try:
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)
    os.chdir(download_dir)

    for url in url_list:
        filename = url.split('/')[-1].replace('%20', ' ')  # grab the filename
        request_file = requests.get(url)
        with open(filename, 'wb') as output_file:
            output_file.write(request_file.content)
            print(f"{filename} Downloaded!")

except:
    pass  # Directory/File already exist or permission denied
