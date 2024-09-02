### Descripción de los notebook y ficheros .py

- extraccion_atributos.py, funciones de extracciones implementadas
- 1_creacion_conjunto_de_datos.ipynb, notebook sobre la creación del conjunto de datos inicial
- 2_creacion_dataset_con_atributos.py, fichero py para crear el conjunto de datos con las extracciones de atributos respectivo de cada URL
- 3_exploracion_de_datos.ipynb, notebook sobre la exploración de datos
- 4_clasificacion_multiclases.ipynb, notebook con las implementaciones de los modelos de aprendizaje automático
- 5_limite_de_decisioones.ipynb, notebook con las gráficas de límites de decisiones usando el paquete mlxtend

### Descripción de las carpetas
Carpeta dataset: contiene 3 ficheros:
- conjunto de datos inicial sin atributos (dataset.csv)
- conjunto de datos con atributos con duplicados (dataset_con_atrib.csv)
- conjunto de datos con atributos sin duplicados (dataset_con_atrib_no_dup.csv)

Carpeta fichero: contiene 2 ficheros, lista de acortadores y fichero con URLs de pruebas para la aplicación web (test.csv)

Carpeta gui: contiene la aplicación web desarrollada usando Streamlit.

Carpeta keras_tuner_resultados_multi: contiene los resultados de la busqueda en malla del modelo de redes neuronales.

### Ejecutar aplicación web en local
Para poder ejecutar la aplicación web en local primero realizar un git clone del repositorio.

Después de clonar el repositorio abrir la carpeta del proyecto con cualquier editor de código por ejemplo VS Code.

En la terminal del VS Code escribir: cd gui > streamlit run gui.py

Para detener la aplicación web: ctrl + c

Esto lanzará la aplicación web.
![image](https://github.com/user-attachments/assets/199ceb51-03e0-4f4f-a2e9-412fed15bb1e)
