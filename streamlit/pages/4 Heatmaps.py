import streamlit as st
from streamlit_functions import *
import streamlit.components.v1 as components

import numpy as np
import pandas as pd

import folium
from folium import Map
from folium.plugins import HeatMap

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title='What the Rock?', page_icon=':guitar:', layout='wide')

df_ratings = pd.read_csv('Datasets/df_ratings.csv')
df = pd.read_csv('Datasets/df_final.csv')
data = pd.read_csv('Datasets/df_country.csv')

st.header('Geographical distribution of rock music')

uk_lat = 53.909290891215214
uk_lon = -2.1608240239505117 
us_lat = 38.09612098863635 
us_lon = -96.48185032372986 

maps = {f"United Kingdom": Map(location=[uk_lat, uk_lon], zoom_start=6), 
        "United States": Map(location=[us_lat, us_lon], zoom_start=4)}
subgenres = list(df["subgenre"].unique())
decades = [1960, 1970, 1980, 1990, 2000]


def create_folium_map_subgenres(df, country, subgenre, folium_map):
    df = df[df['country']==country]  # Select the correct subset
    
    # create the subset of the subsubgenre
    subset_df = df[df['subgenre'] == subgenre]

    # create the FeatureGroup
    subset_subgenres_group = folium.FeatureGroup(name = f'{subgenre}: {subset_df.shape[0]}') 

    # the subset is the subgenre and we are only interested in 2 columns: the coordinates
    HeatMap(data = subset_df[['latitude', 'longitude']]).add_to(subset_subgenres_group) 

    # Add the FeatureGroup to the correct map
    folium_map.add_child(subset_subgenres_group)


def create_folium_map_decades(df, country, decade, folium_map):
    df = df[df['country']==country]  # Select the correct subset
    
    # create the subset of the subsubgenre
    subset_df = df[(df['year']>decade) & (df['year']<decade+10)]

    # create the FeatureGroup
    subset_decades_group = folium.FeatureGroup(name = f'{decade}: {subset_df.shape[0]}') 

    # the subset is the decade and we are only interested in 2 columns: the coordinates
    HeatMap(data = subset_df[['latitude', 'longitude']]).add_to(subset_decades_group) 

    # Add the FeatureGroup to the correct map
    folium_map.add_child(subset_decades_group)


col1, col2 = st.columns([0.15, 0.85])

with col1:
    country = st.radio(' ', [':world_map: Select a country', 'United Kingdom', 'United States'])

    if country == 'United Kingdom':
        feature = st.radio(' ', [':mag: Select a feature', 'Decades', 'Subgenres'])

        if feature == 'Decades':
            uk_map_decades = Map(location=[uk_lat, uk_lon], zoom_start=6)
            for decade in decades:
                create_folium_map_decades(data, "United Kingdom", decade, uk_map_decades)
            folium.LayerControl(collapsed=False, position="topleft").add_to(uk_map_decades)
                
            # Save map to HTML
            uk_map_decades.save("map_uk_decades.html")

        elif feature == 'Subgenres':
            uk_map_subgenres = Map(location=[uk_lat, uk_lon], zoom_start=6)
            for subgenre in subgenres:
                create_folium_map_subgenres(data, "United Kingdom", subgenre, uk_map_subgenres)
            folium.LayerControl(collapsed=False, position="topleft").add_to(uk_map_subgenres)
            
            # Save map to HTML
            uk_map_subgenres.save("map_uk_subgenres.html")

    elif country == 'United States':
        feature = st.radio(' ', [':mag: Select a feature', 'Decades', 'Subgenres'])

        if feature == 'Decades':
            us_map_decades = Map(location=[us_lat, us_lon], zoom_start=4)
            for decade in decades:
                create_folium_map_decades(data, "United States", decade, us_map_decades)
            folium.LayerControl(collapsed=False, position="topleft").add_to(us_map_decades)
                
            # Save map to HTML
            us_map_decades.save("map_us_decades.html")

        elif feature == 'Subgenres':
            us_map_subgenres = Map(location=[us_lat, us_lon], zoom_start=4)
            for subgenre in subgenres:
                create_folium_map_subgenres(data, "United States", subgenre, us_map_subgenres)
            folium.LayerControl(collapsed=False, position="topleft").add_to(us_map_subgenres)
            
            # Save map to HTML
            us_map_subgenres.save("map_us_subgenres.html")

# Display maps in Streamlit using the HTML files
with col2:
        if country == 'United Kingdom':
            if feature == 'Decades':
                st.components.v1.html(open("map_uk_decades.html", "r").read(), height=600)
            elif feature == 'Subgenres':
                st.components.v1.html(open("map_uk_subgenres.html", "r").read(), height=600)
        
        elif country == 'United States': 
            if feature == 'Decades':
                st.components.v1.html(open("map_us_decades.html", "r").read(), height=600)
            elif feature == 'Subgenres':
                st.components.v1.html(open("map_us_subgenres.html", "r").read(), height=600)

