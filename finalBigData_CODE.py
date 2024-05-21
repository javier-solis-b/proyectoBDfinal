import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Cargar el conjunto de datos
df = pd.read_csv("C:/Users/javis/OneDrive/Escritorio/8VO_SEMESTRE/Big_Data/proyecto_final_BD/WallCityTap_Consumer.csv", encoding='latin1')

# Preprocesamiento: Eliminar columnas no numéricas y/o manejar valores faltantes
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()  # Selecciona solo columnas numéricas
df_numeric = df[numeric_columns]

# Función para calcular la WCSS
def calculate_wcss(data):
    wcss = []
    for i in range(1, 11):  # Ajusta el rango según tus necesidades
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(data)
        wcss.append(kmeans.inertia_)
    return wcss

# Calcular la WCSS para diferentes valores de k
wcss = calculate_wcss(df_numeric)

# Graficar la WCSS vs k
plt.plot(range(1, 11), wcss)
plt.title('Método del Codo')
plt.xlabel('Cantidad de Centroides k')
plt.ylabel('WCSS')
plt.show()
