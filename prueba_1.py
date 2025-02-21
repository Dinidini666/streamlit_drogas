import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Configurar título de la app
st.title("Mapas de Calor: Drogas y Armas en la Comunidad Andina")

# Subir archivos directamente desde Streamlit
st.sidebar.header("Cargar Archivos Excel")
uploaded_files = {
    "Peru": st.sidebar.file_uploader("Sube el archivo de Perú", type=["xlsx"]),
    "Colombia": st.sidebar.file_uploader("Sube el archivo de Colombia", type=["xlsx"]),
    "Ecuador": st.sidebar.file_uploader("Sube el archivo de Ecuador", type=["xlsx"]),
    "Bolivia": st.sidebar.file_uploader("Sube el archivo de Bolivia", type=["xlsx"])
}

# Diccionario para almacenar DataFrames
dataframes = {}

# Cargar archivos
for country, uploaded_file in uploaded_files.items():
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        df["Pais"] = country  # Agregar columna del país
        dataframes[country] = df

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

    # Seleccionar mapa
    option = st.sidebar.radio("Selecciona el mapa:", ["Mapa de Drogas", "Mapa de Armas"])

    # Crear mapa base
    map_object = folium.Map(location=[-10, -75], zoom_start=4)

    if option == "Mapa de Drogas":
        df_filtered = df_combined[df_combined['Drogas'] > 0]
        HeatMap(data=df_filtered[['lat', 'lon', 'Drogas']].values, radius=8).add_to(map_object)
        
        # Agregar marcadores interactivos
        for _, row in df_filtered.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=f"<b>País:</b> {row['Pais']}<br><b>Drogas decomisadas:</b> {row['Drogas']} kg",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(map_object)

    elif option == "Mapa de Armas":
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

else:
    st.warning("Sube al menos un archivo Excel para generar los mapas.")
