# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from time import sleep
import requests
import re
from datetime import datetime

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

headers = ["url", "name", "location", "launched", "month", "year", "amt_raised", "goal", "backers", "mean_donation",
           "text_length_words", "duration", "text"]

def scrape_url(url):
    
    page = requests.get(url)
         
    soup = BeautifulSoup(page.text, 'lxml')
    #contains amount raised - goal amount - # of donators - length of fundraising
    try:
        container = soup.find_all("div",{"class":"layer-white hide-for-large mb10"})
        info_string = container[0].text
        info_string = info_string.splitlines()
        info_string = list(filter(None, info_string))
        
        amount_raised = int(info_string[0][1:].replace(',',''))
        
        goal = int(re.findall('\$(.*?) goal', info_string[1])[0].replace(',',''))
        
        NumDonators = int(re.findall('by (.*?) people', info_string[2])[0].replace(',',''))
        
        timeFundraised = re.findall("in (.*)$", info_string[2])[0]
    except:
        amount_raised = np.nan
        goal = np.nan
        NumDonators = np.nan
        timeFundraised = np.nan

    try:
        launched = soup.find('div', {'class': 'created-date'}).text[8:]
        launched = datetime.strptime(launched, '%B %d, %Y')

        month = launched.month
        year = launched.year
    except:
        launched = np.nan
        month = np.nan
        year = np.nan
    
    title_container = soup.find_all("h1",{"class": "campaign-title"})#<h1 class="campaign-title">Help Rick Muchow Beat Cancer</h1>
    
    try:
        title = title_container[0].text
    except:
        title = np.nan
    
    text_container = soup.find('div', {'class': 'co-story'})
    
    try:
        all_text = text_container.text.strip()
        text_length_words = len(tokenizer.tokenize(all_text))

    except:
        all_text = np.nan
        text_length_words = np.nan
    
    # try:
    #     FB_shares_container = soup.find_all("strong", {"class":"js-share-count-text"})
    #     FB_shares = FB_shares_container[0].text.splitlines()
    #     FB_shares = FB_shares[1].replace(" ", "").replace("\xa0", "")
    # except:
    #     FB_shares = np.nan
        
    # try:
    #     hearts_container = soup.find_all("div", {"class":"campaign-sp campaign-sp--heart fave-num"})
    #     hearts = hearts_container[0].text
    # except:
    #     hearts = np.nan
    
    try:
        location_container = soup.find_all("div", {"class":"pills-contain"})
        location = location_container[0].text.splitlines()[-1]
        location = location.replace('\xa0', '').strip()
    except:
        location = np.nan
    
    return [url, title, location, launched, month, year, amount_raised, goal, NumDonators, amount_raised / NumDonators,
            text_length_words, timeFundraised, all_text]


def scrape_all_urls():
    urls = pd.read_csv('data-raw/cancer_urls.csv')['url'].values

    temp_list = []

    for url in urls:
        try:
            print("Scraping url", url)
            temp_list.append(scrape_url(url))

        except:
            sleep(1.25)
            print("Scraping url", url)
            temp_list.append(scrape_url(url))

    pd.DataFrame(temp_list, columns=headers).to_csv('data/gofundme_projects.csv', index=False)

        
scrape_all_urls()
