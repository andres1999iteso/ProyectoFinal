import pytz
from datetime import datetime 
import pandas as pd
import MetaTrader5 as mt5

indicador = pd.read_csv('./files/Gross Domestic Product Annualized.csv')

def descarga_data(tickers):

    mt5.initialize()
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime(2022,6,1,tzinfo=timezone)
    final = {}
    
    for i in tickers:
        
        data=(mt5.copy_rates_from(i,mt5.TIMEFRAME_M15,utc_from,85000))
        
        data=pd.DataFrame(data)
        
        data['time'] = pd.to_datetime(data['time'], unit='s')
        
        data = data[(data['time'] >= '2020-01-01') &  (data['time'] <='2022-02-01')]
        
        final[i]=data
        
        final[i].to_csv('files/'+i+'.csv')
        
    mt5.shutdown()
    
    return final


g=descarga_data(["USDMXN"])


f=descarga_data(["EURUSD"])