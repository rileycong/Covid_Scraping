from bs4 import BeautifulSoup
import requests
import pandas as pd


# link to the web
source = requests.get('https://www.worldometers.info/coronavirus/').text
soup = BeautifulSoup(source, 'lxml')

## The Scrape Begins ##

# Pick the table we want to scrape using id
covid_table = soup.find("table", attrs={"id": "main_table_countries_today"})

# The header's html
head = covid_table.thead.find_all('tr')

# Extract text headers from html to create list
headings = []
for th in head[0].find_all('th'):
    headings.append(th.text.replace('\n','').strip())   # remove any newlines and extra spaces from left and right

# The body's html
body = covid_table.tbody.find_all('tr')

# Append the values of rows to create list
data = []   # A list that hold all rows
for a in range(1, len(body)):
    row = []
    for td in body[a].find_all('td'):
        row.append(td.text.replace('\n','').strip())
    data.append(row)

# data contains all the rows excluding header
# row contains data for one row

# Pass data into a pandas dataframe with headings as the columns
df = pd.DataFrame(data,columns=headings)

data = df[df['#']!=''].reset_index(drop=True)
# Data points with # value are the countries of the world while the data points with
# null values for # columns are features like continents totals etc

data = data.drop_duplicates(subset = ["Country,Other"])
# Reason to drop duplicates : Worldometer reports data for 3 days: today and 2 days back
# Removing duplicates removes the values for the past two days and keep today's

# Drop the following columns
cols = ['#',
            'Tot\xa0Cases/1M pop',
            'Deaths/1M pop',
            'TotalTests',
            'Tests/1M pop',
            '1 Caseevery X ppl',
            '1 Deathevery X ppl',
            '1 Testevery X ppl',
            'New Cases/1M pop',
            'New Deaths/1M pop',
            'Active Cases/1M pop']

# Data full has all needed informations
data_full = data.drop(cols, axis=1)

# Select specific columns from data_full
def Select():
    cases = data_full[['TotalCases','ActiveCases','NewCases','Serious,Critical']]

    deaths = data_full[['TotalDeaths','NewDeaths']]

    recovered = data_full[['TotalRecovered','NewRecovered']]

    population = data_full['Population']

    return cases, deaths, recovered, population