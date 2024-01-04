from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm
import pandas as pd
import pathlib
from time import sleep

def daterange(start: str, end: str):
    """
    helper function for creating a range of dates to scrape
    inputs: start date, end date
    outputs: date range
    """
    s = pd.to_datetime(start)
    e = pd.to_datetime(end)
    return (s, e)

def make_date(year, month, day):
    """
    helper function that I need for some reason
    inputs: year, month, date
    output: one string with all three
    """
    month = str(month)
    day = str(day)

    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day

    output = f'{year}/{month}/{day}'
    return output




def collect_urls(start: str, end: str, path: str, baseurl:str):
    """
        Loops through the date range and extracts urls from each archive page
        inputs: start date, end date, path for storing urls, baseurl of the publication
        output: none (file at path should be populated with urls)
    """
    # establish the path for storing urls
    path = pathlib.Path(path)

    #create date range
    dates = daterange(start, end)
    dates = pd.date_range(dates[0], dates[1])

    #loop through all dates in the range, extract urls
    for d in tqdm(dates):
        day = make_date(d.year, d.month, d.day)
        url = f'{baseurl}/{day}'
        r = requests.get(url)
        txt = r.text
        soup = BeautifulSoup(txt, features="html.parser")
        links = soup.find_all('a', {'class': 'homeheadline'})
        for i in links:
            link = i['href']
            if day in link:
                if path.exists():
                    mode = 'a'
                else:
                    mode = 'w'
                with open(path, mode) as f:
                    f.write(f"{link}\n")
        
        sleep(1)

#start: 07/07
#end: 12/24
collect_urls('2023/09/07', '2023/09/20', './data/urls_log.txt', 'https://dailynorthwestern.com')
