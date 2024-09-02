import streamlit as st
import time
import joblib
import pickle
from keras import models
from extraccion_atributos import extracciones_de_atributos
import numpy as np
from sklearn.preprocessing import LabelEncoder
from pathlib import Path
from urllib.parse import urlparse
import whois

# Obtener el directorio de trabajo actual
CWD = Path.cwd()                                               

# Optimización carga de los modelos
@st.cache_resource
def modelo_rf():
    return joblib.load(CWD / 'rf.pkl')

@st.cache_resource
def modelo_nn():
    return models.load_model(CWD / 'nn_keras.h5')

def validacion_url(url: str):
    """ 
        Función simple que comprueba si una URL es válida
    """

    # Agregar por defecto http:// a las URL, casos example.com
    if not (url.startswith('http') or url.startswith('https')):
        url = 'http://' + url
    
    url_parseada = urlparse(url)
    
    try:
        dominio_info = whois.whois(url_parseada.netloc)
    
        # Devolver True si la URL cumple las condiciones de tener un esquema y un dominio registrado en whois
        return all([url_parseada.scheme, dominio_info.domain_name])
    
    except Exception:
        return False

def predecir(entrada_de_usuario: str, nombre_del_modelo: str, modelo_seleccionado: object):
    
    """
        Función que predice la entrada dada por el usuario,
        para ello primero escala los atributos extraidos
        y el modelo seleccionado devuelve la predicción
    """
    
    # Extraer los atributos de la URL proporcionada
    res = extracciones_de_atributos(entrada_de_usuario)         
    
    le = LabelEncoder()                                         
    le.classes_ = np.load(CWD / 'clases_le.npy', allow_pickle=True) # Cargar el encoder usado
    
    rbscaler_multi = CWD / 'rbscaler_multi.sav'
    scaler = pickle.load(open(rbscaler_multi, 'rb'))            # Cargar el escalador usado

    modelo = modelo_seleccionado
    
    if nombre_del_modelo == 'RF':
        pred = modelo.predict(scaler.transform(np.array(res).reshape(1, -1)))
    else:
        pred = np.argmax(modelo.predict(scaler.transform(np.array(res).reshape(1, -1))), axis=1)
    
    # Animación de espera
    with st.spinner('Espera un momento los resultados estarán enseguida...'):
        time.sleep(8)

        res = le.inverse_transform(pred)[0]
                 
        st.write(f'Los resultados indica que la URL es: **{res}**.')
        
        if res == 'benign':
            st.write("Sitios web legítimos, confiables que no son maliciosas.")
        elif res == 'phishing':
            st.write("Sitios web que finge ser una entidad confiable para obtener la información del usuario.") 
        elif res == 'defacement':
            st.write('Sitios web que han sido comprometido por el atacante modificando la apariencia del sitio original.')
        elif res == 'malware':
            st.write('Sitios web con software malicioso para robar o dañar el dispositivo del usuario.')
        
        
        _ , col2 = st.columns([.3,.7])  # Alineamiento de las imagenes
        
        if res == 'benign':             # Mostrar imagen si es una URL del tipo 'benign'
            with col2:
                st.image(str(CWD / 'image_safe.png'),
                         caption='Source: Freepik @upklyak')        
        else:
            with col2:                  # Mostrar imagen para toda URL maliciosa
                st.image(str(CWD/ 'image_malicious.png'), 
                         caption='Source: Freepik @upklyak')


if __name__ == '__main__':

    st.header('Clasificador de URL', divider='gray')
    st.write("""
             Modelo entrenado basado en el algoritmo de Random Forest y Redes Neuronales Artificiales.
             """)
    
    seleccion_modelo = st.sidebar.selectbox(
        "Elige un modelo",
        ("RF", "NN")
    )

    if seleccion_modelo == 'RF':
        st.sidebar.text("Modelo de Random Forest")
        nombre_del_modelo = 'RF'
        try:
            modelo_seleccionado = modelo_rf()
            
        except Exception:
            print("No se ha podido cargar el modelo")
    else:
        st.sidebar.text("Modelo de redes neuronales")  
        nombre_del_modelo = 'NN'
        try:
            modelo_seleccionado = modelo_nn()
            
        except Exception:
            print("No se ha podido cargar el modelo")
    
    # st.sidebar.divider()
    # st.sidebar.write(
    #     """
    #     *Hola soy el autor, este es un proyecto pensado para poder visualizar los resultados
    #     de los modelos entrenados dejaré un conjunto 'test' en github para poder probar la aplicación.
    #     La aplicación en situaciones reales tiene sus limitaciones debido a la reducida información
    #     usado en el entrenamiento del modelo.*
    #     """
    # )
    

    # Formateo de text_input y botón
    with st.form("formulario"):
        
        col1, col2 = st.columns([.87,.13])
        
        with col1:
            entrada_de_usuario = st.text_input("some_text", placeholder="Introduce una URL para analizar", 
                                               label_visibility='collapsed')
            validacion_entrada = validacion_url(entrada_de_usuario)

        with col2:
            boton = st.form_submit_button('Analizar', type='primary')
        
        if validacion_entrada and boton:
            predecir(entrada_de_usuario, nombre_del_modelo, modelo_seleccionado)
        elif not validacion_entrada and boton:
            st.error("""
                     Ha ocurrido un error. Posibles causas:
                     1. La URL introducida no es válida.
                     2. La URL es válida sin embargo ha ocurrido un timeout en la consulta. Inténtelo de nuevo
                     """)
            
    # Desplegable informacion adicional
    with st.expander("Información adicional acerca de las URL maliciosas"):
        st.write('[What is URL phishing and how to avoid it? (surfshark)](https://surfshark.com/blog/what-is-url-phishing)')
        st.write('[What is website defacement? (imperva)](https://www.imperva.com/learn/application-security/website-defacement-attack/)')
        st.write('[What is website malware? (sucuri)](https://sucuri.net/guides/website-malware/)')
