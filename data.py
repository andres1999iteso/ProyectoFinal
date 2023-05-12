import pandas as pd
import functions as fn
import numpy as np

#USDMXN = fn.descarga_data(["USDMXN"])['USDMXN']

#USDMXN_train = USDMXN[(USDMXN['time'] >= '2020-01-01') & (USDMXN['time'] <='2021-01-01')]

#USDMXN_test = USDMXN[(USDMXN['time'] >= '2021-02-01') & (USDMXN['time'] <='2022-02-01')]

#EURUSD = fn. descarga_data(["EURUSD"])["EURUSD"]

#EURUSD_train = EURUSD[(EURUSD['time'] >= '2020-01-01') & (EURUSD['time'] <='2021-01-01')]

#EURUSD_test = EURUSD[(EURUSD['time'] >= '2021-02-01') & (EURUSD['time'] <='2022-02-01')]

indicador = pd.read_csv('./files/Gross Domestic Product Annualized.csv')

USDMXN = pd.read_csv('./files/USDMXN.csv')

USDMXN_train = pd.read_csv('./files/USDMXN_train.csv')

USDMXN_test = pd.read_csv('./files/USDMXN_test.csv')

EURUSD = pd.read_csv('./files/EURUSD.csv')

EURUSD_train = pd.read_csv('./files/EURUSD_train.csv')

EURUSD_test = pd.read_csv('./files/EURUSD_test.csv')

print(len(USDMXN_train))
print(len(EURUSD_train))
print(len(USDMXN_test))
print(len(EURUSD_test))

capital_inicial = 100000
max_perdida_cap = 1000
capital_acumulado_ent = []
capital_actual = capital_inicial

min_length = min(len(USDMXN_train), len(EURUSD_train), len(USDMXN_test), len(EURUSD_test))

capital_acumulado_ent = []
capital_actual = capital_inicial

# Calcular de capital acumulado periodo entrenamiento
for i in range(min_length):
    precio_actual_USDMXN = USDMXN_train.iloc[i]['close']
    precio_anterior_USDMXN = USDMXN_train.iloc[i-1]['close']
    cambio_precio_USDMXN = precio_actual_USDMXN - precio_anterior_USDMXN

    precio_actual_EURUSD = EURUSD_train.iloc[i]['close']
    precio_anterior_EURUSDN = EURUSD_train.iloc[i-1]['close']
    cambio_precio_EURUSD = precio_actual_EURUSD - precio_anterior_EURUSDN

    # Calculo de capital actualizado
    cambio_capital = cambio_precio_USDMXN + cambio_precio_EURUSD
    capital_actual += cambio_capital

    # Ajuste si excede el limite de perdida max
    if cambio_capital < 0:
        capital_actual = max(capital_actual, capital_actual - max_perdida_cap)
    capital_acumulado_ent.append(capital_actual)

capital_acumulado_prueba = []
capital_actual = capital_inicial

# Calculo de capital acumulado periodo prueba
for i in range(min_length):
    precio_actual_USDMXN = USDMXN_test.iloc[i]['close']
    precio_anterior_USDMXN = USDMXN_test.iloc[i-1]['close']
    cambio_precio_USDMXN = precio_actual_USDMXN - precio_anterior_USDMXN

    precio_actual_EURUSD = EURUSD_test.iloc[i]['close']
    precio_anterior_EURUSDN = EURUSD_test.iloc[i-1]['close']
    cambio_precio_EURUSD = precio_actual_EURUSD - precio_anterior_EURUSDN

    # Calculo de capital actualizado
    cambio_capital = cambio_precio_USDMXN + cambio_precio_EURUSD
    capital_actual += cambio_capital

    # Ajuste si excede el limite de perdida max
    if cambio_capital < 0:
        capital_actual = max(capital_actual, capital_actual - max_perdida_cap)
    capital_acumulado_prueba.append(capital_actual)

# Calculo diferencias absolutas
dif_absolutas = abs(np.array(capital_acumulado_ent[:min_length]) - np.array(capital_acumulado_prueba[:min_length]))

# MAD 
mad1 = dif_absolutas.mean()
mad2 = np.median(dif_absolutas)
mad3 = np.mean(np.abs(dif_absolutas - np.mean(dif_absolutas)))
tabla = pd.DataFrame({'MAD1': [mad1], 'MAD2': [mad2], 'MAD3': [mad3]})
print(tabla)

#Generación de señal de compra o de venta.
import pandas as pd
import numpy as np

# Define las variables y carga los datos

capital_inicial = 100000
max_perdida_cap = 1000
nivel_entrada = 30
nivel_salida = 70

rsi = cal_rsi(USDMXN_train['close'])  # Correr primero functions
indicador = pd.read_csv('./files/Gross Domestic Product Annualized.csv')  

min_length = min(len(USDMXN_train), len(EURUSD_train), len(USDMXN_test), len(EURUSD_test), len(indicador))
rsi = rsi[:min_length]
indicador = indicador[:min_length]

posicion_abierta = False
capital_actual = capital_inicial
cantidad_posicion = 0
precio_apertura = 0
precio_cierre = 0
capital_acumulado = []
operaciones = []

# Itera sobre los datos y realiza las operaciones

for i in range(len(rsi)):
    if rsi[i] > nivel_entrada and not posicion_abierta and indicador.iloc[i]['Gross Domestic Product Annualized'] > 0:
        # Generar señal de compra
        precio_apertura = precio_actual_USDMXN  
        cantidad_posicion = (capital_actual * max_perdida_cap) // precio_apertura
        capital_actual -= cantidad_posicion * precio_apertura
        posicion_abierta = True
        operaciones.append('Compra')

    elif rsi[i] < nivel_salida and posicion_abierta and indicador.iloc[i]['Gross Domestic Product Annualized'] < 0:
        # Generar señal de venta
        precio_cierre = precio_actual_USDMXN  
        capital_actual += cantidad_posicion * precio_cierre
        posicion_abierta = False
        operaciones.append('Venta')

    if posicion_abierta and (precio_cierre - precio_actual_USDMXN) < -max_perdida_cap:
        # Cierre de posición por pérdida máxima alcanzada
        capital_actual += cantidad_posicion * precio_actual_USDMXN
        posicion_abierta = False
        operaciones.append('Venta')

    capital_acumulado.append(capital_actual)

rendimiento_acumulado = capital_actual - capital_inicial
rendimiento_promedio = rendimiento_acumulado / len(rsi)

# Imprime la tabla de resultados

tabla_rsi = pd.DataFrame({'Capital Acumulado': capital_acumulado, 'Operación': operaciones})
print(tabla_rsi)
