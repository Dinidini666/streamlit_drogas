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
    file_peru = "consolidado_peru.xlsx"
    file_colombia = "consolidado_colombia.xlsx"
    file_ecuador = "consolidado_ecuador.xlsx"
    file_bolivia = "consolidado_bolivia.xlsx"
    
    df_peru = pd.read_excel(file_peru, sheet_name="Sheet1")
    df_colombia = pd.read_excel(file_colombia, sheet_name="Sheet1")
    df_ecuador = pd.read_excel(file_ecuador, sheet_name="Sheet1")
    df_bolivia_2022 = pd.read_excel(file_bolivia, sheet_name="2022")
    df_bolivia_2023 = pd.read_excel(file_bolivia, sheet_name="2023")
    
    df_bolivia = pd.concat([df_bolivia_2022, df_bolivia_2023])
    
    df_peru.rename(columns={'Droga Decomisada (kg)': 'Drogas', 'Latitud': 'lat', 'Longitud': 'lon'}, inplace=True)
    df_colombia.rename(columns={'CANTIDAD_DROGA': 'Drogas', 'LATITUD': 'lat', 'LONGITUD': 'lon', 'CANTIDAD_ARMAS': 'Armas'}, inplace=True)
    df_ecuador.rename(columns={'TOTAL_DROGAS_KG.': 'Drogas', 'LATITUD': 'lat', 'LONGITUD': 'lon'}, inplace=True)
    df_bolivia.rename(columns={'Cocaína (ton)': 'Drogas', 'Latitud': 'lat', 'Longitud': 'lon'}, inplace=True)
    
    # Convertir a numérico y filtrar datos válidos
    drug_data = pd.concat([df_peru, df_colombia, df_ecuador, df_bolivia])
    drug_data[['lat', 'lon', 'Drogas']] = drug_data[['lat', 'lon', 'Drogas']].apply(pd.to_numeric, errors='coerce')
    drug_data = drug_data.dropna(subset=['lat', 'lon', 'Drogas'])
    
    if page == "Mapa de Drogas":
        drug_map = folium.Map(location=[-10, -75], zoom_start=4)
        HeatMap(data=drug_data[['lat', 'lon', 'Drogas']].values, radius=8, max_val=drug_data['Drogas'].max()).add_to(drug_map)
        for _, row in drug_data.iterrows():
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=f"Cantidad: {row['Drogas']} kg",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(drug_map)
        folium_static(drug_map)
    else:
        weapons_data = df_colombia[['lat', 'lon', 'Armas']].dropna()
        heatmap_data = weapons_data[['lat', 'lon', 'Armas']].values
        map_view = folium.Map(location=[-10, -75], zoom_start=4)
        HeatMap(data=heatmap_data, radius=8).add_to(map_view)
        folium_static(map_view)
