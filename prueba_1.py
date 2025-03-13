import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns

# Introducción y navegación
st.title("Mapa de Calor: Tráfico Ilícito de Drogas y Armas en la Comunidad Andina")

st.markdown("""
## Introducción
Este dashboard muestra un análisis geoespacial sobre la incautación de drogas y armas en la Comunidad Andina desde el año 2019. 
Los datos provienen de fuentes oficiales y están en constante actualización. En futuras versiones, se implementará la opción de visualizar los datos por año.

La base de datos utilizada es pública; sin embargo, este trabajo implicó un proceso de selección, limpieza y organización de los datos más relevantes, 
de manera que puedan ser utilizados eficazmente por los países de la región para la toma de decisiones.

Utilice los botones a continuación para navegar entre los mapas de calor.
""")

# Sidebar para navegación
page = st.radio("Seleccione una sección:", ["Información General", "Mapa de Drogas", "Mapa de Armas", 'Mapa de Homicidios', "Línea de Tiempo Tráfico vs Homicidios", "Gráfico de línea"])

# Cargar datos de homicidios
@st.cache_data
def load_homicide_data():
    file_path = "homicidios_data.csv"  
    return pd.read_csv(file_path)

df_homicidios = load_homicide_data()

# Cargar los datos normalizados
def load_data():
    file_path = "Datos_Normalizados_v1.csv"  
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

# Línea de Tiempo: Tráfico Ilícito vs Homicidios
if page == "Línea de Tiempo Tráfico vs Homicidios":

    # Limpiar datos
    df.fillna(0, inplace=True)
    df_homicidios.fillna(0, inplace=True)
    
    # Normalizar nombres de países (Perú vs Peru)
    df['País'] = df['País'].replace({'Peru': 'Perú'})
    df_homicidios['País'] = df_homicidios['País'].replace({'Peru': 'Perú'})
    
    # Convertir la columna 'Año' a tipo int
    df['Año'] = df['Año'].astype(int)
    df_homicidios['Año'] = df_homicidios['Año'].astype(int)
    
    # Obtener el rango de años disponibles
    años_disponibles = sorted(df['Año'].unique())
    
    # Crear un slider para seleccionar el año
    año_seleccionado = st.slider(
        "Seleccione el año",
        min_value=min(años_disponibles),
        max_value=max(años_disponibles),
        value=min(años_disponibles)
    )
    
   # Obtener la lista de países disponibles
    paises_disponibles = df['País'].unique()
    
    # Crear un select box para seleccionar el país
    pais_seleccionado = st.selectbox("Seleccione un país", paises_disponibles)
    
    # Filtrar datos por el año y país seleccionado
    df_año_pais = df[(df['Año'] == año_seleccionado) & (df['País'] == pais_seleccionado)]
    df_homicidios_año_pais = df_homicidios[(df_homicidios['Año'] == año_seleccionado) & (df_homicidios['País'] == pais_seleccionado)]
    
    # Combinar los datos de incautaciones y homicidios para el año y país seleccionado
    df_combined = pd.merge(df_año_pais, df_homicidios_año_pais, on=['País', 'Año', 'Ubicación'], how='outer')
    
    # Mostrar los datos en una tabla
    st.write(f"Datos para el año {año_seleccionado} en {pais_seleccionado}:")
    st.dataframe(df_combined)
    
    # Crear un gráfico de barras para las incautaciones de drogas por región/departamento
    st.write(f"Incautaciones de drogas por región/departamento en {pais_seleccionado} ({año_seleccionado}):")
    fig, ax = plt.subplots(figsize=(10, 6))
    df_combined.set_index('Ubicación')[['Cocaína (kg)', 'Marihuana (kg)']].plot(kind='bar', ax=ax)
    ax.set_ylabel('Cantidad (kg)')
    ax.set_title(f'Incautaciones de drogas por región/departamento en {pais_seleccionado} ({año_seleccionado})')
    plt.xticks(rotation=45, ha='right')  # Rotar los nombres de las regiones para mejor legibilidad
    st.pyplot(fig)
    
    # Crear un gráfico de barras para la tasa de homicidios por región/departamento
    st.write(f"Tasa de homicidios por región/departamento en {pais_seleccionado} ({año_seleccionado}):")
    fig, ax = plt.subplots(figsize=(10, 6))
    df_combined.set_index('Ubicación')['Tasa de Homicidios'].plot(kind='bar', color='red', ax=ax)
    ax.set_ylabel('Tasa de homicidios (por 100,000 hab.)')
    ax.set_title(f'Tasa de homicidios por región/departamento en {pais_seleccionado} ({año_seleccionado})')
    plt.xticks(rotation=45, ha='right')  # Rotar los nombres de las regiones para mejor legibilidad
    st.pyplot(fig)

# Gráfico de línea
if page == "Gráfico de línea":

    # Limpiar datos
    df.fillna(0, inplace=True)
    df_homicidios.fillna(0, inplace=True)
    
    # Normalizar nombres de países (Perú vs Peru)
    df['País'] = df['País'].replace({'Peru': 'Perú'})
    df_homicidios['País'] = df_homicidios['País'].replace({'Peru': 'Perú'})
    
    # Convertir la columna 'Año' a tipo int
    df['Año'] = df['Año'].astype(int)
    df_homicidios['Año'] = df_homicidios['Año'].astype(int)
    
    # Obtener la lista de países disponibles
    paises_disponibles = df['País'].unique()
    
    # Seleccionar país desde un menú desplegable
    pais_seleccionado = st.selectbox("Seleccione un país", paises_disponibles)
    
    # Filtrar datos por país seleccionado
    df_pais = df[df['País'] == pais_seleccionado]
    df_homicidios_pais = df_homicidios[df_homicidios['País'] == pais_seleccionado]
    
    # Agrupar los datos por año para el país seleccionado
    df_pais_grouped = df_pais.groupby('Año').sum().reset_index()
    df_homicidios_pais_grouped = df_homicidios_pais.groupby('Año').sum().reset_index()
    
    # Combinar los datos de incautaciones y homicidios
    df_combined = pd.merge(df_pais_grouped, df_homicidios_pais_grouped, on='Año', how='outer')
    
    # Crear el gráfico con dos ejes Y
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Gráfico de incautaciones de drogas (eje Y izquierdo)
    color = 'tab:blue'
    ax1.set_xlabel('Año')
    ax1.set_ylabel('Incautaciones (kg)', color=color)
    ax1.plot(df_combined['Año'], df_combined['Cocaína (kg)'], color=color, label='Cocaína (kg)')
    ax1.plot(df_combined['Año'], df_combined['Marihuana (kg)'], color='tab:green', label='Marihuana (kg)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Crear un segundo eje Y para la tasa de homicidios
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Tasa de Homicidios (por 100,000 hab.)', color=color)
    ax2.plot(df_combined['Año'], df_combined['Tasa de Homicidios'], color=color, label='Tasa de Homicidios')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Añadir título y leyenda
    plt.title(f'Comparación de Incautaciones y Tasa de Homicidios en {pais_seleccionado}')
    fig.tight_layout()
    
    # Mostrar la leyenda
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    
# Función para agregar leyenda
def add_legend(map_object):
    legend_html = '''
     <div style="position: fixed; 
                 bottom: 20px; left: 20px; width: 250px; height: 140px; 
                 background-color: white; z-index:9999; font-size:14px;
                 border:2px solid grey; padding: 10px; opacity: 0.9;">
     <b> Leyenda del Mapa de Calor </b><br>
     <i style="background: blue; width: 15px; height: 15px; display: inline-block;"></i> Baja Intensidad <br>
     <i style="background: green; width: 15px; height: 15px; display: inline-block;"></i> Media Intensidad <br>
     <i style="background: yellow; width: 15px; height: 15px; display: inline-block;"></i> Alta Intensidad <br>
     <i style="background: red; width: 15px; height: 15px; display: inline-block;"></i> Muy Alta Intensidad <br>
     </div>
     '''
    map_object.get_root().html.add_child(folium.Element(legend_html))

# Mapa de Drogas
if page == "Mapa de Drogas":
    variable = st.sidebar.selectbox(
        "Seleccione la variable a visualizar:",
        ["Cocaína (kg)", "Marihuana (kg)", "Base de Coca (kg)", "Sustancias Químicas Sólidas (kg)", "Sustancias Químicas Líquidas (L)"]
    )
    
    m = folium.Map(location=[-10, -70], zoom_start=4, tiles='https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri World Imagery', name='Esri Satellite')

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["Latitud"], row["Longitud"]],
            radius=1.5,
            color='purple',
            fill=True,
            fill_color='purple',
            fill_opacity=0.08,
            popup=f"Ubicación: {row['Ubicación']}<br>{variable}: {row[variable]}",
        ).add_to(m)
        
    heat_data = df[["Latitud", "Longitud", variable]].dropna().values.tolist()
    HeatMap(heat_data).add_to(m)

    add_legend(m)
    
    st.markdown(f"### Mapa de Calor - {variable}")
    folium_static(m)

# Mapa de Armas
if page == "Mapa de Armas":
    m = folium.Map(location=[-10, -70], zoom_start=4, tiles='https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri World Imagery', name='Esri Satellite')

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["Latitud"], row["Longitud"]],
            radius=1.5,
            color="purple",
            fill=True,
            fill_color="purple",
            fill_opacity=0.08,
            popup=f"Ubicación: {row['Ubicación']}<br>Armas Incautadas: {row['Armas Incautadas']}",
        ).add_to(m)
        
    heat_data = df[["Latitud", "Longitud", "Armas Incautadas"]].dropna().values.tolist()
    HeatMap(heat_data).add_to(m)

    add_legend(m)
    
    st.markdown("### Mapa de Calor - Armas Incautadas")
    folium_static(m)
    
# Mapa de Homicidios
if page == "Mapa de Homicidios":
    # Agregar opción "Todos los países"
    paises_disponibles = ["Todos los países"] + sorted(df_homicidios["País"].unique())
    pais_seleccionado = st.sidebar.selectbox("Seleccione el país", paises_disponibles)

    # Filtrar por país (si no es "Todos los países")
    if pais_seleccionado == "Todos los países":
        df_pais = df_homicidios
    else:
        df_pais = df_homicidios[df_homicidios["País"] == pais_seleccionado]

    # Seleccionar el año disponible dentro del país o todos los países
    año_seleccionado = st.sidebar.selectbox("Seleccione el año", sorted(df_pais["Año"].dropna().unique(), reverse=True))

    # Filtrar por el año seleccionado
    df_filtrado = df_pais[df_pais["Año"] == año_seleccionado].dropna(subset=["Latitud", "Longitud"])

    m = folium.Map(location=[-10, -70], zoom_start=4, tiles="cartodb positron")

    # Agregar puntos individuales (solo los que tienen coordenadas válidas)
    for _, row in df_filtrado.iterrows():
        folium.CircleMarker(
            location=[row["Latitud"], row["Longitud"]],
            radius=1.5,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
            popup=f"<b>País:</b> {row['País']}<br>"
                  f"<b>Departamento:</b> {row['Departamento']}<br>"
                  f"<b>Tasa de Homicidios:</b> {row['Tasa de Homicidios']} por 100,000 habitantes",
        ).add_to(m)

    # Crear capa de calor
    heat_data = df_filtrado[["Latitud", "Longitud", "Tasa de Homicidios"]].dropna().values.tolist()
    HeatMap(heat_data, radius=15).add_to(m)

    st.markdown(f"### Mapa de Calor - Tasa de Homicidios ({año_seleccionado}, {pais_seleccionado})")
    st.markdown("Tasa de homicidios por cada 100,000 habitantes.")
    folium_static(m)
