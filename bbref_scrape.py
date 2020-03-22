from bs4 import BeautifulSoup, Comment
import requests
import re
import pandas as pd

def tbl_scrape_from_bbref_seasonsumm(tbl_string, year):
    '''scrapes a table from a Basketball-Reference season summary page specified by:
    tbl_string, the string id for the specific table to scrape off the page
    year, for the end year of a specific season
    
    output:
    df, a dataframe corresponding to the table from the season summary page
    '''
    
    # scrape the season summary page
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    soup = get_soup(url)
    
    tbl = soup.find('table', {'id': tbl_string})
    
    # collect each table row (corresponding to team) into a dict then convert dict to dataframe
    d = {}
    rows=[row for row in tbl.find_all('tr')]
    for row in rows[:-1]:
        items = row.find_all('td')
        if len(items) > 0:
            team = items[0].text.replace('*', '') + ' ' + str(year)
            d[team] = [j.text.strip() for j in items[1:]]
    df = pd.DataFrame.from_dict(d, orient='index')
    
    df.columns = make_tbl_cols(rows, tbl_string)
    
    return df
    
    

def make_tbl_cols(rows, tbl_string):
    '''renames columns for dataframe of scraped Basketball-Reference season summary table specified by:
    rows, the Beautiful Soup-parsed list of table rows which includes the row of column names
    tbl_string, the string id for the specific table that was scraped
    
    output:
    df, a dataframe corresponding to the table from the season summary page with new column names
    '''
    
    # Set of if/else statements to deal with curiosities of each table (cleaning dataframe column names)
    # Tables with the string 'shooting' and 'misc' have multilevel grouped columns to address
    # Any table with the string 'opp' (for opponents) needs 'opp' appended to each column
    if tbl_string.find('shooting') != -1:
        columns = [k.text for k in rows[2].find_all('th')][2:]
        columns = [col + 'r' if i in range(4,10) else col for i, col in enumerate(columns)] 
        columns = [col + 'p' if i in range(10,16) else col for i, col in enumerate(columns)]
        columns[16] = '2P' + columns[16]
        columns = ['Dunk' + col if i in range(17,19) else col for i, col in enumerate(columns)]
        columns = ['Layup' + col if i in range(19,21) else col for i, col in enumerate(columns)]
        columns[21] = '3P' + columns[21]
        columns = ['Corner' + col if i in range(22,24) else col for i, col in enumerate(columns)]
        columns = ['Heave' + col if i in range(24,26) else col for i, col in enumerate(columns)]
    elif tbl_string.find('misc') != -1:
        columns = [k.text for k in rows[1].find_all('th')][2:]
        columns = ['O' + col if i in [15,16,18] else col for i, col in enumerate(columns)]
        columns = ['D' + col if i in [19,20,22] else col for i, col in enumerate(columns)]
    else:
        columns = [k.text for k in rows[0].find_all('th')][2:]
    return columns

def get_soup(url):
    '''
    Parses page located at specified url into a "soup" of html content readable in python
    
    Given:
        url, string of webpage location
    Returns:
        the "soup" (python-compatible objects) of the html parsed webpage content collected and read thru
        requests
    '''
                       
    response = requests.get(url)
    page = response.text
    return BeautifulSoup(re.sub('<!--|-->', '', page), 'html5lib')