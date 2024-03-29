#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 21:30:39 2023

@author: yousuf
"""
#installing libraries
!pip install yfinance
!pip install bs4

#importing libraries
import pandas as pd

import yfinance as yf
import requests
from bs4 import BeautifulSoup

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price ($)", "Historical Revenue ($)"), vertical_spacing = .5)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($ Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=1000, title=stock, xaxis_rangeslider_visible=True)
    fig.show()


# Using the Ticker function to create a ticker object.
# ticker symbol of tesla is TSLA
tesla_data = yf.Ticker('TSLA')

# history function helps to extract stock information.
# setting period parameter to max to get information for the maximum amount of time.
tsla_data = tesla_data.history(period='max')

# Resetting the index
tsla_data.reset_index(inplace=True)

# display the first five rows
tsla_data.head()


# using requests library to download the webpage
url='https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'

# Save the text of the response
html_text = requests.get(url).text

# Parse the html data using beautiful_soup.
soup=BeautifulSoup(html_text, 'html5lib')



# Using beautiful soup extract the table with Tesla Quarterly Revenue.
# creating new dataframe
tsla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

tables = soup.find_all('table')
table_index=0

for index, table in enumerate(tables):
    if ('Tesla Quarterly Revenue'in str(table)):
        table_index=index
        
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col!=[]):
        date =col[0].text
        # to remove comma and dollar sign
        revenue =col[1].text.replace("$", "").replace(",", "")
        tsla_revenue=tsla_revenue.append({'Date':date,'Revenue':revenue},
                                           ignore_index=True)

# displaying dataframe
tsla_revenue


# removing null values
tsla_revenue = tsla_revenue[tsla_revenue['Revenue']!='']
tsla_revenue


plot_graph(tsla_data, tsla_revenue, 'Tesla Historical Share Price & Revenue')


#  ticker symbol of GameStop is GME
gamestop = yf.Ticker('GME')

# extracting stock information
gme_data=gamestop.history(period='max')

#reset the index
gme_data.reset_index(inplace=True)
gme_data.head()


# using requests library to download the webpage
url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'

# Save the text of the response
html_data = requests.get(url).text

# parse the html data
soup=BeautifulSoup(html_data, 'html5lib')


# Using beautiful soup extract the table with GameStop Quarterly Revenue
# creating new dataframe
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
tables = soup.find_all('table')

table_index=0
for index, table in enumerate(tables):
    if ('GameStop Quarterly Revenue'in str(table)):
        table_index=index
        
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col!=[]):
        date =col[0].text
        # comma and dollar sign is removed
        revenue =col[1].text.replace("$", "").replace(",", "")
        gme_revenue=gme_revenue.append({'Date':date,'Revenue':revenue},
                                       ignore_index=True)
        
gme_revenue.head()


plot_graph(gme_data, gme_revenue, 'GameStop')