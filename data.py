import pandas as pd
import functions as fn

#USDMXN = fn.descarga_data(["USDMXN"])['USDMXN']

#USDMXN_train = USDMXN[(USDMXN['time'] >= '2020-01-01') & (USDMXN['time'] <='2021-01-01')]

#USDMXN_test = USDMXN[(USDMXN['time'] >= '2021-02-01') & (USDMXN['time'] <='2022-02-01')]

#EURUSD = fn. descarga_data(["EURUSD"])["EURUSD"]

#EURUSD_train = EURUSD[(EURUSD['time'] >= '2020-01-01') & (EURUSD['time'] <='2021-01-01')]

#EURUSD_test = EURUSD[(EURUSD['time'] >= '2021-02-01') & (EURUSD['time'] <='2022-02-01')]

#indicador = pd.read_csv('./files/Gross Domestic Product Annualized.csv')


USDMXN = pd.read_csv('./files/USDMXN.csv')

USDMXN_train = pd.read_csv('./files/USDMXN_train.csv')

USDMXN_test = pd.read_csv('./files/USDMXN_test.csv')

EURUSD = pd.read_csv('./files/EURUSD.csv')

EURUSD_train = pd.read_csv('./files/EURUSD_train.csv')

EURUSD_test = pd.read_csv('./files/EURUSD_test.csv')

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

#calculo de capital acumulado periodo prueba
for i in range(len(USDMXN_test)):
    precio_actual_USDMXN = USDMXN_test.iloc[i]['close']
    precio_anterior_USDMXN = USDMXN_train.iloc[i-1]['close']
    cambio_precio_USDMXN = precio_actual_USDMXN - precio_anterior_USDMXN

    precio_actual_EURUSD = EURUSD_test.iloc[i]['close']
    precio_anterior_EURUSDN = EURUSD_test.iloc[i-1]['close']
    cambio_precio_EURUSD = precio_actual_EURUSD - precio_anterior_EURUSDN
    
    # Calculo de capital actualizado
    cambio_capital = cambio_precio_USDMXN + cambio_precio_EURUSD
    capital_actual += cambio_capital

    #ajuste si excede el limite de perdida max

    if cambio_capital<0:
        capital_actual = max(capital_actual, capital_actual - max_perdida_cap)
        capital_acumulado_prueba.append(capital_actual)

#calculo diferencias absolutas
dif_absolutas = abs(capital_acumulado_ent - capital_acumulado_ent)

# MAD 
mad1 = dif_absolutas.mean()
mad2 = dif_absolutas.median()
mad3 = dif_absolutas.mad()
tabla = pd.DataFrame({'MAD1':[mad1],'MAD2':[mad2],'MAD3':[mad3]})
print(tabla)

