# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:59:13 2025

@author: user
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Cargar datos desde Excel
archivo_excel = "Organismos_Lucha_Drogas_Armas.xlsx"
df_incautaciones = pd.read_excel(archivo_excel, sheet_name="2024")
df_organismos = pd.read_excel(archivo_excel, sheet_name="Sheet1")
df_fuentes = pd.read_excel(archivo_excel, sheet_name="Hoja2")

# Diccionario de coordenadas para los puntos
coordenadas = {
    "VRAEM": (-13.030239, -73.527642),
    "zonas cercanas a la frontera con Brasil": (-11.181560, -69.696645),
    "Cochabamba mayor cantidad": (-17.403949, -66.180874),
    "Nariño": (1.717644, -78.015853),
    "Cauca": (2.205564, -77.827279),
    "Carchi": (0.759330, -78.118665),
    "Esmeraldas": (1.207707, -78.723301),
    "Sucumbíos": (0.266970, -77.208508)
}

# Expandir filas con múltiples ubicaciones
df_incautaciones["Lugar_especifico"] = df_incautaciones["Lugar específico"].replace({
    "VRAEM / zonas cercanas a la frontera con brasil": "VRAEM, zonas cercanas a la frontera con Brasil",
    "Nariño y Cauca": "Nariño, Cauca",
    "Esmeraldas y Sucumbíos": "Esmeraldas, Sucumbíos"
})
df_expanded = df_incautaciones.assign(Lugar_especifico=df_incautaciones["Lugar_especifico"].str.split(", ")).explode("Lugar_especifico")

# Asignar coordenadas
df_expanded["Latitud"] = df_expanded["Lugar_especifico"].map(lambda x: coordenadas.get(x, (None, None))[0])
df_expanded["Longitud"] = df_expanded["Lugar_especifico"].map(lambda x: coordenadas.get(x, (None, None))[1])
df_expanded = df_expanded.dropna(subset=["Latitud", "Longitud"])

# Crear el mapa con Folium
st.title("Mapa de Incautaciones de Drogas y Armas")
m = folium.Map(location=[-10, -70], zoom_start=4)

# Agregar puntos al mapa
for _, row in df_expanded.iterrows():
    folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        popup=f"{row['Lugar_especifico']} ({row['País']})\nIncautaciones de drogas: {row['Incautacion de drogas']}\nIncautaciones de armas: {row['incautacion de armas']}",
        tooltip=row["Lugar_especifico"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

st_folium(m)

# Mostrar tabla de organismos internacionales
st.header("Organismos y Programas Internacionales")
st.dataframe(df_organismos)

# Mostrar fuentes de información
st.header("Fuentes de Información")
st.write("Fuentes utilizadas para recopilar los datos:")
for url in df_fuentes.iloc[:, 1].dropna():
    st.markdown(f"- [{url}]({url})")
