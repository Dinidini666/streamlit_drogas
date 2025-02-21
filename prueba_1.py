import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Configurar título de la app
st.title("Mapa de Calor: Drogas y Armas en la Comunidad Andina")

st.markdown("""
## Introducción
Este dashboard muestra un análisis geoespacial sobre la incautación de drogas y armas en la Comunidad Andina desde el año 2019. 
Los datos provienen de fuentes oficiales y están en constante actualización.
""")

# Sidebar para navegación
page = st.radio("Seleccione una sección:", ["Información General", "Mapa de Drogas", "Mapa de Armas"])

# URL de los archivos en GitHub (REEMPLAZA con la URL de tu repositorio)
files = {
    "Peru": "https://raw.githubusercontent.com/TU_USUARIO/TU_REPOSITORIO/main/consolidado_peru.xlsx",
    "Colombia": "https://raw.githubusercontent.com/TU_USUARIO/TU_REPOSITORIO/main/consolidado_colombia.xlsx",
    "Ecuador": "https://raw.githubusercontent.com/TU_USUARIO/TU_REPOSITORIO/main/consolidado_ecuador.xlsx",
    "Bolivia": "https://raw.githubusercontent.com/TU_USUARIO/TU_REPOSITORIO/main/consolidado_bolivia.xlsx"
}

# Cargar los datos
dataframes = []
for country, url in files.items():
    df = pd.read_excel(url)
    df["Pais"] = country
    dataframes.append(df)

# Unificar los DataFrames
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

# Asegurar que las columnas necesarias existen
for col in ['lat', 'lon', 'Drogas', 'Armas']:
    if col not in df_combined.columns:
        df_combined[col] = 0  # Crear la columna si no existe

# Convertir a numérico, asegurando que la columna no sea un DataFrame anidado
for col in ['lat', 'lon', 'Drogas', 'Armas']:
    df_combined[col] = df_combined[col].astype(str).str.replace(r'[^0-9.-]', '', regex=True)  # Eliminar caracteres no numéricos
    df_combined[col] = pd.to_numeric(df_combined[col], errors='coerce')

# Eliminar filas sin latitud o longitud
df_combined.dropna(subset=['lat', 'lon'], inplace=True)

# Seleccionar el mapa a mostrar
st.title(f"Mapa de Calor: {page.split()[1]} en la Comunidad Andina")

map_object = folium.Map(location=[-10, -75], zoom_start=4)

if page == "Mapa de Drogas":
    df_filtered = df_combined[df_combined['Drogas'] > 0]
    HeatMap(data=df_filtered[['lat', 'lon', 'Drogas']].values, radius=8).add_to(map_object)

    # Agregar marcadores interactivos
    for _, row in df_filtered.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<b>País:</b> {row['Pais']}<br><b>Drogas decomisadas:</b> {row['Drogas']} kg",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(map_object)

elif page == "Mapa de Armas":
    df_filtered = df_combined[df_combined['Armas'] > 0]
    HeatMap(data=df_filtered[['lat', 'lon', 'Armas']].values, radius=8).add_to(map_object)

    # Agregar marcadores interactivos
    for _, row in df_filtered.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<b>País:</b> {row['Pais']}<br><b>Armas decomisadas:</b> {row['Armas']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(map_object)

# Mostrar mapa en Streamlit
folium_static(map_object)
