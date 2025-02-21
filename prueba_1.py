# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:59:13 2025

@author: user
"""
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

La base de datos utilizada es pública; sin embargo, este trabajo implicó un proceso de selección, limpieza y organización de los datos más relevantes, 
de manera que puedan ser utilizados eficazmente por los países de la región para la toma de decisiones.

Utilice los botones a continuación para navegar entre los mapas de calor.
""")

# Sidebar para navegación
page = st.radio("Seleccione una sección:", ["Información General", "Mapa de Drogas", "Mapa de Armas"])

# Información General
if page == "Información General":
    st.markdown("""
    ## Mecanismos y Programas Internacionales Relacionados
    A continuación se presentan las principales organizaciones y programas que abordan la problemática de las drogas y las armas en la Comunidad Andina:
    """)
    
    data = {
        "Organización": ["ONU", "ONU", "OEA", "UE", "INTERPOL", "INTERPOL"],
        "Mecanismo/Programa": [
            "Oficina de las Naciones Unidas contra la Droga y el Delito (UNODC)",
            "Programa Mundial sobre Armas de Fuego de la UNODC",
            "Comisión Interamericana para el Control del Abuso de Drogas (CICAD)",
            "Estrategia de la UE sobre Drogas 2021-2025",
            "Proyecto AMEAP",
            "Proyecto DISRUPT"
        ],
        "Enfoque": ["Drogas", "Armas", "Drogas", "Drogas", "Drogas", "Armas"],
        "Normativa Asociada": [
            "Convención Única sobre Estupefacientes de 1961; Convenio sobre Sustancias Sicotrópicas de 1971; Convención de las Naciones Unidas contra el Tráfico Ilícito de Estupefacientes y Sustancias Sicotrópicas de 1988",
            "Protocolo contra la Fabricación y el Tráfico Ilícitos de Armas de Fuego (2001)",
            "Convención Interamericana contra la Fabricación y el Tráfico Ilícitos de Armas de Fuego (CIFTA) de 1997",
            "Estrategia de la UE en materia de lucha contra la droga 2021-2025",
            "No se asocia a una normativa específica, pero opera bajo el marco de cooperación internacional en materia de control de drogas.",
            "No se asocia a una normativa específica, pero se alinea con el Protocolo contra la Fabricación y el Tráfico Ilícitos de Armas de Fuego."
        ],
        "Países de la Comunidad Andina Firmantes": [
            "Bolivia, Colombia, Ecuador y Perú",
            "Bolivia, Colombia, Ecuador y Perú",
            "Bolivia, Colombia, Ecuador y Perú",
            "No aplica directamente a la Comunidad Andina",
            "Bolivia, Colombia, Ecuador y Perú",
            "Bolivia, Colombia, Ecuador y Perú"
        ]
    }
    
    df_info = pd.DataFrame(data)
    st.dataframe(df_info)

# Mapas de Drogas y Armas
if page == "Mapa de Drogas" or page == "Mapa de Armas":
    st.title(f"Mapa de Calor: {page.split()[1]} en la Comunidad Andina")
    
    # Cargar los datos
    files = {
        "Peru": "consolidado_peru.xlsx",
        "Colombia": "consolidado_colombia.xlsx",
        "Ecuador": "consolidado_ecuador.xlsx",
        "Bolivia": "consolidado_bolivia.xlsx"
    }
    
    dataframes = []
    for country, file in files.items():
        df = pd.read_excel(file, sheet_name="Sheet1")
        df["Pais"] = country
        dataframes.append(df)
    
    df_combined = pd.concat(dataframes, ignore_index=True)
    
    column_map = {'Droga Decomisada (kg)': 'Drogas', 'Latitud': 'lat', 'Longitud': 'lon',
                  'CANTIDAD_DROGA': 'Drogas', 'CANTIDAD_ARMAS': 'Armas', 'TOTAL_DROGAS_KG.': 'Drogas',
                  'Cocaína (ton)': 'Drogas'}
    df_combined.rename(columns=column_map, inplace=True)
    
    df_combined[['lat', 'lon', 'Drogas', 'Armas']] = df_combined[['lat', 'lon', 'Drogas', 'Armas']].apply(pd.to_numeric, errors='coerce')
    df_combined = df_combined.dropna(subset=['lat', 'lon'])
    
    if page == "Mapa de Drogas":
        df_filtered = df_combined.dropna(subset=['Drogas'])
        map_object = folium.Map(location=[-10, -75], zoom_start=4)
        HeatMap(data=df_filtered[['lat', 'lon', 'Drogas']].values, radius=8, max_val=df_filtered['Drogas'].max()).add_to(map_object)
        folium_static(map_object)
    else:
        df_filtered = df_combined.dropna(subset=['Armas'])
        map_object = folium.Map(location=[-10, -75], zoom_start=4)
        HeatMap(data=df_filtered[['lat', 'lon', 'Armas']].values, radius=8, max_val=df_filtered['Armas'].max()).add_to(map_object)
        folium_static(map_object)
