# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:59:13 2025

@author: user
"""
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd

# Cargar el GeoDataFrame desde el archivo GeoJSON
gdf_path = "GeoDataFrame_Final.geojson"
gdf = gpd.read_file(gdf_path)

# Información adicional antes del mapa
st.title("Organismos de Lucha contra Drogas y Armas")

data_organismos = pd.DataFrame({
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
        "Convención Única sobre Estupefacientes de 1961; Convenio sobre Sustancias Sicotrópicas de 1971; Convención de 1988",
        "Protocolo contra la Fabricación y el Tráfico Ilícitos de Armas de Fuego (2001)",
        "Convención Interamericana contra la Fabricación y el Tráfico Ilícitos de Armas de Fuego (CIFTA) de 1997",
        "Estrategia de la UE en materia de lucha contra la droga 2021-2025",
        "No se asocia a una normativa específica, pero opera bajo el marco de cooperación internacional en materia de control de drogas.",
        "No se asocia a una normativa específica, pero se alinea con el Protocolo contra la Fabricación y el Tráfico Ilícitos de Armas de Fuego."
    ],
    "Países Firmantes": [
        "Bolivia, Colombia, Ecuador y Perú", "Bolivia, Colombia, Ecuador y Perú", "Bolivia, Colombia, Ecuador y Perú",
        "No aplica directamente a la Comunidad Andina", "Bolivia, Colombia, Ecuador y Perú", "Bolivia, Colombia, Ecuador y Perú"
    ]
})

st.dataframe(data_organismos)

# Crear el mapa con Folium
st.title("Mapa de Incautaciones de Drogas y Factores Sociales")
m = folium.Map(location=[-10, -70], zoom_start=4)

# Agregar puntos al mapa con información relevante
for _, row in gdf.iterrows():
    folium.Marker(
        location=[row["geometry"].y, row["geometry"].x],
        popup=f"{row['Departamento']} ({row['País']})\n"
              f"Incautaciones de drogas: {row.get('TOTAL DROGAS KG.', 'N/A')} kg\n"
              f"Analfabetismo (último año disponible): {row.get('2023', 'N/A')}%\n"
              f"Pobreza monetaria (último año disponible): {row.get('2023', 'N/A')}%\n"
              f"Población económicamente no activa (último año disponible): {row.get('2023', 'N/A')}%",
        tooltip=row["Departamento"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Mostrar el mapa en Streamlit
st_folium(m)

# Mostrar tabla con datos
st.header("Datos Consolidados")
st.dataframe(gdf.drop(columns=["geometry"]))

# Agregar fuentes de información
st.header("Fuentes de Información")
fuentes = [
    "[Insight Crime](https://insightcrime.org/es/noticias/dudas-historica-incautacion-cocaina-bolivia/)",
    "[Gobierno de Perú](https://www.gob.pe/institucion/mininter/noticias/1083462-record-historico-pnp-decomiso-mas-de-160-toneladas-de-droga-durante-el-ano-2024)",
    "[CNN Español](https://cnnespanol.cnn.com/2024/12/29/colombia/toneladas-cocaina-incautadas-colombia-anio-2024-efe)",
    "[Datos Colombia](https://www.datos.gov.co/Seguridad-y-Defensa/Reporte-Incautaci-n-de-Armas-de-Fuego-Polic-a-Naci/2iz5-9bbz/data?no_mobile=true)",
    "[Infobae Colombia](https://www.infobae.com/colombia/2024/06/11/representantes-de-estados-unidos-piden-rebajar-ayuda-antinarcoticos-para-colombia-recortarian-usd200000-millones-al-pais/)",
    "[SwissInfo](https://www.swissinfo.ch/spa/ecuador-decomis%C3%B3-294-toneladas-de-droga-en-2024%2C-seg%C3%BAn-la-polic%C3%ADa/88668009)",
    "[Ministerio del Interior Ecuador](https://www.ministeriodelinterior.gob.ec/en-nueve-meses-de-trabajo-coordinado-entre-policia-nacional-y-fuerzas-armadas-se-han-incautado-mas-de-307-toneladas-de-droga/#:~:text=Otro%20de%20los%20datos%20importantes,manera%20permanente%20a%20nivel%20nacional.)",
    "[Fuerza Aérea de Ecuador](https://www.fae.mil.ec/2024/09/17/fuerzas-armadas-del-ecuador-refuerzan-seguridad-con-decomiso-de-armas-y-municiones-en-operativos-camex/)",
    "[Primicias Ecuador](https://www.primicias.ec/seguridad/ecuador-frontera-norte-cultivos-coca-hectareas-real-81218/)"
]

for fuente in fuentes:
    st.markdown(f"- {fuente}")

import geopandas as gpd

gdf_path = "GeoDataFrame_Final.geojson"
gdf = gpd.read_file(gdf_path)

print(gdf.head())  # Debería mostrar las primeras filas del GeoDataFrame
