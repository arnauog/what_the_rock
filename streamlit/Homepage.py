import streamlit as st
from streamlit_functions import *
import streamlit.components.v1 as components

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import folium
from folium import Marker, Icon, Map
from folium.plugins import HeatMap

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title='What the Rock?', page_icon=':guitar:', layout='wide')

st.title(':drum_with_drumsticks: What the Rock? :guitar:')
st.subheader("A Rock music anaylsis in the US and UK between 1960 and 2010")
st.divider()

st.write("In this project you'll be able to explore the following and much more:")
st.write('- Which are the best albums of a specific subgenre or style?')
st.write("- Evolution of rock styles throughout since its birth in the 1960s.")
st.write('- Timeline of an artist with the best and most popular albums categorized by styles.')
st.write('- Comparison of several artists.')
st.write('- Where do the bands you listen to most come from?')
st.write("- In which regions and cities are more predominant certain styles?")
st.write("- Which are best artists and albums of a specific region/state.")
st.write("- Analysis of album and song length depending on the style.")
st.write(" ")
st.write("And last but not least...")
st.write("- **Buy the album with the lowest price per minute** to make the most of your money and support the artist.")

st.divider()
st.subheader("Project flowchart: visual representation of the development of the project")
st.image('Roadmap.jpg', width=1000)

# # Wordcloud
# df = pd.read_csv('Datasets/df_final.csv')
# artists = df['artist'].values
# artists_joined = ", ".join(artists)
# wordcloud = WordCloud(width=1600, height=800, background_color="white").generate(artists_joined)
# fig, ax = plt.subplots(figsize=(8,4), dpi=300)
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# st.pyplot(fig)



