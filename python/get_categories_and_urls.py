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

url = 'https://www.gofundme.com/mvc.php?route=homepage_norma/search&term=cancer'

def extract_urls_from_categories(url, MoreGFMclicks = 5):

    # eg. url = 'https://www.gofundme.com/discover/medical-fundraiser'
    driver = webdriver.Chrome(executable_path = DRIVER_BIN)
    driver.get(url)

    for i in range(MoreGFMclicks):
        for elem in driver.find_elements_by_link_text('Show More'):
            try:
                elem.click()
                print('Succesful click %s' %(i+1))#make this more useful- say what category it is e.g. url.get_category()
            except:
                print('Unsuccesful click %s' %(i+1))

            sleep(0.8) #longer delay - more succesful

    source = driver.page_source

    driver.close()

    soup = BeautifulSoup(source, 'lxml')

    containers = soup.findAll("div", {"class": "cell grid-item small-6 medium-4 js-fund-tile"})

    temp_url = []
    i = 1

    for container in containers:
        for link in container.find_all('a'):
            temp_url.append(link.get('href'))

    return temp_url

print(extract_urls_from_categories(url, 2))