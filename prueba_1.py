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

# Load the data
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

# Print column names for debugging
print("Perú Columns:", df_peru.columns)
print("Colombia Columns:", df_colombia.columns)
print("Ecuador Columns:", df_ecuador.columns)
print("Bolivia Columns:", df_bolivia.columns)

# Standardize columns
df_peru.rename(columns={'Droga Decomisada (kg)': 'Drogas'}, inplace=True)
df_colombia.rename(columns={'CANTIDAD_DROGA': 'Drogas'}, inplace=True)
df_ecuador.rename(columns={'TOTAL_DROGAS_KG.': 'Drogas'}, inplace=True)
df_bolivia.rename(columns={'Cocaína (ton)': 'Drogas'}, inplace=True)

# Check if 'Drogas' column exists
for df, name in zip([df_peru, df_colombia, df_ecuador, df_bolivia], 
                     ["Perú", "Colombia", "Ecuador", "Bolivia"]):
    if 'Drogas' not in df.columns:
        print(f"⚠️ Advertencia: La columna 'Drogas' no está en {name}")

# Convert to numeric
df_ecuador['Drogas'] = pd.to_numeric(df_ecuador['Drogas'], errors='coerce')

drug_data = pd.concat([df_peru[['lat', 'lon', 'Drogas']], df_colombia[['lat', 'lon', 'Drogas']], df_ecuador[['lat', 'lon', 'Drogas']], df_bolivia[['lat', 'lon', 'Drogas']]])

drug_data.dropna(inplace=True)

# Map for drugs
st.title("Mapa de Calor: Drogas Decomisadas")
drug_map = folium.Map(location=[-10, -75], zoom_start=4)
HeatMap(data=drug_data[['lat', 'lon', 'Drogas']].values, radius=15).add_to(drug_map)
folium_static(drug_map)

# Map for weapons
df_colombia.rename(columns={'CANTIDAD_ARMAS': 'Armas'}, inplace=True)
weapons_data = df_colombia[['lat', 'lon', 'Armas']].dropna()

st.title("Mapa de Calor: Armas Incautadas")
weapon_map = folium.Map(location=[-10, -75], zoom_start=4)
HeatMap(data=weapons_data[['lat', 'lon', 'Armas']].values, radius=15).add_to(weapon_map)
folium_static(weapon_map)

