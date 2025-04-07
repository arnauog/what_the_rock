import streamlit as st
from streamlit_functions import *
import streamlit.components.v1 as components

import numpy as np
import pandas as pd
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt

import folium
from folium import Marker, Icon, Map
from folium.plugins import HeatMap


# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title='What the Rock?', page_icon=':guitar:', layout='wide')

df = pd.read_csv('Datasets/df_final.csv')

st.title(':drum_with_drumsticks: What the Rock? :guitar:')
st.subheader("A Rock music anaylsis in the US and UK between 1960 and 2010")
st.divider()
st.image('Roadmap/Roadmap.jpg', width=1000)

# # Wordcloud
# artists = df['artist'].values
# artists_joined = ", ".join(artists)
# wordcloud = WordCloud(width=1600, height=800, background_color="white").generate(artists_joined)
# fig, ax = plt.subplots(figsize=(8,4), dpi=300)
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# st.pyplot(fig)



