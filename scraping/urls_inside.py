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
    # for d in tqdm(dates):
    #for x in tqdm(range(9, 13)):
    for y in tqdm(range(6, 17)):
        x = 11
        day = f"{x}/{y}"
        url = f'{baseurl}/{2023}/{day}'
        #print(url)
        r = requests.get(url)
        txt = r.text
        soup = BeautifulSoup(txt, features="html.parser")
        classes = soup.find_all('h2', {'class': 'c-entry-box--compact__title'})
        links = []
        for i in classes:
            for j in i.find_all('a', href=True):
                links += [j]
        hrefs = [i['href'] for i in links if day in i['href']]
        if path.exists():
            mode = 'a'
        else:
            mode = 'w'
        with open(path, mode) as f:
            for link in hrefs:
                f.write(f"{link}\n")

        
        sleep(1)

#start: 07/07
#end: 12/24
# sports and/or football
collect_urls('2023/07/07', '2023/12/24', './data/insidenu_urls_log.txt', 'https://www.insidenu.com/archives')
#collect_urls('2023/7/7', '2023/7/8', './data/insidenu_urls_log.txt', 'https://www.insidenu.com/archives')


#print(requests.get('https://www.insidenu.com/archives/2023/7/7').text)
