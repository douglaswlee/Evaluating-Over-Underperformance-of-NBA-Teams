from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

def scrape_nbacom_tmclutch_by_url(start, end, url):
    '''Scrape team clutch statistics from NBA.com over a range of seasons given:
    start, the end year of the first season in the range
    end, the end year of the last season in the range
    url, the url of the page with the team clutch stats to be scraped
    
    Output:
    df, a dataframe combining all team clutch stats for the entire range of seasons
    '''

    driver = get_driver("/Applications/chromedriver")
    driver.get(url)
    df = scrape_table(driver, start, end)
    close_driver(driver)
    
    return df


def scrape_table(driver, start, end):
    '''Scrape table of given page of statistics given
    driver, the (Chrome) WebDriver being used to scrape
    start, the end year of the first season in the range
    end, the end year of the last season in the range
    
    Output:
    df_main, a dataframe combining all team clutch stats for the entire range of seasons
    '''
    
    df_main = pd.DataFrame()

    for year in range(start, end+1):
        start = str(year-1)
        end = str(year)[2:]
        time.sleep(2)
        xpath = './/option[@label="' + start + '-' + end + '"]'
        season = driver.find_element_by_xpath(xpath)
        season.click()
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tbl = soup.find('tbody').find_all('tr')

        d = {}
        for row in tbl:
            items = row.find_all('td')
            team = items[1].text.strip().replace('*', '') + ' ' + str(year)
            d[team] = [j.text for j in items[2:]]
        df = pd.DataFrame.from_dict(d, orient='index')
        df_main = pd.concat([df_main, df])
    tbl_cols = soup.find_all('th')
    df_main.columns = ['Clutch' + c.text.strip().replace('xa0', '') for c in tbl_cols][2:(2+df_main.shape[1])]
    df_main.index = [teamyr.replace('LA Clippers', 'Los Angeles Clippers') for teamyr in df_main.index]
    
    return df_main

def get_driver(chromedriver):
    '''
    Given
    chromedriver, the path to chromedriver
    
    Return
    driver, the (Chrome) WebDriver to be used to scrape
    '''    
    chromedriver = chromedriver
    driver = webdriver.Chrome(chromedriver)
    return driver

def close_driver(driver):
    '''
    Given
    driver, the (Chrome) WebDriver being used to scrape
    close and quit the driver
    '''
    
    driver.close()
    driver.quit()