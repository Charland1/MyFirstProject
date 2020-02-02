# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:38:21 2020

@author: czhang
"""

from BBGScraper import BBGScraper

import datetime 
import pandas as pd


startDate = '20171031'
endDate = datetime.date.today().strftime('%Y%m%d')
test_tickers = ['SPX Index','UKX Index', 'SX5E Index']


def get_data(startDate,endDate,tickers):

    # Initialize class
    bbg = BBGScraper(startDate, endDate)
    
    # Scrape Tickers
    bbg.scrape_tickers_Best_PE(tickers)

    return bbg.df


df1 = get_data(startDate,endDate,test_tickers)
print (df1)

