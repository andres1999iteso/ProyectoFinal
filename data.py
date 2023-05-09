import pandas as pd
import functions as fn

indicador = pd.read_csv('./files/Gross Domestic Product Annualized.csv')

USDMXN = fn.descarga_data(["USDMXN"])['USDMXN']

USDMXN_train = USDMXN[(USDMXN['time'] >= '2020-01-01') & (USDMXN['time'] <='2021-01-01')]

USDMXN_test = USDMXN[(USDMXN['time'] >= '2021-02-01') & (USDMXN['time'] <='2022-02-01')]

EURUSD = fn. descarga_data(["EURUSD"])["EURUSD"]

EURUSD_train = EURUSD[(EURUSD['time'] >= '2020-01-01') & (EURUSD['time'] <='2021-01-01')]

EURUSD_test = EURUSD[(EURUSD['time'] >= '2021-02-01') & (EURUSD['time'] <='2022-02-01')] 
