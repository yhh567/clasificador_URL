import ipaddress
from urllib.parse import urlparse
import re
from math import log2
from collections import Counter
import whois
from datetime import datetime
from pathlib import Path

CWD = Path.cwd()

def longitud_url(url):
    """Calcula la longitud de la url"""
    
    return len(url)

def longitud_hostname(url):
    """Calcula la longitud del hostname de la url"""
    
    url_parseada = urlparse(url)
    hostname = url_parseada.hostname
    
    if hostname:
        return len(hostname)
    return 0

def longitud_de_ruta(url):
    """Calcula la longitud de la ruta de la url"""
    
    url_parseada = urlparse(url)
    ruta = url_parseada.path

    return len(ruta)

def longitud_de_consulta(url):
    """Calcula la longitud de la consulta de la url"""
    
    url_parseada = urlparse(url)
    consulta = url_parseada.query
    
    return len(consulta)

def contiene_https(url):
    """Comprueba si la url contiene https"""
    
    url_parseada = urlparse(url)
    esquema = url_parseada.scheme
    
    if esquema == 'https':
        return 1 
    return 0

def contiene_ip(url):
    """Comprueba si la url contiene direcciones ip en el host"""

    try:
        url_parseada = urlparse(url)
        hostname = url_parseada.hostname
        ipaddress.ip_address(hostname)
        return 1
    except Exception:
        return 0

def contiene_php(url):
    """Comprueba si la url contiene la palabra php en la ruta"""
    
    url_parseada = urlparse(url)
    ruta = url_parseada.path
    if 'php' in ruta:
        return 1
    else:
        return 0

def contiene_html(url):
    """Comprueba si la url contiene la palabra html en la ruta"""
    
    url_parseada = urlparse(url)
    ruta = url_parseada.path
    if 'html' in ruta:
        return 1
    else:
        return 0

def contiene_doble_barras(url):
    """Comprueba si la url contiene doble barras que no sea en el esquema"""
    
    url_parseada = urlparse(url)
    ruta = url_parseada.path
    consulta = url_parseada.query
    fragmento = url_parseada.fragment

    if '//' in ruta or '//' in consulta or '//' in fragmento:
        return 1
    return 0

def profundidad_la_ruta(url):
    """Calcula la profundidad de la ruta de la url"""
    
    url_parseada = urlparse(url)
    ruta = url_parseada.path
    
    # Manejo de los casos de url que acaban en / sin especificar recursos
    if url.endswith('/') and len(ruta) == 1:
        return 0
    return ruta.count('/')

def acortadores_de_url(url):
    """
        Comprueba si la url ha sido acortado
        Lista de acortadores sacados de: https://github.com/PeterDaveHello/url-shorteners/blob/master/list
    """
    
    with open(CWD / 'ficheros' /'lista_acortadores_url.txt', 'r') as fichero:
        for linea in fichero:
            coincidencias = re.search(linea.strip(), url)
            if coincidencias:
                return 1
    return 0

def num_digitos(url):
    """Calcula los digitos que contiene la url"""
    
    return len([c for c in url if c.isdigit()])

def num_caracteres_especiales(url):
    """
        Calcula el número de caracteres especiales que no sean alfanumérico de la url
    """
        
    url_parseada = urlparse(url)
    
    url_sin_esquema = url_parseada.netloc + url_parseada.path \
        + url_parseada.params+ url_parseada.query + url_parseada.fragment
    
    char_especiales = [c for c in url_sin_esquema if not c.isalnum()]
    
    return len(char_especiales)

def dom_dias_activo(url):
    """
        Calcula los dias activos del dominio, devuelve 0 o los dias que lleva activo el dominio
    """
       
    fecha_actual = datetime.today() # Obtener fecha actual para calcular la diferencia
    dias_activos = 0 # Inicialización variable
    
    try:
        url_parseada = urlparse(url)
        dominio = url_parseada.netloc
        dominio_info = whois.whois(dominio) # Información del dominio mediante consulta a WHOIS
        fecha_creacion = dominio_info.creation_date # Obtener la fecha de creación del dominio
        
        if fecha_creacion is None: # Si la fecha es None devolver 0
            dias_activos = 0
    
        if isinstance(fecha_creacion, str): # Si la fecha es un string con formato Año-Mes-Dia
            try:
                fecha_creacion = datetime.strptime(fecha_creacion, '%Y-%m-%d') # Convertir a formato datetime
                dias_activos = (fecha_actual - fecha_creacion).days # Calcular los dias activos del dominio
            except Exception:
                dias_activos = 0 # Si ocurre una excepción devolver 0
        elif isinstance(fecha_creacion, list): # Si la fecha es una lista
            try:
                fecha_creacion = fecha_creacion[-1] # Quedarse con la última fecha, la más reciente
                fecha_creacion = fecha_creacion.replace(tzinfo=None) # Eliminar el timezone para lidiar con los problemas de ariméticas
                dias_activos = (fecha_actual - fecha_creacion).days
            except Exception:
                dias_activos = 0 # Si ocurre una excepción devolver 0
        else: # Si no es ninguno de los casos anteriores, calcular dias activos
            dias_activos = (fecha_actual - fecha_creacion).days
    
    except Exception: # Manejo de los casos en que la url no está dentro de WHOIS
        dias_activos = 0
    return dias_activos

def dom_dias_hasta_expiracion(url):
    """
        Calcula los dias hasta la expiración del dominio, devuelve -1 si ya expiró 
        o los dias que falta para la expiracón del dominio
    """
    
    fecha_actual = datetime.today()
    dias_hasta_expiracion = -1 # -1 para indicar que ya expiró el dominio si salta excepciones

    try:
        url_parseada = urlparse(url)
        dominio = url_parseada.netloc
        dominio_info = whois.whois(dominio)
        fecha_expiracion = dominio_info.expiration_date

        if fecha_expiracion is None:
            dias_hasta_expiracion = -1

        if isinstance(fecha_expiracion, str):
            try:
                fecha_expiracion = datetime.strptime(fecha_expiracion, '%Y-%m-%d')
                dias_hasta_expiracion = (fecha_expiracion - fecha_actual).days
            except Exception:
                dias_hasta_expiracion = -1
        elif isinstance(fecha_expiracion, list):
            try:
                fecha_expiracion = fecha_expiracion[-1]
                fecha_expiracion = fecha_expiracion.replace(tzinfo=None)
                dias_hasta_expiracion = (fecha_expiracion - fecha_actual).days
            except Exception:
                dias_hasta_expiracion = -1
        else:
            dias_hasta_expiracion = (fecha_expiracion - fecha_actual).days

    except Exception:
        dias_hasta_expiracion = -1

    return dias_hasta_expiracion

def entropia(url):
    """
        Calcula la entropia de Shannon
        La entropia de Shannon representa la cantidad de información dentro de un texto. Es una medida de incertidumbre
        Fuente de código original: https://rosettacode.org/wiki/Entropy#Python:_More_succinct_version
    """
    
    p, lns = Counter(url), float(len(url))
    return log2(lns) - sum(count * log2(count) for count in p.values()) / lns

def extracciones_de_atributos(url):
    """Crea una lista con las extracciones de cada url"""    
    
    atributos = []
    
    atributos.append(longitud_url(url))
    atributos.append(longitud_hostname(url))
    atributos.append(longitud_de_ruta(url))
    atributos.append(longitud_de_consulta(url))
    atributos.append(contiene_https(url))
    atributos.append(contiene_ip(url))
    atributos.append(contiene_php(url))
    atributos.append(contiene_html(url))
    atributos.append(contiene_doble_barras(url))
    atributos.append(profundidad_la_ruta(url))
    atributos.append(acortadores_de_url(url))
    atributos.append(num_digitos(url))
    atributos.append(num_caracteres_especiales(url))
    atributos.append(dom_dias_activo(url))
    atributos.append(dom_dias_hasta_expiracion(url))
    atributos.append(entropia(url))
    
    return atributos

