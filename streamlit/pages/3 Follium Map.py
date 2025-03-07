import streamlit as st
from streamlit_functions import *
import streamlit.components.v1 as components

import numpy as np
import pandas as pd
import random

import folium
from folium import Marker, Icon, Map
from folium.plugins import HeatMap


# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title='What the Rock?', page_icon=':guitar:', layout='wide')

df = pd.read_csv('Datasets/df_test.csv')

st.header('Geographical distribution of the genres')
data = pd.read_csv('Datasets/df_country.csv')

uk_lat = 53.909290891215214
uk_lon = -2.1608240239505117 
us_lat = 38.09612098863635 
us_lon = -96.48185032372986 

maps = {f"United Kingdom": Map(location=[uk_lat, uk_lon], zoom_start=6),  # Example coordinates
        "United States": Map(location=[us_lat, us_lon], zoom_start=4)}

def create_folium_map(df, country, subgenre):
    df = df[df['country']==country]  # Select the correct DataFrame
    
    # create the subset of the subsubgenre
    subset_df = df[df['subgenre'] == subgenre]

    # create the FeatureGroup
    subset_df_group = folium.FeatureGroup(name = f'{subgenre}: {subset_df.shape[0]}') 

    # the subset is the subsubgenre and we i només ens interessen 2 columnes: les coordenades
    HeatMap(data = subset_df[['latitude', 'longitude']]).add_to(subset_df_group) 

    # Add the FeatureGroup to the correct map
    maps[country].add_child(subset_df_group)

country = st.radio(' ', ['Select a country', 'United Kingdom', 'United States'])

if country == 'United Kingdom':
    create_folium_map(data, "United Kingdom", "roots")
    create_folium_map(data, "United Kingdom", "classic")
    create_folium_map(data, "United Kingdom", "metal")
    create_folium_map(data, "United Kingdom", "punk")
    create_folium_map(data, "United Kingdom", "indie")
    folium.LayerControl(collapsed=False, position="topleft").add_to(maps['United Kingdom'])
    
    # Save map to HTML
    maps['United Kingdom'].save("map_uk.html")

    # Display map in Streamlit using the HTML file
    st.components.v1.html(open("map_uk.html", "r").read(), height=600)

elif country == 'United States':
    create_folium_map(data, "United States", "roots")
    create_folium_map(data, "United States", "classic")
    create_folium_map(data, "United States", "metal")
    create_folium_map(data, "United States", "punk")
    create_folium_map(data, "United States", "indie")
    folium.LayerControl(collapsed=False, position="topleft").add_to(maps['United States'])
    
    # Save map to HTML
    maps['United States'].save("map_us.html")

    # Display map in Streamlit using the HTML file
    st.components.v1.html(open("map_us.html", "r").read(), height=600)

