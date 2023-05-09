
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

dict_test = {'key_a': 'a', 'key_b': 'b'}

import datetime
import pytz
from datetime import datime 
import pandas as pd
import MetaTrader5 as mt5

indice = pd.read_csv(r'/Users/gabrielaortiz/Documents/ITESO/Micro y sistemas de traiding/ProyectoFinal/files/Gross Domestic Product Annualized.csv')

def f_import_mt5(list_tickers):
    mt5.initialize()
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2020,1,1,tzinfo=timezone)
    utc_to = datetime(2022,2,1,tzinfo=timezone)
    mt5_rates = {}
    for i in list_tickers:
        rates=(mt5.copy_rates_from(i,mt5.TIMEFRAME_M15,utc_from,85000,utc_to))
        rates=pd.DataFrame(rates)
        rates['time'] = pd.to_datetime(rates['time'], unit='s')
        #rates.to_csv('')
        mt5_rates[i]=rates
        mt5_rates[i].to_csv('files/'+i+'.csv')
    mt5.shutdown()
    return mt5_rates

list_tickers = ['USDMXN','USDEUR']
historico = f_import_mt5(list_tickers)
usdmxn_prices = historical_data['USDMXN']
usdeur_prices = historical_data['USDEUR']

print(indice.head())
print(usdmxn_prices.head())
print(usdeur_prices.head())
