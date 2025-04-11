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
st.subheader("An analysis of rock music from the US and UK (1960-2010)")
st.divider()

st.write(":white_check_mark: In this project you'll be able to explore the following and much more:")
st.write('- Which are the best albums of a specific subgenre or style?')
st.write("- :chart: Evolution of rock styles since its birth in the 1960s.")
st.write('- Timeline of an artist highlighting their best and most popular albums, categorized by styles.')
st.write('- Comparison between several artists.')
st.write("- :world_map: Maps of the US and UK showing the most common styles in each state and city.")
st.write("- Which are best artists and albums from a specific region/state?")
st.write("- Analysis of :stopwatch: album and song lengths by style.")
st.write(" ")
st.write("And last but not least...")
st.write("- **Buy the album with the lowest :money_with_wings: price per minute** to make the most of your money and support the artist.")

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



