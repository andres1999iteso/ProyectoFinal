import pandas as pd
import functions as fn

indicador = pd.read_csv('./files/Gross Domestic Product Annualized.csv')

USDMXN = fn.descarga_data(["USDMXN"])['USDMXN']

USDMXN_train = USDMXN[(USDMXN['time'] >= '2020-01-01') & (USDMXN['time'] <='2021-01-01')]

USDMXN_test = USDMXN[(USDMXN['time'] >= '2021-02-01') & (USDMXN['time'] <='2022-02-01')]

EURUSD = fn. descarga_data(["EURUSD"])["EURUSD"]

EURUSD_train = EURUSD[(EURUSD['time'] >= '2020-01-01') & (EURUSD['time'] <='2021-01-01')]

EURUSD_test = EURUSD[(EURUSD['time'] >= '2021-02-01') & (EURUSD['time'] <='2022-02-01')] 

capital_inicial = 100000
max_perdida_cap = 1000
capital_acumulado_ent = []
capital_actual = capital_inicial

for i in range(len(USDMXN_train)):
    precio_actual_USDMXN = USDMXN_train.iloc[i]['close']
    precio_anterior_USDMXN = USDMXN_train.iloc[i-1]['close']
    cambio_precio_USDMXN = precio_actual_USDMXN - precio_anterior_USDMXN

    precio_actual_EURUSD = EURUSD_train.iloc[i]['close']
    precio_anterior_EURUSDN = EURUSD_train.iloc[i-1]['close']
    cambio_precio_EURUSD = precio_actual_EURUSD - precio_anterior_EURUSDN

    # Calculo de capital actualizado
    cambio_capital = cambio_precio_USDMXN + cambio_precio_EURUSD
    capital_actual += cambio_capital

    #ajuste si excede el limite de perdida max

    if cambio_capital<0:
        capital_actual = max(capital_actual, capital_actual - max_perdida_cap)
        capital_acumulado_ent.append(capital_actual)
capital_acumulado_prueba = []
capital_actual = capital_inicial 

for i in range(len(USDMXN_test)):
    precio_actual_USDMXN = USDMXN_test.iloc[i]['close']
    precio_anterior_USDMXN = USDMXN_train.iloc[i-1]['close']
    cambio_precio_USDMXN = precio_actual_USDMXN - precio_anterior_USDMXN

#calculo de capital acumulado periodo prueba
for i in range(len(USDMXN_test)):

    
    #calculo diferencias absolutas
    dif_absolutas = abs(capital_acumulado_ent - capital_acumulado_ent)
