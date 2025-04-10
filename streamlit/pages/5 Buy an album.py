import streamlit as st
from streamlit_functions import *
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import webbrowser

url = "https://drive.google.com/uc?export=download&id=1x4Owf2IgtkwDfopMyYOWuDfzPxXrBf_g"
df = pd.read_csv(url) 
st.title("Buy an album in Bandcamp")
st.write("But we are not rich, are we? So we want to make the most of our money...")
st.write("Let's search for the cheapest albums in terms of price per minute.")

st.markdown("""<style>
    div[data-baseweb="select"] {
        width: 400px !important;  /* Adjust width as needed */}
    </style>
    """,
    unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.6, 0.3, 0.1])
with col1:
    artist = st.selectbox(':musical_note: **Artist**', ['Select an artist']+list(df["artist"].unique()))

    if artist != 'Select an artist':
        st.write(f"Looking for the albums of {artist} in Bandcamp... Please wait.")
        df_bandcamp = bandcamp_albums(artist)
        time.sleep(1)
        df_bandcamp.index = range(1, len(df_bandcamp) + 1)
        artist_clean = artist.lower().replace(' ', '')
        url_artist = f'https://{artist_clean}.bandcamp.com/music'

        st.divider()

        if len(df_bandcamp) > 0:
            st.write(f'The cheapest albums of {artist} are:')
            st.dataframe(df_bandcamp)

                # get the album cover of the cheapest album for the bandcamp website
            album = df_bandcamp.head(1)['title'].values[0]
            title_changed = (
                album.replace('(', '')
                    .replace(')', '')
                    .replace('[', '')
                    .replace(']', '')
                    .replace('/', ' ')
                    .replace("'", '')
                    .replace('"', '')
                    .replace('& ', '')
                    .replace('feat.', 'feat')
                    .replace(',', '')
                    .replace(' - ', '-') 
                    .replace(' ', '-')
                    .lower()
            )
            year = df_bandcamp.head(1)['year'].values[0]
            try:
                url = f'https://{artist_clean}.bandcamp.com/album/{title_changed}'
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                album_cover = soup.select('#tralbumArt > a > img')[0]['src']

                with col2: 
                    time.sleep(1)
                    st.image(album_cover, width=400)
                    st.write(f'**{album}**, from {year} is the **{artist}** album with the lowest price per minute')

                    time.sleep(1)
                    st.link_button("Visit the artist's Bandcamp website", url_artist)
            except:
                try:
                    url = f'https://{artist_clean}.bandcamp.com/music'
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, "html.parser")
                    album_cover = soup.select('#tralbumArt > a > img')[0]['src']

                    with col2: 
                        time.sleep(1)
                        st.image(album_cover, width=400)
                        st.write(f'**{album}**, from {year} is the **{artist}** album with the lowest price per minute')

                        time.sleep(1)
                        st.link_button("Visit the artist's Bandcamp website", url_artist)   
                except: 
                    st.write(f'**{album}**, from {year} is the **{artist}** album with the lowest price per minute')

                    time.sleep(1)
                    st.link_button("Visit the artist's Bandcamp website", url_artist)
        else:
            st.write(f"Sorry, we couldn't find any albums from {artist}")