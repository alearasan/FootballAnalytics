import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import datetime as dt

# # carga la base de datos de partidos anteriores
# partidos = pd.read_csv('../data/DatosPartidosLimpio(18-04-2023).csv')
#
# # seleccionar las columnas necesarias
# partidos = partidos['Corners']

# partidos['Fecha'] = pd.to_datetime(partidos['Fecha'])
#
# # Convierte la columna de fechas a números enteros
# partidos['Fecha'] = partidos['Fecha'].apply(lambda x: dt.datetime.toordinal(x))

# carga la base de datos de predicciones y resultados
predicciones = pd.read_csv('../data/Estadisticas.csv', sep=';')

# seleccionar las columnas necesarias
predicciones = predicciones[['Minuto', 'Linea', 'Probabilidad', 'CornersFinales']]

# unir los DataFrames utilizando las columnas "Local" y "Visitante"
# data = pd.merge(predicciones, partidos, on=['Local', 'Visitante'])

# seleccionar las características y la variable objetivo
X = predicciones[['Minuto', 'Probabilidad']]
y = predicciones['CornersFinales']

# dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20, train_size=0.8)

# normalizar las características
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# crear y entrenar el modelo de red neuronal
modelo = MLPClassifier(hidden_layer_sizes=(10, 5), max_iter=1000)
modelo.fit(X_train, y_train)

# hacer predicciones con el conjunto de prueba
y_pred = modelo.predict(X_test)

# evaluar la precisión del modelo
precisión = accuracy_score(y_test, y_pred)
print('Precisión: {:.2f}%'.format(precisión * 100))
