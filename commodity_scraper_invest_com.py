# script to scrape commodity prices from investing.com on the hour and load
# into SQL server

import requests
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import urllib
from sqlalchemy import create_engine
import sys

# initiate a session necessary to pass in headers parameter and then return
# the sites html
session = requests.Session()

try:
    response = session.get('https://uk.investing.com/commodities/real-time-futures', headers={'User-Agent':'Mozilla/5.0'})
except:
    http_err = requests.exceptions.HTTPError
    print('HTTP error occured: {}'.format(http_err))

response_text = response.text

# use BeautifulSoup to return the html table id=cross_rate_1
soup = BeautifulSoup(response_text,'html.parser')
table = soup.find('table',id='cross_rate_1',)

# use urllib to pass a pyodbc connection string to a parameter
# pass the parameter to sqlalchemy engine
params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=DESKTOP-PVSJ3PE\MIKE_LOCAL;DATABASE=Commodity_Spot_Rates;Trusted_Connection=yes')
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

# initiate a pandas DataFrame
df = pd.DataFrame()

# create a function taking in a DataFrame object, removing any commas and converting
# them to a float
def clean_df(dfo):
    dfo = dfo.apply(lambda x: x.replace(',',''))
    dfo = dfo.apply(lambda x: float(x))
    return dfo

# initiate a loop
while 1:

# initiate an empty list and append all table cells
    td = []
    for tds in table.findAll('td'):
        td.append(tds.text)

# use list slicing to add data to the DataFrame
    df['commodity'] = td[1::10]
    df['month'] = td[2::10]
    df['last'] = td[3::10]
    df['high'] = td[4::10]
    df['low'] = td[5::10]

# clean and convert the float data using the clean_df function previously made
    df['last'] = clean_df(df['last'])
    df['high'] = clean_df(df['high'])
    df['low'] = clean_df(df['low'])

# grab the digits from the change column using slice and convert to float
    chg = []
    for items in td[6::10]:
        chg.append(float(items[slice(1,5)]))

# grab the digits from the change percentage column and convert to float
    chg_pct = []
    for items in td[7::10]:
        chg_pct.append(float(items[slice(0,4)]))

# add the change and change percentage columns to the DataFrame as well as the time
# column
    df['chg'] = chg
    df['chg_pct'] = chg_pct
    df['time'] = td[8::10]

# get current system time and format to ISO8601 format
# add current time to the DataFrame
    time_now = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    df['upload_date'] = time_now

# export data from DataFrame to sql server using the sqlalchemy engine and appending to table
# can truncate if necessary by changing if_exists parameter to truncate
    try:
        df.to_sql('invest_dot_com',engine,schema='dbo',if_exists='append',index=False)
    except:
        pd.errors
# create varuable dt which is set to the next hour
    dt = datetime.now() + timedelta(hours=1)

# pause code until next hour before repeating
    while datetime.now() < dt:
        time.sleep(1)
