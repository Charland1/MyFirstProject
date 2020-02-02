# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:06:11 2019

@author: czhang
"""
'''code borrowed from Risk Analytics team, with some major modifications for the purposes of this analysis'''
import pdblp
import datetime
import requests
import pandas as pd
import sys

# connector to local bloomberg machine
class BBGScraper():
    

    def __init__(self, startDate='19850101', endDate=datetime.date.today().strftime('%Y%m%d')):

        self.startDate = startDate
        self.endDate = endDate

    def _connect(self):
        self.conn = pdblp.BCon(debug=True, port=8194, timeout=10000)
        self.conn.debug = False


    @staticmethod
    def _convert_issue_to_ticker(issue_name):
 
         if len(issue_name.split(' ')) == 2:
             ticker = issue_name.split(' ')[0]
         else:
             ticker = issue_name.split(' ')[0]
         for piece in issue_name.split(' ')[0:-1]:
             ticker = ticker + ' ' + piece
         
         return ticker


    def scrape_tickers_Best_PE(self, tickers):


        print('Scraping Date for Tickers below:')
        print(tickers)
#        print('-' * 40)
        print('For all dates available')
        print('From: {}'.format(self.startDate))
        print('To:   {}'.format(self.endDate))

        # Connect to Bloomberg
        self._connect()
        self.conn.start()

        # Scrape Ticker Data

        print('Searching ticker data...')
        df = self.conn.bdh(tickers, ['BEST_PE_RATIO'], str(self.startDate), str(self.endDate),
                           elms=[("periodicityAdjustment", "ACTUAL")])

        # Transform ticker data
        df = df.reset_index()
        df.columns = df.columns.droplevel(1)

        self.df = df

        print('Values Returned:  {}'.format(len(df)))

    def scrape_tickers_Best_EPS(self, tickers):


        print('Scraping Date for Tickers below:')
        print(tickers)
#        print('-' * 40)
        print('For all dates available')
        print('From: {}'.format(self.startDate))
        print('To:   {}'.format(self.endDate))

        # Connect to Bloomberg
        self._connect()
        self.conn.start()

        # Scrape Ticker Data

        print('Searching ticker data...')
        df = self.conn.bdh(tickers, ['BEST_EPS'], str(self.startDate), str(self.endDate),
                           elms=[("periodicityAdjustment", "ACTUAL")])

        # Transform ticker data
        df = df.reset_index()
        df.columns = df.columns.droplevel(1)

        self.df = df

        print('Values Returned:  {}'.format(len(df)))
     

    def scrape_tickers_px_last(self, tickers):


        print('Scraping Date for Tickers below:')
        print(tickers)
#        print('-' * 40)
        print('For all dates available')
        print('From: {}'.format(self.startDate))
        print('To:   {}'.format(self.endDate))

        # Connect to Bloomberg
        self._connect()
        self.conn.start()

        # Scrape Ticker Data

        print('Searching ticker data...')
        df = self.conn.bdh(tickers, ['PX_LAST'], str(self.startDate), str(self.endDate),
                           elms=[("periodicityAdjustment", "ACTUAL")])

        # Transform ticker data
        df = df.reset_index()
        df.columns = df.columns.droplevel(1)

        self.df = df

        print('Values Returned:  {}'.format(len(df)))

