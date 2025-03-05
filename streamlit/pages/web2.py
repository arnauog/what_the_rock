import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")
from streamlit_functions import *
import time
import folium
from folium import Marker, Icon, Map
from folium.plugins import HeatMap
import streamlit.components.v1 as components
import random

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title='What the Rock?', page_icon=':guitar:', layout='wide')

df = pd.read_csv('Datasets/df_test.csv')

# define the sidebar

st.title('Best albums of every rock style')

# Wordcloud
# styles = df['style'].values
# styles_joined = ", ".join(styles)
# wordcloud = WordCloud(width=1600, height=800, background_color="white").generate(styles_joined)
# fig, ax = plt.subplots(figsize=(8,4), dpi=300)
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# st.pyplot(fig)

col1, col2 = st.columns([0.6, 0.4])

with col1:
    subgenre = st.selectbox(':mag: **Subgenre**', ['All']+list(df["subgenre"].unique()))


    if subgenre is 'All':
        style = st.selectbox(':musical_note: **Style**', ['All']+list(df['style'].unique()))
    else:
        # df_subgenre = df[df['subgenre']==subgenre]
        style = st.selectbox(':musical_note: **Style**', ['All']+list(df[df['subgenre']==subgenre]['style'].unique()))

        st.write('The top rated albums of that year are:')

        if style is not 'All':
            artist, album, query = display_top_albums(df, style)
            year = st.number_input(':watch: **Year**', min_value=df[df['style']==style]['year'].min(), max_value=2010, step=1)
            df_style = df[df['year']==year].query(f"style == '{style}'")[['artist', 'title', 'rating']]\
                            .sort_values('rating', ascending=False)\
                            .head()\
                            .reset_index(drop=True)
            df_style.index = range(1, len(df_style) + 1)

        else:
            year = st.number_input(':watch: **Year**', min_value=1960, max_value=2010, step=1)
            df_style = df[df['year']==year][['artist', 'title', 'rating']]\
                        .groupby(['artist', 'title']).agg('mean')\
                        .sort_values('rating', ascending=False)\
                        .head()\
                        .reset_index()
            df_style.index = range(1, len(df_style) + 1)

        if st.button('Search', key=random.randint(1, 100000000)):
            st.dataframe(df_style)

            artist = df_style.head(1)['artist'].values[0]
            album = df_style.head(1)['title'].values[0]
            query = artist + ' ' + album

with col2:  
    album_cover = show_album_cover(query)
    st.image(album_cover)
    time.sleep(1)
    st.write(f'**{album}** by **{artist}** was the top rated album that year')
    key=random.randint(1, 1000000000)
    if st.button('Listen in Spotify', key=key):
        spoti_open(query)
