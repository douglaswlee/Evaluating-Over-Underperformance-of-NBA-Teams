from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import os
import requests

import pandas as pd

def scrape_nbacom_by_url(start, end, url):
    '''Scrape team statistics from NBA.com over a range of seasons (in reverse order) given:
    start, the end year of the first season in the range
    end, the end year of the last season in the range
    url, the url of the page with the team stats to be scraped
    
    Output:
    df_main, a dataframe combining all team stats for the entire range of seasons
    '''
    chromedriver = "/Applications/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver

    driver = webdriver.Chrome(chromedriver)

    driver.get(url)
    
    how_many_seasons = end - start + 1
    k = 1
    year = end
    df_main = pd.DataFrame()


    for season in driver.find_elements_by_xpath('.//select[@name="Season"]/option'):
        season.click()
        k += 1
    
        time.sleep(15)
    
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tbl = soup.find('tbody').find_all('tr')
        tbl[0].find_all('td')

        d = {}
        for row in tbl:
            items = row.find_all('td')
            team = items[1].text.replace('*', '') + ' ' + str(year)
            d[team] = [j.text for j in items[2:]]
            df = pd.DataFrame.from_dict(d, orient='index')
        df_main = pd.concat([df_main, df])
        if k > how_many_seasons:
            break
        year -= 1
    
    driver.close()
    driver.quit()
        
    df_main.columns = [j.text for j in soup.find('thead').find_all('th')][2:(2+df_main.shape[1])]
    df_main.index = [teamyr.replace('LA Clippers', 'Los Angeles Clippers') for teamyr in df_main.index]
    
    return df_main

def scrape_nbacom_tmclutch_by_url(start, end, url):
    '''Scrape team clutch statistics from NBA.com over a range of seasons (in reverse order) given:
    start, the end year of the first season in the range
    end, the end year of the last season in the range
    url, the url of the page with the team clutch stats to be scraped
    
    Output:
    df_main, a dataframe combining all team clutch stats for the entire range of seasons
    '''
    df_main = scrape_nbacom_by_url(start, end, url)
    df_main.columns.values[0:df_main.shape[1]] = 'Clutch' + df_main.columns.values[0:df_main.shape[1]]
    
    return df_main