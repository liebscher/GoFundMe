# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:48:43 2018

@author: loren
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import numpy as np
import pandas as pd

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

print(DRIVER_BIN)

url = 'https://www.gofundme.com/mvc.php?route=homepage_norma/search&term=breast%20cancer'

def extract_urls_from_categories(url, MoreGFMclicks = 5):

    driver = webdriver.Chrome(executable_path = DRIVER_BIN)
    driver.get(url)

    for i in range(MoreGFMclicks):
        for elem in driver.find_elements_by_link_text('Show More'):
            try:
                elem.click()
                print('Succesful click %s' %(i+1))
            except:
                print('Unsuccesful click %s' %(i+1))

            sleep(3) #longer delay - more successful

    source = driver.page_source

    driver.close()

    soup = BeautifulSoup(source, 'lxml')

    containers = soup.findAll("div", {"class": "cell grid-item small-6 medium-4 js-fund-tile"})

    temp_url = pd.read_csv('data-raw/cancer_urls.csv')['url'].tolist()

    c = 0
    for container in containers:
        for link in container.find_all('a'):
            if link.get('href') not in temp_url:
                temp_url.append(link.get('href'))
                c += 1

    print('Found %d' % c)

    return temp_url

pd.DataFrame({'url': extract_urls_from_categories(url, 50)}).to_csv('data-raw/cancer_urls2.csv', index=False)