from bs4 import BeautifulSoup, Comment
import requests
import re
import pandas as pd

def tbl_scrape_from_bbref_seasonsumm(tbl_string, year):
    '''scrapes a table from a Basketball-Reference season summary page specified by:
    tbl_string, for the specific table to scrape off the page
    year, for the end year of a specific season
    
    output:
    df, a dataframe corresponding to the table from the season summary page
    '''
    
    # scrape the season summary page
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(re.sub('<!--|-->', '', page), 'html5lib')
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
    
    # Set of if/else statements to deal with curiosities of each table (cleaning dataframe column names)
    # Tables with the string 'shooting' and 'misc' have multilevel grouped columns to address
    # Any table with the string 'opp' (for opponents) needs 'opp' appended to each column
    if tbl_string.find('shooting') != -1:
        df.columns = [k.text for k in rows[2].find_all('th')][2:]
        df.columns.values[4:10] = df.columns.values[4:10] + 'r'
        df.columns.values[10:16] = df.columns.values[10:16] + 'p' 
        df.columns.values[16] = '2P' + df.columns.values[16]
        df.columns.values[17:19] = 'Dunk' + df.columns.values[17:19]
        df.columns.values[19:21] = 'Layup' + df.columns.values[19:21]
        df.columns.values[21] = '3P' + df.columns.values[21]
        df.columns.values[22:24] = 'Corner' + df.columns.values[22:24]
        df.columns.values[24:26] = 'Heave' + df.columns.values[24:26]
    elif tbl_string.find('misc') != -1:
        df.columns = [k.text for k in rows[1].find_all('th')][2:]
        df.columns.values[[14,15,17]] = 'O' + df.columns.values[[14,15,17]]
        df.columns.values[[18,19,21]] = 'D' + df.columns.values[[18,19,21]]
    else:
        df.columns = [k.text for k in rows[0].find_all('th')][2:]
        if year == 2017 and tbl_string.find('opp') != -1:
            df.columns.values[[7,10]] = df.columns.values[[7,10]] + '%'
        
    if tbl_string.find('opp') != -1:
            df.columns.values[0:] = 'opp' + df.columns.values[0:]
    return df

def scrape_bbref_teampg_adv(url):
    '''Given a url, scrape advanced table from a given team season page
    Output: dataframe for player advanced stats for the team season
    '''
    response = requests.get(url)
    page = response.text    
    soup = BeautifulSoup(re.sub('<!--|-->', '', page), 'html5lib')
    
    tbl = soup.find('table', {'id': 'advanced'})
    
    thead = tbl.select('thead')
    tbody = tbl.select('tbody')
    
    df = pd.DataFrame()
    rows=[row for row in tbody[0].find_all('tr')]
    for row in rows:
        items = row.find_all('td')
        new_row = pd.Series([j.text.strip() for j in items])
        df = pd.concat([df, new_row], axis=1)
    return df.T.reset_index().drop('index', axis = 1)

def collect_bbref_team_page_urls():
    '''Collect all franchise index urls for each current NBA team from the front page
    Output: a list of urls
    '''
    root = 'https://www.basketball-reference.com'
    response = requests.get(root)
    page = response.text
    
    soup = BeautifulSoup(re.sub('<!--|-->', '', page), 'html5lib')
    team_pg_td = soup.find_all('td', {'data-stat': 'franchise_text'})
    
    rel_paths = [b['href'] for b in list(filter(None.__ne__, [k.find('a') for k in team_pg_td]))]
    
    return [root + j for j in rel_paths]

def get_all_teampg_urls(url, start, end):
    '''Collect all individual team season pages within a range of seasons given:
    url, the franchise index url
    start, the end year of the first season in the range
    end, the end year of last season in the range
    
    Output:
    urls, a list of urls for each team season page in the specified range
    '''
    
    root = 'https://www.basketball-reference.com'
    
    response = requests.get(url)
    page = response.text
    
    soup = BeautifulSoup(re.sub('<!--|-->', '', page), 'html5lib')
    
    what_seasons = soup.find_all('tr')
    seasons_endYr = [int(season.find('a').get('href').split('/')[3].split('.')[0]) for season in what_seasons[1:]]
    #print(seasons_endYr)
    
    what_rows = soup.find('tbody').find_all('tr')
    urls = []
    
    idx = 0
    year = end
    
    while year > start and idx < len(what_rows):
        tmp_url = what_rows[idx].find('a').get('href')
        urls.append(root + tmp_url)
        idx += 1
        year = int(what_seasons[idx].find('a').get('href').split('/')[3].split('.')[0])
    return urls