#from scraping_dolar import obtener_valores_dolar
#from scraping_deptos import obtener_valores_depto
import pandas as pd
from unidecode import unidecode
import re
import os

# Obtener la ruta del directorio actual
directorio_actual = os.getcwd()

#cotizacion del dolar
#obtener_valores_dolar()
#valores deptos
#obtener_valores_depto()

#limpieza de los datos con pandas
ruta_dolar = os.path.join(directorio_actual, 'dataframes', 'cotizacion_dolar_hoy.csv')
ruta_deptos = os.path.join(directorio_actual, 'dataframes', 'venta_deptos.csv')
df_dolar = pd.read_csv(ruta_dolar, encoding='utf-8')
df_deptos = pd.read_csv(ruta_deptos, encoding='utf-8')

#limpieza datos de dolares
df_dolar['tipo_dolar'] = df_dolar['tipo_dolar'].apply(lambda x: unidecode(x).replace(' ', '_').lower())
df_dolar['valor_compra'] = df_dolar['valor_compra'].str.replace('$', '').astype(float)
df_dolar['valor_venta'] = df_dolar['valor_venta'].str.replace('$', '').astype(float)

ruta_nueva_dolar = os.path.join(directorio_actual, 'dataframes', 'cotizacion_dolar_hoy_limpio.csv')
df_dolar.to_csv(path_or_buf=ruta_nueva_dolar, index=False)

#limpieza datos deptos
df_deptos.dropna(inplace=True)
df_deptos['precio'] = (df_deptos['precio'].astype(int)) * 1000
df_deptos['direccion'] = df_deptos['direccion'].apply(lambda x: x.replace('.', ' ').replace(' ', '-').replace('al-', '').title().replace('--', '-').replace("[", '').replace("]", '').replace("'", '').split(',')[0])


def separar_calle_numero(direccion):
    # Dividir la dirección en partes utilizando el guion como separador
    partes = direccion.split('-')
    # Verificar si la última parte es un número
    ultimo_parte = partes[-1].strip()
    if ultimo_parte.isdigit():  # Si es un número, asumimos que es el número de la dirección
        calle = '-'.join(partes[:-1]).strip()
        numero = int(ultimo_parte)
    else:  # Si no es un número, asumimos que es parte del nombre de la calle
        calle = direccion
        numero = None
    return calle, numero


df_deptos[['calle', 'altura']] = df_deptos['direccion'].apply(separar_calle_numero).apply(pd.Series)
df_deptos.drop(columns=['direccion'], inplace=True)


# Función para extraer los números de la cadena de características
def extraer_numeros(caracteristicas):
    metros_totales = metros_cubiertos = ambientes = banios = dormitorios = cocheras = None

    for elem in caracteristicas:
        if 'M²-Tot' in elem:
            metros_totales_match = re.search(r'(\d+)', elem)
            metros_totales = float(metros_totales_match.group(1)) if metros_totales_match else None
        if 'M²-Cub' in elem:
            metros_cubiertos_match = re.search(r'(\d+)', elem)
            metros_cubiertos = float(metros_cubiertos_match.group(1)) if metros_cubiertos_match else None
        elif 'Amb' in elem:
            ambientes_match = re.search(r'(\d+)', elem)
            ambientes = int(ambientes_match.group(1)) if ambientes_match else None
        elif 'Baños' in elem:
            banios_match = re.search(r'(\d+)', elem)
            banios = int(banios_match.group(1)) if banios_match else None
        elif 'Baño' in elem:
            banios_match = re.search(r'(\d+)', elem)
            banios = int(banios_match.group(1)) if banios_match else None
        elif 'Dorm' in elem:
            dormitorios_match = re.search(r'(\d+)', elem)
            dormitorios = int(dormitorios_match.group(1)) if dormitorios_match else None
        elif 'Coch' in elem:
            cocheras_match = re.search(r'(\d+)', elem)
            cocheras = int(cocheras_match.group(1)) if cocheras_match else None

    return metros_totales, metros_cubiertos, ambientes, banios, dormitorios, cocheras


df_deptos['caracteristicas'] = df_deptos['caracteristicas'].apply(lambda x: x.replace(r'\n', ' ').replace('.', '').replace("'", '').replace("[", '').replace("]", '').title().replace(' ', '-').split(',-'))
# Aplicar la función a la columna 'caracteristicas'
df_deptos['metros_totales'], df_deptos['metros_cubiertos'], df_deptos['ambientes'], df_deptos['banios'], df_deptos['dormitorios'], df_deptos['cocheras'] = zip(*df_deptos['caracteristicas'].apply(extraer_numeros))
df_deptos.drop(columns=['caracteristicas'], inplace=True)

ruta_nueva_deptos = os.path.join(directorio_actual, 'dataframes', 'venta_deptos_limpio.csv')
df_deptos.to_csv(path_or_buf=ruta_nueva_deptos, index=False)
