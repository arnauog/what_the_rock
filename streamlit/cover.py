import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")
from my_functions import *
import time
import folium
from folium import Marker, Icon, Map
from folium.plugins import HeatMap
import streamlit.components.v1 as components

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title='What the Rock?', page_icon=':guitar:', layout='wide')

df = pd.read_csv('Datasets/df_test.csv')

# define the sidebar
with st.sidebar:
    selection = st.radio('', [':house: Introduction', ':chart: Tableau', ':world_map: Map', 'Search for styles'])

if selection == ':house: Introduction':
    st.title(':drum_with_drumsticks: What the Rock? :guitar:')
    st.write("A Rock music anaylsis in the US and UK between 1960 and 2010")
    st.image('images/photos/rock_concert.jpg')
    st.subheader('Features :mag:')

elif selection == ':chart: Tableau':
    st.title("Let's see some graphs!")
    def main():
        html_temp="<div class='tableauPlaceholder' id='viz1741109972455' style='position: relative'><noscript><a href='#'><img alt='ratings_styles_decades (2) ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Wh&#47;Whattherock&#47;ratings_styles_decades2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Whattherock&#47;ratings_styles_decades2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Wh&#47;Whattherock&#47;ratings_styles_decades2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='es-ES' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1741109972455');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"
        components.html(html_temp, width=1000, height=600)

    if __name__ == '__main__':
        main()

elif selection == ':world_map: Map':
    st.header('Geographical distribution of the genres')
    data = pd.read_csv('Datasets/df_country.csv')

    uk_lat = 53.909290891215214
    uk_lon = -2.1608240239505117 
    us_lat = 38.09612098863635 
    us_lon = -96.48185032372986 

    maps = {f"United Kingdom": Map(location=[uk_lat, uk_lon], zoom_start=6),  # Example coordinates
            "United States": Map(location=[us_lat, us_lon], zoom_start=4)}

    def create_folium_map(df, country, subgenre):
        df = df[df['country']==country]  # Select the correct DataFrame
        
        # create the subset of the subsubgenre
        subset_df = df[df['subgenre'] == subgenre]

        # create the FeatureGroup
        subset_df_group = folium.FeatureGroup(name = f'{subgenre}: {subset_df.shape[0]}') 

        # the subset is the subsubgenre and we i només ens interessen 2 columnes: les coordenades
        HeatMap(data = subset_df[['latitude', 'longitude']]).add_to(subset_df_group) 

        # Add the FeatureGroup to the correct map
        maps[country].add_child(subset_df_group)

    country = st.selectbox('Select a country', ['Select a country', 'United Kingdom', 'United States'])

    if country == 'United Kingdom':
        create_folium_map(data, "United Kingdom", "roots")
        create_folium_map(data, "United Kingdom", "classic")
        create_folium_map(data, "United Kingdom", "metal")
        create_folium_map(data, "United Kingdom", "punk")
        create_folium_map(data, "United Kingdom", "indie")
        folium.LayerControl(collapsed=False, position="topleft").add_to(maps['United Kingdom'])
        
        # Save map to HTML
        maps['United Kingdom'].save("map_uk.html")

        # Display map in Streamlit using the HTML file
        st.components.v1.html(open("map_uk.html", "r").read(), height=600)

    elif country == 'United States':
        create_folium_map(data, "United States", "roots")
        create_folium_map(data, "United States", "classic")
        create_folium_map(data, "United States", "metal")
        create_folium_map(data, "United States", "punk")
        create_folium_map(data, "United States", "indie")
        folium.LayerControl(collapsed=False, position="topleft").add_to(maps['United States'])
        
        # Save map to HTML
        maps['United States'].save("map_us.html")

        # Display map in Streamlit using the HTML file
        st.components.v1.html(open("map_us.html", "r").read(), height=600)

elif selection == 'Search for styles':
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
        subgenre = st.selectbox(':mag: **Subgenre**', ['All', 'Roots Rock', 'Classic Rock', 'Metal', 'Punk', 'Indie Rock'])
        with col2:
            with col1:
                if subgenre == 'Roots Rock':
                    roots_rock = ['Blues Rock', 'Country Rock', 'Folk Rock', 'Rock & Roll', 'Soft Rock', 'Southern Rock']
                    style = st.selectbox(':musical_note: **Style**', roots_rock, placeholder='All')

                    artist, album, query = display_top_albums(df, style)

                    with col2:  
                        album_cover = show_album_cover(query)
                        st.image(album_cover)
                        time.sleep(1)
                        st.write(f'**{album}** by **{artist}** was the top rated album that year')

                elif subgenre == 'Classic Rock':
                    style = st.selectbox(':musical_note: **Style**', ["All", 'Art Rock', 'Classic Rock', 'Prog Rock', 'Psychedelic Rock', 'Space Rock', 'Symphonic Rock'])
                elif subgenre == 'Metal':
                    style = st.selectbox(':musical_note: **Style**', ["All", 'Black Metal', 'Death Metal', 'Doom Metal', 'Hard Rock', 'Heavy Metal', 'Metalcore',
                                                                        'Nu Metal', 'Progressive Metal', 'Speed Metal', 'Stoner Rock', 'Thrash'])
                elif subgenre == 'Punk':
                    style = st.selectbox(':musical_note: **Style**', ["All", 'Garage Rock', 'Grunge', 'Hardcore', 'Pop Punk', 'Post-Hardcore', 'Post-Punk', 'Punk'])
                else:
                    style = st.selectbox(':musical_note: **Style**', ["All", 'Alternative Rock', 'Emo', 'Indie Rock', 'New Wave', 'Pop Rock', 'Post Rock', 'Shoegaze'])

                if style is not 'All':
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

                st.write('The top rated albums of that year are:')
                if st.button('Search'):
                    st.dataframe(df_style)

                    artist = df_style.head(1)['artist'].values[0]
                    album = df_style.head(1)['title'].values[0]
                    query = artist + ' ' + album

                    with col2:  
                        album_cover = show_album_cover(query)
                        st.image(album_cover)
                        time.sleep(1)
                        st.write(f'**{album}** by **{artist}** was the top rated album that year')


