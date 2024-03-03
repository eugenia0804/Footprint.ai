import re
from time import sleep
from typing import List

from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm
import pathlib


def load_and_filter_urls(path: str) -> List[str]:
    with open(path, "r") as f:
        urls = f.readlines()
    urls = [i.replace("\n", "") for i in urls]

    urls = list(set(urls))
    urls = [i for i in urls]

    return urls

def scrape_article(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, features="html.parser")
    titles = [x.text for x in soup.find_all(["h2"])]
    if titles[0] != "FanShot":
        pub_dt = soup.find("time")['datetime']

        try:
            authors = soup.find_all("span", {'class': 'c-byline-wrapper'})[0].text
        except IndexError or AttributeError:
            authors = ''
        try:
            hed = soup.find("h1").contents[0]
        except IndexError:
            hed = ""

        try:
            art = soup.find("article")
            text = [i.text for i in art.find_all(["p", "h2"])]
        except AttributeError:
            text = ""
        try:
            comment_num = soup.find_all("span", {'class': "coral-count-number"})
        except AttributeError or IndexError:
            comment_num = 0

        result = {
            "url": url,
            "pub_date": pub_dt,
            "authors": authors,
            "hed": hed,
            "article_text": text,
            'article_comment_num': comment_num
        }

        return result

def collect_articles(url_path, storage_path):
    """
    function that loops through each link in the .txt file and scrapes
    """
    storage_path = pathlib.Path(storage_path)
    
    with open(url_path, 'r') as f:
        urls = list(f.read().splitlines())
    for u in tqdm(urls):
        contents = scrape_article(u)
        contents = pd.DataFrame([contents])
        if storage_path.exists():
                mode = "a"
                header = False
        else:
            mode = "w"
            header = True

        contents.to_csv(storage_path, mode=mode, header=header, index=False)

        sleep(1)

# print('\n')
# print(scrape_article('https://www.insidenu.com/2023/11/18/23966444/a-heartfelt-farewell-to-ryan-field'))
# print('\n')


# collect_articles('data/insidenu_urls_BEFORE_log.txt', 'data/inside_data_BEFORE.csv')

# pd.DataFrame([scrape_article('https://www.insidenu.com/2023/12/24/24013883/northwestern-footballs-las-vegas-bowl-win-caps-a-legendary-season-and-a-foundational-one')]).to_csv('data/inside_data_test.csv', mode='a', header=False, index=False)

#test = requests.get('https://www.insidenu.com/2023/11/16/23934334/how-new-head-coach-rachel-stratton-mills-plans-on-taking-northwestern-swim-and-dive-to-new-heights')
#print(BeautifulSoup(test.text).find_all('p'))

'''
this code could be optimized in the future by removing automatically any 'fanshot' links, as I did it by hand this time
'''

def features_text(urls):
    for i in urls:
        r = requests.get(i)
        soup = BeautifulSoup(r.text)
        text = [x.text for x in soup.find_all(["p"])]
        print(text, "\n\n")

features_text(['https://www.insidenu.com/2023/5/26/23737809/with-super-regionals-on-the-horizon-for-northwestern-softball-ties-to-2007-team-become-clear', 
               'https://www.insidenu.com/2023/6/13/23759047/put-that-whole-team-on-his-back-how-northwestern-boosted-quarterback-dan-persas-2011-heisman-hopes'])