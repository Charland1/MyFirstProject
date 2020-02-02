# -*- coding: utf-8 -*-
"""

@author: czhang
"""

from __future__ import division
import pandas as pd
import statsmodels.api as sm

'''import raw date file'''
Input = pd.read_excel(r'N:\Fixed Income Team\CTA Exposure Positioning\CTA exposure_new.xlsx',parse_dates = True, index_col = 0)

output_folder = r'N:\Fixed Income Team\CTA Exposure Positioning\Beta Output\%s.csv'

    
'''main regression function'''
def reg(index_file, file_name_str, window_size):

    
    '''create a copy of the input file'''
    df_clean = Input.copy(deep=True)
    
    df_clean_colname = pd.DataFrame(df_clean).iloc[1].tolist()
    
    col_name_lst = [str(n) for n in df_clean_colname]
    df_clean.columns = col_name_lst
     
       
    df_clean = df_clean[5:]
    


    
    '''get risk free rates, and convert rf rates to daily rates'''
    df_rf = df_clean.iloc[:,-1][1:]/252
    
    '''remove non-numeric rows for later processing'''
    df_clean = df_clean.iloc[:,0:6]
    
    '''calculate daily returns for each index, and drop N/A '''
    df_clean = df_clean.pct_change().dropna()
    
    '''calculate excess returns over risk free rate'''
    for i in df_clean.columns:
        
        df_clean[i] = df_clean[i] - df_rf

    '''set response varaible using the SG CTA Index'''
    df_Y = df_clean[["CTA Index"]]

    '''set explanatory varaibles'''
    df_X = df_clean[["10Y US","EX US Bond","SPX Index","Commodity Index","Tbill Index"]]
    
    count = 0
    result_country = pd.DataFrame(columns = ['time', 'const', "10Y US","EX US Bond","SPX Index","Commodity Index","Tbill Index", 'R_sq'])
    
    list_of_index = df_clean.index.tolist()

    
    for i in range(window_size,len(df_clean)):
        
        window_X = df_X[(i-window_size) : i]
        window_X = sm.add_constant(window_X)
        window_Y = df_Y[(i-window_size) : i] 
        
        '''run OLS regression on all asset calss indices variables against CTA index'''
        window_results = sm.OLS(window_Y.astype(float),window_X.astype(float)).fit()
#        print (window_results.summary())
        
        '''get regression parameters'''
        country_coef = window_results.params
        print (country_coef)
        
        country_coef = country_coef.to_frame().T
        
        '''get regression RSQ'''
        country_R_2 = window_results.rsquared
        
        '''put regression results in an array in each interation'''
        result_country.loc[i] = [list_of_index[i], country_coef.iat[0,0], country_coef.iat[0,1], country_coef.iat[0,2], country_coef.iat[0,3], country_coef.iat[0,4],country_coef.iat[0,5], country_R_2]
        count = count + 1

    
    result_final_country = result_country.set_index('time')
    result_final_country.to_csv(output_folder % file_name_str)
        
    return result_final_country
#    

    
#    
'''run main function'''
reg(Input,'output_excel_30_new_3Y',30)    
        