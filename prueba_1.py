# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Introducción y navegación
st.title("Mapa de Calor: Drogas y Armas en la Comunidad Andina")

st.markdown("""
## Introducción
Este dashboard muestra un análisis geoespacial sobre la incautación de drogas y armas en la Comunidad Andina desde el año 2019. 
Los datos provienen de fuentes oficiales y están en constante actualización. En futuras versiones, se implementará la opción de visualizar los datos por año.
""")

# Sidebar para navegación
page = st.radio("Seleccione una sección:", ["Información General", "Mapa de Drogas", "Mapa de Armas"])

# Cargar los datos
files = {
    "Peru": "/mnt/data/consolidado_peru.xlsx",
    "Colombia": "/mnt/data/consolidado_colombia.xlsx",
    "Ecuador": "/mnt/data/consolidado_ecuador.xlsx",
    "Bolivia": "/mnt/data/consolidado_bolivia.xlsx"
}

dataframes = []

for country, file in files.items():
    with pd.ExcelFile(file) as xls:
        sheet_name = 'Sheet1' if 'Sheet1' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df["Pais"] = country

        # Ajustar nombres de columnas
        column_map = {
            "Droga Decomisada (kg)": "Drogas",
            "CANTIDAD_DROGA": "Drogas",
            "TOTAL_DROGAS_KG.": "Drogas",
            "Cocaína (ton)": "Drogas",
            "CANTIDAD_ARMAS": "Armas",
            "Latitud": "lat", "LATITUD": "lat", "Latitud ": "lat",
            "Longitud": "lon", "LONGITUD": "lon"
        }
        df.rename(columns=column_map, inplace=True)

        # Limpiar datos de Ecuador
        if country == "Ecuador":
            df.replace("non", None, inplace=True)  # Eliminar valores "non"
        
        # Seleccionar columnas necesarias
        required_columns = ['lat', 'lon', 'Drogas', 'Armas']
        for col in required_columns:
            if col not in df.columns:
                df[col] = 0  # Crear la columna si no existe

        # Asegurar que latitud y longitud sean numéricas
        for col in ['lat', 'lon', 'Drogas', 'Armas']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        dataframes.append(df)

df_combined = pd.concat(dataframes, ignore_index=True)

# Eliminar filas con latitud o longitud vacías
df_combined.dropna(subset=['lat', 'lon'], inplace=True)

# Mostrar mapa de calor
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
