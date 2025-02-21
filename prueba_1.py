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
from folium import FeatureGroup

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

# Standardize column names
df_peru.rename(columns={'Droga Decomisada (kg)': 'Drogas', 'Latitud': 'lat', 'Longitud': 'lon'}, inplace=True)
df_colombia.rename(columns={'CANTIDAD_DROGA': 'Drogas', 'LATITUD': 'lat', 'LONGITUD': 'lon'}, inplace=True)
df_ecuador.rename(columns={'TOTAL_DROGAS_KG.': 'Drogas', 'LATITUD': 'lat', 'LONGITUD': 'lon'}, inplace=True)
df_bolivia.rename(columns={'Cocaína (ton)': 'Drogas', 'Latitud': 'lat', 'Longitud': 'lon'}, inplace=True)

# Ensure required columns exist
def ensure_columns(df, required_columns):
    for col in required_columns:
        if col not in df.columns:
            df[col] = pd.NA

required_columns = ['lat', 'lon', 'Drogas', 'Año']
ensure_columns(df_peru, required_columns)
ensure_columns(df_colombia, required_columns)
ensure_columns(df_ecuador, required_columns)
ensure_columns(df_bolivia, required_columns)

# Convert columns to numeric and remove invalid data
def clean_data(df):
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    df['Drogas'] = pd.to_numeric(df['Drogas'], errors='coerce')
    df['Año'] = pd.to_numeric(df['Año'], errors='coerce')
    return df.dropna(subset=['lat', 'lon', 'Drogas', 'Año'])

df_peru = clean_data(df_peru)
df_colombia = clean_data(df_colombia)
df_ecuador = clean_data(df_ecuador)
df_bolivia = clean_data(df_bolivia)

drug_data = pd.concat([df_peru, df_colombia, df_ecuador, df_bolivia])

drug_data.dropna(inplace=True)

drug_map = folium.Map(location=[-10, -75], zoom_start=4)

years = sorted(drug_data['Año'].unique())
for year in years:
    year_layer = FeatureGroup(name=str(year))
    data_year = drug_data[drug_data['Año'] == year]
    HeatMap(data=data_year[['lat', 'lon', 'Drogas']].values, radius=15).add_to(year_layer)
    drug_map.add_child(year_layer)

drug_map.add_child(folium.LayerControl())

st.title("Mapa de Calor: Drogas Decomisadas por Año")
folium_static(drug_map)
