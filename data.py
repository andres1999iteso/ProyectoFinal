import pandas as pd
import functions as fn

indicador = pd.read_csv('./files/Gross Domestic Product Annualized.csv')

USDMXN = fn.descarga_data(["USDMXN"])

EURUSD = fn. descarga_data(["EURUSD"]) 