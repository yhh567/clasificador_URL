import pandas as pd
from extraccion_atributos import extracciones_de_atributos

# Descripción del archivo:
# Este código tiene la finalidad de crear el conjunto de datos para el proyecto
# Para ello creará una lista con las extracciones correspondiente de cada url 
# Aplicándoles las funciones de extracciones del fichero extraccion_atributos.py
# Una vez finalizada las extracciones se creará un dataframe apartir de la lista
# Nombrandolo a cada columna con sus correspondiente nombre
# Finalmente se guarda el conjunto de datos en un fichero csv para posterior uso

# Inicializado
print("Se esta ejecutando")

df = pd.read_csv('dataset/dataset.csv')

# print(df)
# print(len(df))

# El siguiente bucle recorre de 0 a 19999 leyendo cada url del dataframe y aplicando las funciones de extracciones
lista_de_atributos = []

for i in range(0, 20000):
    url = df['url'][i]
    lista_de_atributos.append(extracciones_de_atributos(url))
    

nombre_de_columnas = ['longitud_url', 'longitud_hostname', 'longitud_de_ruta', 'longitud_de_consulta', 'contiene_https', 
                       'contiene_ip', 'contiene_php', 'contiene_html', 'contiene_doble_barras', 'profundidad_de_la_ruta', 
                       'acortadores_de_url', 'num_digitos', 'num_caracteres_especiales', 'dom_dias_activo', 
                       'dom_dias_hasta_expiracion', 'entropia']

# Convertir la lista en un dataframe con las columnas correspondiente
df_con_atributos = pd.DataFrame(lista_de_atributos, columns=nombre_de_columnas)

# Unir el dataframe de los atributos con el dataframe de las url y type
dataset_con_atributos = pd.concat([df, df_con_atributos], axis=1).reset_index(drop=True)

# Guardar el dataframe para uso posterior
dataset_con_atributos.to_csv('dataset_con_atributos_final.csv', index=False)

# Finalizado
print('Fin de la ejecuccion')
