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

# Cargar los datos normalizados
def load_data():
    file_path = "Datos_Normalizados.csv"  # Reemplazar con la ruta correcta
    return pd.read_csv(file_path)

df = load_data()

df.fillna(0, inplace=True)

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
    }
    
    df_info = pd.DataFrame(data)
    st.dataframe(df_info)

# Mapa de Drogas
elif page == "Mapa de Drogas":
    variable = st.sidebar.selectbox(
        "Seleccione la variable a visualizar:",
        ["Cocaína (kg)", "Marihuana (kg)", "Base de Coca (kg)", "Sustancias Químicas Sólidas (kg)", "Sustancias Químicas Líquidas (L)"]
    )
    
    m = folium.Map(location=[-10, -70], zoom_start=4)
    heat_data = df[["Latitud", "Longitud", variable]].dropna().values.tolist()
    HeatMap(heat_data).add_to(m)
    
    st.markdown(f"### Mapa de Calor - {variable}")
    folium_static(m)

# Mapa de Armas
elif page == "Mapa de Armas":
    m = folium.Map(location=[-10, -70], zoom_start=4)
    heat_data = df[["Latitud", "Longitud", "Armas Incautadas"]].dropna().values.tolist()
    HeatMap(heat_data).add_to(m)
    
    st.markdown("### Mapa de Calor - Armas Incautadas")
    folium_static(m)

