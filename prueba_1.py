import streamlit as st
import pandas as pd
import requests
import io
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# URL base de los archivos en GitHub (reemplaza con la tuya)
GITHUB_BASE_URL = "https://raw.githubusercontent.com/tu_usuario/tu_repositorio/main/"

# Diccionario con los archivos de cada país
files = {
    "Peru": "consolidado_peru.xlsx",
    "Colombia": "consolidado_colombia.xlsx",
    "Ecuador": "consolidado_ecuador.xlsx",
    "Bolivia": "consolidado_bolivia.xlsx"
}

def load_excel_from_github(url):
    """Descarga un archivo Excel desde GitHub y lo carga en un DataFrame."""
    response = requests.get(url)
    if response.status_code == 200:
        file_bytes = io.BytesIO(response.content)
        with pd.ExcelFile(file_bytes) as xls:
            sheet_name = 'Sheet1' if 'Sheet1' in xls.sheet_names else xls.sheet_names[0]
            return pd.read_excel(xls, sheet_name=sheet_name)
    else:
        st.error(f"Error al descargar: {url} (Código {response.status_code})")
        return None

# Cargar todos los archivos en un solo DataFrame
dataframes = []
for country, file in files.items():
    file_url = GITHUB_BASE_URL + file
    df = load_excel_from_github(file_url)
    if df is not None:
        df["Pais"] = country
        dataframes.append(df)

# Unificar los DataFrames
if dataframes:
    df_combined = pd.concat(dataframes, ignore_index=True)

    # Normalizar nombres de columnas
    column_map = {
        "Droga Decomisada (kg)": "Drogas",
        "CANTIDAD_DROGA": "Drogas",
        "TOTAL_DROGAS_KG.": "Drogas",
        "Cocaína (ton)": "Drogas",
        "CANTIDAD_ARMAS": "Armas",
        "Latitud": "lat", "LATITUD": "lat", "Latitud ": "lat",
        "Longitud": "lon", "LONGITUD": "lon"
    }
    df_combined.rename(columns=column_map, inplace=True)

    # Verificación de columnas
    for col in ['lat', 'lon', 'Drogas', 'Armas']:
        if col not in df_combined.columns:
            df_combined[col] = 0  # Crear la columna si no existe

    # Conversión a valores numéricos
    for col in ['lat', 'lon', 'Drogas', 'Armas']:
        df_combined[col] = pd.to_numeric(df_combined[col], errors='coerce')

    # Eliminar filas sin latitud o longitud
    df_combined.dropna(subset=['lat', 'lon'], inplace=True)

# Sidebar para navegación
page = st.radio("Seleccione una sección:", ["Información General", "Mapa de Drogas", "Mapa de Armas"])

# Mapas de Drogas y Armas
if page == "Mapa de Drogas":
    df_filtered = df_combined[df_combined['Drogas'] > 0]
    map_object = folium.Map(location=[-10, -75], zoom_start=4)
    HeatMap(data=df_filtered[['lat', 'lon', 'Drogas']].values, radius=8).add_to(map_object)
    folium_static(map_object)
elif page == "Mapa de Armas":
    df_filtered = df_combined[df_combined['Armas'] > 0]
    map_object = folium.Map(location=[-10, -75], zoom_start=4)
    HeatMap(data=df_filtered[['lat', 'lon', 'Armas']].values, radius=8).add_to(map_object)
    folium_static(map_object)
