import pandas as pd
import numpy as np
import streamlit as st
import time

def get_style(df, subgenre, col2):
    style = st.selectbox(':musical_note: **Style**', ['Select a style']+list(df[df['subgenre']==subgenre]['style'].unique()))
    
    if style != 'Select a style': 
        year, artist, album, query, df_style = display_top_albums(df, subgenre, style)

        if st.button('Search'):
            st.dataframe(df_style)
            album_cover = show_album_cover(query)

            with col2: 
                st.image(album_cover, width=400)
                st.write(f'**{album}** by **{artist}** was the top {style} album of {year}')


def display_top_albums(df, subgenre, style):
        year = st.number_input(':watch: **Year**', min_value=df[df['style']==style]['year'].min(), max_value=2010, step=1)
        df_style = df[df['year']==year].query(f"style == '{style}'")[['artist', 'title', 'rating']]\
                        .sort_values('rating', ascending=False)\
                        .head()\
                        .reset_index(drop=True)
        df_style.index = range(1, len(df_style) + 1)

        if len(df_style)>0:
            artist = df_style.head(1)['artist'].values[0]
            album = df_style.head(1)['title'].values[0]
            query = artist + ' ' + album
            return year, artist, album, query, df_style
        else:
            st.write('Try another style or year')
            artist = ''
            album = ''
            query = artist + ' ' + album
            return year, artist, album, query, df_style


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


    

