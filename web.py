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
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header('Price per brand')
        price_per_brand = df.groupby(["brand"]).agg({'price': 'mean'}).sort_values('price', ascending=False).astype({'price': int}) # mean price per brand
        fig, ax = plt.subplots(figsize=(10,10))
        sns.barplot(data=price_per_brand, y='brand', x='price')
        st.pyplot(fig)

        st.header('Scatterplots')
        st.write('How do the different features affect the price?')
        columnes = ['age', 'km', 'power_cv']
        for i in columnes:
            fig, ax = plt.subplots(figsize=(5,5))
            sns.scatterplot(data=df, x=i, y='price')
            st.pyplot(fig)

    with col2:
        st.header('Price per style')
        price_per_style = df.pivot_table(values="price", index="style", aggfunc='mean').sort_values(['price'], ascending=False).astype({'price': int}) # mean price per style
        fig, ax = plt.subplots(figsize=(10,20))
        sns.barplot(data=price_per_style, y='style', x='price')
        st.pyplot(fig)

elif selection == ':world_map: Map':
    df

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
        subgenre = st.selectbox(':mag: **Subgenre**', [None, 'Roots Rock', 'Classic Rock', 'Metal', 'Punk', 'Indie Rock'])
        if subgenre is None:
            st.write("Please select a subgenre.")
        else:
            with col2:
                with col1:
                    if subgenre == 'Roots Rock':
                        roots_rock = ['Blues Rock', 'Country Rock', 'Folk Rock', 'Rock & Roll', 'Soft Rock', 'Southern Rock']
                        style = st.selectbox(':musical_note: **Style**', roots_rock)

                        artist, album, query = display_top_albums(df, style)

                        # if style is not 'All':
                        #     year = st.number_input(':watch: **Year**', min_value=df[df['style']==style]['year'].min(), max_value=2010, step=1, key="year_input")
                        #     df_style = df[df['year']==year].query(f"style == '{style}'")[['artist', 'title', 'rating']]\
                        #                     .sort_values('rating', ascending=False)\
                        #                     .head()\
                        #                     .reset_index(drop=True)
                        #     df_style.index = range(1, len(df_style) + 1)

                        # else:
                        #     year = st.number_input(':watch: **Year**', min_value=1960, max_value=2010, step=1)
                        #     df_style = df[df['year']==year].query(f"style.isin({roots_rock})")\
                        #                 [['artist', 'title', 'rating']]\
                        #                 .groupby(['artist', 'title']).agg('mean')\
                        #                 .sort_values('rating', ascending=False)\
                        #                 .head()\
                        #                 .reset_index()
                        #     df_style.index = range(1, len(df_style) + 1)

                        # st.write('The top rated albums of that year are:')
                        # if st.button('Search'):
                        #     st.dataframe(df_style)

                        #     artist = df_style.head(1)['artist'].values[0]
                        #     album = df_style.head(1)['title'].values[0]
                        #     query = artist + ' ' + album

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
    
                    # if style is not 'All':
                    #     year = st.number_input(':watch: **Year**', min_value=df[df['style']==style]['year'].min(), max_value=2010, step=1)
                    #     df_style = df[df['year']==year].query(f"style == '{style}'")[['artist', 'title', 'rating']]\
                    #                     .sort_values('rating', ascending=False)\
                    #                     .head()\
                    #                     .reset_index(drop=True)
                    #     df_style.index = range(1, len(df_style) + 1)

                    # else:
                    #     year = st.number_input(':watch: **Year**', min_value=1960, max_value=2010, step=1)
                    #     df_style = df[df['year']==year][['artist', 'title', 'rating']]\
                    #                 .groupby(['artist', 'title']).agg('mean')\
                    #                 .sort_values('rating', ascending=False)\
                    #                 .head()\
                    #                 .reset_index()
                    #     df_style.index = range(1, len(df_style) + 1)

                    # st.write('The top rated albums of that year are:')
                    # if st.button('Search'):
                    #     st.dataframe(df_style)

                    #     artist = df_style.head(1)['artist'].values[0]
                    #     album = df_style.head(1)['title'].values[0]
                    #     query = artist + ' ' + album

                    #     with col2:  
                    #         album_cover = show_album_cover(query)
                    #         st.image(album_cover)
                    #         time.sleep(1)
                    #         st.write(f'**{album}** by **{artist}** was the top rated album that year')


