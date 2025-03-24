import streamlit as st
from streamlit_functions import *
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import webbrowser


df_ratings = pd.read_csv('Datasets/df_ratings.csv')
df_ratings["year"] = df_ratings["year"].astype(str)
df = pd.read_csv('Datasets/df_artists_bandcamp_concat.csv') 
st.title("Buy an album in Bandcamp")
st.write("But we are not rich, are we? So we want to make the most of our money...")
st.write("Let's search for the cheapest albums in terms of price per minute.")

col1, col2 = st.columns([0.6, 0.4])
with col1:
    artist = st.selectbox(':musical_note: **Artist**', ['Select an artist']+list(df["artist"].unique()))

    if artist != 'Select an artist':
        st.write("Looking for the albums in Bandcamp... Please wait.")
        df_bandcamp = bandcamp_albums(artist)
        artist_clean = artist.lower().replace(' ', '')
        url = f'https://{artist_clean}.bandcamp.com/music'

        st.divider()
        st.write(f'The cheapest albums of {artist} are:')
        st.dataframe(df_bandcamp)

        album = df_bandcamp.head(1)['title'].values[0]
        year = df_bandcamp.head(1)['year'].values[0]
        query = artist + ' ' + album

        album_cover = show_album_cover(query)
        with col2: 
            time.sleep(1)
            st.image(album_cover, width=400)
            st.write(f'**{album}**, from {year} is the **{artist}** album with the lowest price per minute')

            time.sleep(1)
            st.link_button("Visit the artist's Bandcamp website", url)
