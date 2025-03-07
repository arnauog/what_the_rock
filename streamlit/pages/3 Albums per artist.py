import streamlit as st
from streamlit_functions import *
import pandas as pd
import numpy as np

df_ratings = pd.read_csv('Datasets/df_ratings.csv')
df = df_ratings.groupby('artist').filter(lambda x: len(x)>10).sort_values('artist')
st.title('Search for albums of your favourite artist')

col1, col2 = st.columns([0.6, 0.4])

st.markdown("""<style>
    div[data-baseweb="select"] {
        width: 400px !important;  /* Adjust width as needed */}
    </style>
    """,
    unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
with col1:
    artist = st.selectbox(':musical_note: **Subgenre**', ['Select an artist']+list(df["artist"].unique()))

    if artist != 'Select an artist':
        album_kind = st.radio(':mag: **Search for an album**', ['Top rated', 'Worst rated', 'Most popular', 'First'
                                                                , 'Longest', 'With the shortest songs'])

        if album_kind == 'Top rated':
            df_subset = df[df['artist']==artist][['artist', 'title', 'rating', 'votes', 'year']]\
                            .sort_values('rating', ascending=False)\
                            .head()\
                            .reset_index(drop=True)
            df_subset.index = range(1, len(df_subset) + 1)

            album = df_subset.head(1)['title'].values[0]
            year = df_subset.head(1)['year'].values[0]
            rating = df_subset.head(1)['rating'].values[0]
            votes = df_subset.head(1)['votes'].values[0]
            query = artist + ' ' + album

            album_cover = show_album_cover(query)
            with col2:
                time.sleep(1)
                st.image(album_cover, width=400)
                st.write(f'**{album}**, from **{year}**, is the best rated album of **{artist}** with a rating of **{rating}** and **{votes} votes**')
        

        elif album_kind == 'Worst rated':
            df_subset = df[df['artist']==artist][['artist', 'title', 'rating', 'votes', 'year']]\
                            .sort_values('rating')\
                            .head()\
                            .reset_index(drop=True)
            df_subset.index = range(1, len(df_subset) + 1)

            album = df_subset.head(1)['title'].values[0]
            year = df_subset.head(1)['year'].values[0]
            rating = df_subset.head(1)['rating'].values[0]
            votes = df_subset.head(1)['votes'].values[0]
            query = artist + ' ' + album


            album_cover = show_album_cover(query)
            with col2: 
                time.sleep(1)
                st.image(album_cover, width=400)
                st.write(f'**{album}**, from **{year}**, is the worst rated album of **{artist}** with a rating of **{rating}** and **{votes} votes**')


        elif album_kind == 'Most popular':
            df_subset = df[df['artist']==artist][['artist', 'title', 'votes', 'year']]\
                            .sort_values('votes', ascending=False)\
                            .head()\
                            .reset_index(drop=True)
            df_subset.index = range(1, len(df_subset) + 1)

            album = df_subset.head(1)['title'].values[0]
            year = df_subset.head(1)['year'].values[0]
            votes = df_subset.head(1)['votes'].values[0]
            query = artist + ' ' + album

            album_cover = show_album_cover(query)
            with col2: 
                time.sleep(1)
                st.image(album_cover, width=400)
                st.write(f'**{album}**, from **{year}**, is the most popular album of **{artist}** with **{votes} votes**')


        elif album_kind == 'First':
            df_subset = df[df['artist']==artist][['artist', 'title', 'year']]\
                            .sort_values('year')\
                            .head()\
                            .reset_index(drop=True)
            df_subset.index = range(1, len(df_subset) + 1)

            album = df_subset.head(1)['title'].values[0]
            year = df_subset.head(1)['year'].values[0]
            query = artist + ' ' + album

            album_cover = show_album_cover(query)
            with col2: 
                time.sleep(1)
                st.image(album_cover, width=400)
                st.write(f'**{album}**, released in **{year}**, is the debut album of **{artist}**')


        elif album_kind == 'Longest':
            df_subset = df[df['artist']==artist][['artist', 'title', 'album_length', 'year']]\
                            .sort_values('album_length', ascending=False)\
                            .head()\
                            .reset_index(drop=True)
            df_subset.index = range(1, len(df_subset) + 1)

            album = df_subset.head(1)['title'].values[0]
            year = df_subset.head(1)['year'].values[0]
            album_length = df_subset.head(1)['album_length'].values[0]
            query = artist + ' ' + album

            album_cover = show_album_cover(query)
            with col2: 
                time.sleep(1)
                st.image(album_cover, width=400)
                st.write(f'**{album}**, from **{year}**, is the longest album of **{artist}** with a duration of **{album_length}** minutes')


        elif album_kind == 'With the shortest songs':
            df_subset = df[df['artist']==artist][['artist', 'title', 'avg_song_length', 'year']]\
                            .sort_values('avg_song_length')\
                            .head()\
                            .reset_index(drop=True)
            df_subset.index = range(1, len(df_subset) + 1)

            album = df_subset.head(1)['title'].values[0]
            year = df_subset.head(1)['year'].values[0]
            avg_song_length = df_subset.head(1)['avg_song_length'].values[0]
            query = artist + ' ' + album

            album_cover = show_album_cover(query)
            with col2: 
                time.sleep(1)
                st.image(album_cover, width=400)
                st.write(f'**{album}**, from **{year}** is the **{artist}** album with the shortest songs with an average song length of **{avg_song_length}** minutes')