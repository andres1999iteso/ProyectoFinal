import pytz
from datetime import datetime 
import pandas as pd
import MetaTrader5 as mt5

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
       
    mt5.shutdown()
    
    return final

#def calcular_capital_acumulado(datos_precios):
import pandas as pd

def cal_rsi(data, window=14):
    delta = data.diff(1)
    delta.dropna(inplace=True)

    positive = delta.copy()
    negative = delta.copy()

    positive[positive < 0] = 0
    negative[negative > 0] = 0

    average_gain = positive.rolling(window=window).mean()
    average_loss = abs(negative.rolling(window=window).mean())

    relative_strength = average_gain / average_loss
    rsi = 100 - (100 / (1 + relative_strength))
    return rsi