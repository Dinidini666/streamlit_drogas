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

# Standardize column names
df_peru.rename(columns={'Droga Decomisada (kg)': 'Drogas', 'Latitud': 'lat', 'Longitud': 'lon'}, inplace=True)
df_colombia.rename(columns={'CANTIDAD_DROGA': 'Drogas', 'LATITUD': 'lat', 'LONGITUD': 'lon'}, inplace=True)
df_ecuador.rename(columns={'TOTAL_DROGAS_KG.': 'Drogas', 'LATITUD': 'lat', 'LONGITUD': 'lon'}, inplace=True)
df_bolivia.rename(columns={'Cocaína (ton)': 'Drogas', 'Latitud': 'lat', 'Longitud': 'lon'}, inplace=True)

# Ensure all required columns exist
def ensure_columns(df, required_columns):
    for col in required_columns:
        if col not in df.columns:
            df[col] = pd.NA  # Fill missing columns with NaN
            print(f"⚠️ Advertencia: Se creó la columna faltante '{col}' en el DataFrame")

required_columns = ['lat', 'lon', 'Drogas']
ensure_columns(df_peru, required_columns)
ensure_columns(df_colombia, required_columns)
ensure_columns(df_ecuador, required_columns)
ensure_columns(df_bolivia, required_columns)

# Convert columns to numeric and remove invalid data
def clean_data(df):
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    df['Drogas'] = pd.to_numeric(df['Drogas'], errors='coerce')
    return df.dropna(subset=['lat', 'lon', 'Drogas'])

df_peru = clean_data(df_peru)
df_colombia = clean_data(df_colombia)
df_ecuador = clean_data(df_ecuador)
df_bolivia = clean_data(df_bolivia)

# Merge data
drug_data = pd.concat([df_peru[['lat', 'lon', 'Drogas']], df_colombia[['lat', 'lon', 'Drogas']], df_ecuador[['lat', 'lon', 'Drogas']], df_bolivia[['lat', 'lon', 'Drogas']]])

drug_data.dropna(inplace=True)

# Map for drugs
st.title("Mapa de Calor: Drogas Decomisadas")
drug_map = folium.Map(location=[-10, -75], zoom_start=4)
HeatMap(data=drug_data[['lat', 'lon', 'Drogas']].values, radius=15).add_to(drug_map)
folium_static(drug_map)

# Map for weapons
df_colombia.rename(columns={'CANTIDAD_ARMAS': 'Armas'}, inplace=True)
weapons_data = df_colombia[['lat', 'lon', 'Armas']].dropna(subset=['lat', 'lon', 'Armas'])

st.title("Mapa de Calor: Armas Incautadas")
weapon_map = folium.Map(location=[-10, -75], zoom_start=4)
HeatMap(data=weapons_data[['lat', 'lon', 'Armas']].values, radius=15).add_to(weapon_map)
folium_static(weapon_map)
