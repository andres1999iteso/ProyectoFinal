import pytz
from datetime import datetime 
import pandas as pd
import MetaTrader5 as mt5
import numpy as np

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
    rsi = rsi.dropna()
    rsi = rsi.reset_index(drop=True)
    
    return rsi

#%% Funcion optimizacion 
    
def evaluar_parametros(parametros):
    nivel_entrada, stop_loss, nivel_salida = parametros

    # Inicializar variables y listas para el cálculo del rendimiento
    posicion_abierta = False
    capital_actual = capital_inicial
    cantidad_posicion = 0
    precio_apertura = 0
    precio_cierre = 0
    capital_acumulado = []

    # Obtener el número mínimo de elementos en los datos históricos
    min_length = min(len(USDMXN_train), len(EURUSD_train), len(rsi), len(indicador), len(capital_acumulado_prueba))

    # Iterar sobre los datos históricos y realizar las operaciones
    for i in range(min_length):
        # Obtener los precios y datos relevantes para el cálculo
        precio_actual_USDMXN = USDMXN_train.iloc[i]['close']
        precio_anterior_USDMXN = USDMXN_train.iloc[i-1]['close']
        cambio_precio_USDMXN = precio_actual_USDMXN - precio_anterior_USDMXN

        precio_actual_EURUSD = EURUSD_train.iloc[i]['close']
        precio_anterior_EURUSDN = EURUSD_train.iloc[i-1]['close']
        cambio_precio_EURUSD = precio_actual_EURUSD - precio_anterior_EURUSDN


        # Realizar la lógica de entrada y salida basada en los parámetros
        if rsi[i] > nivel_entrada and not posicion_abierta and indicador.iloc[i]['actual'] > 0:
            # Generar señal de compra
            precio_apertura = precio_actual_USDMXN  
            cantidad_posicion = (capital_actual * max_perdida_cap) / precio_apertura
            capital_actual -= cantidad_posicion * precio_apertura
            posicion_abierta = True
        elif rsi[i] < nivel_salida and posicion_abierta and indicador.iloc[i]['actual'] < 0:
            # Generar señal de venta
            precio_cierre = precio_actual_USDMXN  
            capital_actual += cantidad_posicion * precio_cierre
            posicion_abierta = False

        # Verificar si se alcanzó la pérdida máxima permitida
        if posicion_abierta and (precio_cierre - precio_actual_USDMXN) < -max_perdida_cap:
            # Cierre de posición por pérdida máxima alcanzada
            capital_actual += cantidad_posicion * precio_actual_USDMXN
            posicion_abierta = False

        # Agregar el capital acumulado a la lista
        capital_acumulado.append(capital_actual)

    # Calcular la diferencia absoluta entre el capital acumulado en el período de entrenamiento y prueba
    dif_absolutas = abs(np.array(capital_acumulado) - np.array(capital_acumulado_prueba[:min_length]))

    # Calcular la métrica de rendimiento (por ejemplo, MAD)
    rendimiento = dif_absolutas.mean()

    return rendimiento

def algoritmo_genetico(tamaño_poblacion, num_generaciones, probabilidad_cruce, probabilidad_mutacion, rango_entrada, rango_stop_loss, rango_salida):
    ## Parámetros del algoritmo genético
    #tamaño_poblacion = 20
    #num_generaciones = 50
    #probabilidad_cruce = 0.8
    #probabilidad_mutacion = 0.2
    
    # Rango de valores para cada parámetro
    #rango_entrada = (1, 30)
    #rango_stop_loss = (1, 1000)
    #rango_salida = (31, 70)
    
    # Espacio de búsqueda total
    espacio_busqueda = (rango_entrada[1] - rango_entrada[0] + 1) * (rango_stop_loss[1] - rango_stop_loss[0] + 1) * (rango_salida[1] - rango_salida[0] + 1)
    
    # Generación aleatoria de la población inicial
    poblacion = []
    for _ in range(tamaño_poblacion):
        entrada = random.randint(rango_entrada[0], rango_entrada[1])
        stop_loss = random.randint(rango_stop_loss[0], rango_stop_loss[1])
        salida = random.randint(rango_salida[0], rango_salida[1])
        individuo = [entrada, stop_loss, salida]
        poblacion.append(individuo)
    
    # Algoritmo genético
    mejor_fitness = float('inf')
    mejores_parametros = None
    mejor_fitness_historico = []
    mejor_entrada_historico = []
    mejor_stop_loss_historico = []
    mejor_salida_historico = []
    
    for generacion in range(num_generaciones):
        # Evaluación de la población actual
        fitness_poblacion = [evaluar_parametros(individuo) for individuo in poblacion]
    
        # Actualización del mejor individuo y su fitness
        mejor_individuo_idx = np.argmin(fitness_poblacion)
        mejor_fitness_actual = fitness_poblacion[mejor_individuo_idx]
        mejor_individuo_actual = poblacion[mejor_individuo_idx]
    
        # Verificación si se encontró un nuevo mejor individuo
        if mejor_fitness_actual < mejor_fitness:
            mejor_fitness = mejor_fitness_actual
            mejores_parametros = mejor_individuo_actual
    
        # Almacenar los resultados de la mejor configuración en cada generación
        mejor_fitness_historico.append(mejor_fitness)
        mejor_entrada_historico.append(mejores_parametros[0])
        mejor_stop_loss_historico.append(mejores_parametros[1])
        mejor_salida_historico.append(mejores_parametros[2])
    
        # Selección de padres mediante torneo binario
        padres = []
        for _ in range(tamaño_poblacion):
            padre1 = random.choice(poblacion)
            padre2 = random.choice(poblacion)
            if fitness_poblacion[poblacion.index(padre1)] < fitness_poblacion[poblacion.index(padre2)]:
                padres.append(padre1)
            else:
                padres.append(padre2)
    
        # Creación de la nueva generación mediante cruces y mutaciones
        nueva_generacion = []
        for _ in range(tamaño_poblacion):
            padre1 = random.choice(padres)
            padre2 = random.choice(padres)
    
            # Operador de cruce: punto de cruce aleatorio
            punto_cruce = random.randint(1, 2)
            hijo = padre1[:punto_cruce] + padre2[punto_cruce:]
    
            # Operador de mutación: mutación aleatoria en un gen
            if random.random() < probabilidad_mutacion:
                gen_mutado = random.randint(0, 2)
                 
                if gen_mutado == 0:
                    hijo[gen_mutado] = random.randint(rango_entrada[0], rango_entrada[1])
                elif gen_mutado == 1:
                    hijo[gen_mutado] = random.randint(rango_stop_loss[0], rango_stop_loss[1])
                else:
                    hijo[gen_mutado] = random.randint(rango_salida[0], rango_salida[1])
    
            nueva_generacion.append(hijo)
    
        # Reemplazo de la población anterior con la nueva generación
        poblacion = nueva_generacion
    

    
    # Gráfica de los resultados
    plt.figure(figsize=(10, 6))
    plt.plot(range(num_generaciones), mejor_entrada_historico, label='Nivel de entrada')
    plt.plot(range(num_generaciones), mejor_stop_loss_historico, label='Stop Loss')
    plt.plot(range(num_generaciones), mejor_salida_historico, label='Nivel de salida')
    plt.xlabel('Número de iteración')
    plt.ylabel('Valor del parámetro')
    plt.title('Optimización de parámetros')
    plt.legend()
    plt.show()