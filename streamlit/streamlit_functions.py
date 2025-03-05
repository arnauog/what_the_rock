import pandas as pd
import numpy as np


def display_top_albums(df, style):
    import streamlit as st
    import time
    col1, col2 = st.columns([0.6, 0.4])
    roots_rock = ['Blues Rock', 'Country Rock', 'Folk Rock', 'Rock & Roll', 'Soft Rock', 'Southern Rock']

    if style is not 'All':
        year = st.number_input(':watch: **Year**', min_value=df[df['style']==style]['year'].min(), max_value=2010, step=1, key="year_input")
        df_style = df[df['year']==year].query(f"style == '{style}'")[['artist', 'title', 'rating']]\
                        .sort_values('rating', ascending=False)\
                        .head()\
                        .reset_index(drop=True)
        df_style.index = range(1, len(df_style) + 1)

    else:
        year = st.number_input(':watch: **Year**', min_value=1960, max_value=2010, step=1)
        df_style = df[df['year']==year].query(f"style.isin({roots_rock})")\
                    [['artist', 'title', 'rating']]\
                    .groupby(['artist', 'title']).agg('mean')\
                    .sort_values('rating', ascending=False)\
                    .head()\
                    .reset_index()
        df_style.index = range(1, len(df_style) + 1)

    # st.write('The top rated albums of that year are:')
    # if st.button('Search'):
    #     st.dataframe(df_style)

        artist = df_style.head(1)['artist'].values[0]
        album = df_style.head(1)['title'].values[0]
        query = artist + ' ' + album

        return artist, album, query


def show_album_cover(query):
    import requests 
    url = "https://api.discogs.com/database/search"
    headers = {"Authorization": "Discogs token=UwfqmsztxwnfABgQpmhaAsprbUgpOJKGOJSQAqfp"}

    # Define parameters for artist search
    params = {
        "per_page": 10    # Number of results per page (max 100)
        , 'type': 'release'
        , 'format': 'album'
        , 'genre': 'Rock'
        , 'query': query
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()['results']
    album_cover = data[0]['cover_image']
    return album_cover

    
def spoti_open(song_name):
    from dotenv import load_dotenv
    import os
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    import time
    import webbrowser

    load_dotenv()
    user = os.getenv('client_id')
    password = os.getenv('client_secret')

    #Initialize SpotiPy with user credentials
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = user,
                                                            client_secret = password))
    opensong = sp.search(q=song_name, limit=1)
    browser = opensong['tracks']['items'][0]['external_urls']['spotify']
    time.sleep(2)
    webbrowser.open(browser)

def create_folium_map(df, country, subgenre):
    import folium
    from folium import Map
    from folium.plugins import HeatMap

    df = pd.read_csv('Datasets/df_country.csv')

    uk_lat = 53.909290891215214
    uk_lon = -2.1608240239505117 
    us_lat = 38.09612098863635 
    us_lon = -96.48185032372986 

    maps = {f"United Kingdom": Map(location=[uk_lat, uk_lon], zoom_start=6),  # Example coordinates
            "United States": Map(location=[us_lat, us_lon], zoom_start=5)}

    # Select the correct DataFrame
    df = df[df['country']==country]
    
    # create the subset of the subgenre
    subset_df = df[df['subgenre'] == subgenre]

    # create the FeatureGroup
    subset_df_group = folium.FeatureGroup(name = f'{subgenre}: {subset_df.shape[0]}') 

    # the subset is the subgenre and we i només ens interessen 2 columnes: les coordenades
    HeatMap(data = subset_df[['latitude', 'longitude']]).add_to(subset_df_group) 

    # Add the FeatureGroup to the correct map
    maps[country].add_child(subset_df_group)


    

