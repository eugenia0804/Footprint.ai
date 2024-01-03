from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm
import pandas as pd

def collect_urls(start: str, end: str, path: str, baseurl:str):
    """
        Loops through the date range and extracts urls from each archive page
    """
    url = baseurl + start
    #print(url)
    url_end = baseurl + end

    r = requests.get(url)
    # for i in BeautifulSoup(r.text).find_all('a', {'class': 'homeheadline'}):
    #     print(f"{i}\n")
    soup = BeautifulSoup(r.text).find_all('a', {'class': 'homeheadline'})
    for i in soup:
        if start in i['href']:
            print(i['href'])


collect_urls('2023/07/07', '2023/12/24/', '', 'https://dailynorthwestern.com/')


