# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 12:55:17 2019

@author: czhang
"""


from BBGScraper import BBGScraper

import datetime 
import pandas as pd
import statsmodels.api as sm
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt

import matplotlib.gridspec as gridspec
import timeit 

start = timeit.default_timer()

register_matplotlib_converters()
#######################################################################
'''
This model imports relevant raw data series from Bloomberg and apply multi-factor regression tecchnique 
to calculate rolling coefficent on each asset class indices. 

the start date, end date and relevant tickers, and produces a Pandas Dataframe
The function "run_data" consumes the index series and calculate rolling regression betas, and produces a 
dataframe that contains all the betas in time series format.
'''
#######################################################################
output_folder = r'N:\Fixed Income Team\CTA Exposure Positioning\Beta Output\%s.csv'

'''input variable infomration here'''
startDate = '20171031'
endDate = datetime.date.today().strftime('%Y%m%d')

#endDate = '20191107'
window_size = 30
file_name_str = 'output_excel_30_new_3Y_BBG_connector'
CTA_tickers = ['NEIXCTA Index','MLT1US10 Index','JHDC1R10 Index',
                   'SPX Index','SPGSCI Index','G0O1 Index', 'USGG3M Index']

macro_HF_tickers = ['HFRXM Index','MLT1US10 Index','JHDC1R10 Index',
                   'SPX Index','SPGSCI Index','G0O1 Index', 'USGG3M Index']

##############################################################################################################################################
'''function to retrive data from bloomberg'''


def get_data(startDate,endDate,tickers):

    # Initialize class
    bbg = BBGScraper(startDate, endDate)
    
    # Scrape Tickers
    bbg.scrape_tickers_px_last(tickers)

    return bbg.df


def run_data(startDate,endDate,CTA_tickers,window_size,file_name_str):
    
#    get raw dataframe
    raw_df = get_data(startDate,endDate,CTA_tickers)
    
#    creat a deep copy of the dataframe
    df_clean = raw_df.copy(deep=True)
    df_clean = df_clean.dropna()
    
    df_clean_colname = df_clean.columns
    
    col_name_lst = [str(n) for n in df_clean_colname]
    df_clean.columns = col_name_lst
    
#    use date as dataframe index
    df_clean = df_clean.set_index('date')
    
    '''get risk free rates, and convert rf rates to daily rates'''
    df_rf = df_clean.iloc[:,-1][:]/252    
    
    df_clean = df_clean.iloc[:,0:6]
    
    '''calculate daily returns for each index, and drop N/A '''
    df_clean = df_clean.pct_change().dropna()
    
    '''calculate excess returns over risk free rate'''
    for i in df_clean.columns:
        
        df_clean[i] = df_clean[i] - df_rf    
    
    '''set response varaible using the SG CTA Index'''
    df_Y = df_clean.iloc[:,0]

    '''set explanatory varaibles'''
    df_X = df_clean[['MLT1US10 Index','JHDC1R10 Index',
                   'SPX Index','SPGSCI Index','G0O1 Index']]
    
    count = 0
    
    '''set the result dataframe'''
    result_index = pd.DataFrame(columns = ['time', 'const', "10Y US","EX US Bond",
                                           "SPX Index","Commodity Index","Tbill Index", 'R_sq'])
    
    list_of_index = df_clean.index.tolist()

    for i in range(window_size,len(df_clean)):
        
        window_X = df_X[(i-window_size) : i]
        window_X = sm.add_constant(window_X)
        window_Y = df_Y[(i-window_size) : i] 
        
        '''run OLS regression on all asset calss indices variables against CTA index'''
        window_results = sm.OLS(window_Y.astype(float),window_X.astype(float)).fit()
        
        '''get regression parameters'''
        index_coef = window_results.params
#        print (index_coef)
        
        index_coef = index_coef.to_frame().T
        
        '''get regression RSQ'''
        index_R_2 = window_results.rsquared
        
        '''put regression results in an array in each interation'''
        result_index.loc[i] = [list_of_index[i], index_coef.iat[0,0], index_coef.iat[0,1], 
                         index_coef.iat[0,2], index_coef.iat[0,3], 
                         index_coef.iat[0,4],index_coef.iat[0,5], index_R_2]
        
        count = count + 1

    
    result_final_index = result_index.set_index('time')
    result_final_index.to_csv(output_folder % file_name_str)
    file_name = (output_folder % file_name_str)
        
    return result_final_index, file_name
    
file_name_CTA = run_data(startDate,endDate,CTA_tickers,window_size,file_name_str)[1]
#file_name_MacroHF = run_data(startDate,endDate,macro_HF_tickers,window_size,file_name_str)[1]

'''the following function charts the output regression coefficients'''
def chart_plot(file_name):

    df_result_file = pd.read_csv(file_name) 

    fig_1 = plt.figure(figsize=(16,10), constrained_layout=True)
    grid_1 = gridspec.GridSpec(ncols=2,nrows=5,figure=fig_1)
    
    time_temp = df_result_file['time']
    time = []
    
    '''convert data type to date'''
    for i in time_temp:
        i = datetime.datetime.strptime(i, "%Y-%m-%d").date()
        time.append(i)

     
    chart_1_1 = fig_1.add_subplot(grid_1[:2, 0])

    chart_1_2 = fig_1.add_subplot(grid_1[:2, 1])

    chart_1_3 = fig_1.add_subplot(grid_1[2:4, 0])

    chart_1_4 = fig_1.add_subplot(grid_1[2:4, 1])
    


    chart_1_1.plot(time, df_result_file['10Y US'], color='r')   
    chart_1_1.set_title('Exposure to 10Y US Treasury')
    chart_1_1.grid(axis='y', linestyle='-', linewidth=0.1, color='grey') 


    chart_1_2.plot(time, df_result_file['EX US Bond'], color='b')   
    chart_1_2.set_title('Exposure to ex. US Bond')
    chart_1_2.grid(axis='y', linestyle='-', linewidth=0.1, color='grey')       
        
    
    chart_1_3.plot(time, df_result_file['SPX Index'],color='olive')   
    chart_1_3.set_title('Exposure to S&P')
    chart_1_3.grid(axis='y', linestyle='-', linewidth=0.1, color='grey') 


    chart_1_4.plot(time, df_result_file['Commodity Index'], color='c')   
    chart_1_4.set_title('Exposure to commodity')
    chart_1_4.grid(axis='y', linestyle='-', linewidth=0.1, color='grey')                               


''''class ref'''    
if __name__ == '__main__':
    
#    data = get_data(startDate,endDate,CTA_tickers)    
#    data = run_data(startDate,endDate,CTA_tickers,window_size,file_name_str)
    chart_plot(file_name_CTA)
#    chart_plot(file_name_MacroHF)
 
    
stop = timeit.default_timer()
print('Time: ', stop - start)
    