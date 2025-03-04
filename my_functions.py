def check_duplicates_origins(df):
    if df['origin'].duplicated().sum() == 0:
        print('No duplicates')
    else: 
        duplicates = df['origin'].duplicated().sum()
        print(f'Found {duplicates} duplicates:')
        print(f'{df[df['origin'].duplicated()][['city', 'country']]}\n')

        df.drop_duplicates(subset=['origin'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        print(f'Resulting dataset: {df.shape}')

def check_duplicates_artists(df):
    if df['artist'].duplicated().sum() == 0:
        print('No duplicates')
    else: 
        duplicates = df['artist'].duplicated().sum()
        print(f'Found {duplicates} duplicates:')
        print(f'{df[df['artist'].duplicated()]['artist']}\n')

        df.drop_duplicates(subset=['artist'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        print(f'Resulting dataset: {df.shape}')

def check_duplicates(df):
    if df.duplicated().sum() == 0:
        print('No duplicates')
    else: 
        duplicates = df.duplicated().sum()
        print(f'Found {duplicates} duplicates:')

        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        print(f'Resulting dataset: {df.shape}')

def check_duplicates_masters(df):
    if df['master_id'].duplicated().sum() == 0:
        print('No duplicates')
    else: 
        duplicates = df['master_id'].duplicated().sum()
        df.drop_duplicates(subset='master_id', inplace=True)
        df.reset_index(drop=True, inplace=True)
        print(f'Found {duplicates} duplicates')
        print(f'Resulting dataset: {df.shape}')

def check_duplicates_albums(df):
    if df[['artist', 'title']].duplicated().sum() == 0:
        print('No duplicates')
    else: 
        duplicates = df[['artist', 'title']].duplicated().sum()
        df.drop_duplicates(subset=(['artist', 'title']), inplace=True)
        df.reset_index(drop=True, inplace=True)
        print(f'Found {duplicates} duplicates')
        print(f'Resulting dataset: {df.shape}')

def delete_non_uk_artists(df):
    import numpy as np
    
    non_uk_artists = ['Evanescence', "Stake", "Embrace", 'Ultimate Spinach', 'Jeff Buckley', 'Four Year Strong', 'Todd Rundgren', 'Lunatic Soul', 'Throwing Muses', 'The Cramps', 'American Football',
                    'MD.45', 'Quiet Riot', 'Nine Inch Nails', 'Red House Painters', 'The Bronx', 'Weezer', 'Panchiko', 'Megadeth', 'The Band', 'Enslaved', 'Thin Lizzy', 'The Lucksmiths', 'Opeth',
                    'Talking Heads', 'Rory Gallagher', 'Pearl Jam', 'My Bloody Valentine', 'The Doors', 'The Beach Boys', 'Metallica', 'Death', 'Bob Dylan', 'Tom Waits', 'Tool', 'Brand New',
                    'Alice in Chains', 'Rush', 'Willie Nelson', 'Phil Lynott', 'Dead Can Dance', 'Bon Jovi', 'Paul Simon', 'At the Drive-In', 'Deftones', 'System of a Down', 'Green Day', 'Linkin Park',
                    'Slayer', 'Neutral Milk Hotel', 'The Mars Volta', 'Rage Against the Machine', 'Mastodon', 'Queens of the Stone Age', 'Beach House', 'Turnover', 'A Day To Remember', 'Sahg', 'Rival Sons',
                    'Minus the Bear', 'The Incredible Bongo Band', 'Jimi Hendrix', 'Framing Hanley', 'Bon Iver', 'Alter Bridge', 'Death From Above 1979', 'The Smashing Pumpkins', 'Arcade Fire',
                    'Red Hot Chili Peppers', 'Nirvana', 'Between the Buried and Me', 'Something Corporate', 'blink-182', 'Pantera', 'Deafheaven', 'My Chemical Romance', 'Slipknot', 'Soundgarden',
                    "Guns N' Roses", 'Converge', 'Pixies', 'Protest the Hero', 'Poison the Well', 'Death Cab for Cutie', 'Ephel Duath', 'Blind Melon', 'Behemoth', 'Insomnium', 'Ben Harper', 'The Replacements',
                    'Caribou', 'Samiam', 'Satyricon', 'Sponge', 'Midlake', 'Frank Zappa', 'M. Ward', 'The Brian Jonestown Massacre', 'Cinderella', 'Ulver', 'Further Seems Forever', 'Babylon A.D.',
                    'Severed Savior', 'Threshold', 'Soul Asylum', 'Red Krayola', 'Art Garfunkel', 'Toad', 'Indian Summer', 'Santana', 'Eagles', 'New York Dolls', 'Bruce Springsteen', 'Emperor',
                    'Chicago'
                  ]
    
    print(f"Initial artists: {df['artist'].nunique()}")
    df['artist'] = df['artist'].apply(lambda x: np.nan if x in non_uk_artists else x)
    df.dropna(subset=['artist'], inplace=True)
    print(f"Final artists: {df['artist'].nunique()}")

def columns_show_ratings(df):
    # I want to see the year next to the album title, and I don't care much about the ids
    list_of_columns = ['album_id', 'artist', 'title', 'year', 'rating', 'votes', 'album_length', 'tracks', 'release_country',
                       'release_type', 'genres', 'styles', 'artist_profile', 'artist_id', 'master_id', 'main_release_id']
    df = df[list_of_columns]
    return df

def columns_hide_ratings(df):
    # columns like df_masters, they have to be the same in order for the next merge to properly work
    list_of_columns = ['artist_id', 'master_id', 'main_release_id', 'release_country', 'artist', 'title', 'year',
                       'album_length', 'tracks', 'release_type', 'genres', 'styles', 'artist_profile']
    df = df[list_of_columns]
    return df

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

def display_top_albums(df, style):
    import streamlit as st
    import time
    col1, col2 = st.columns([0.6, 0.4])
    roots_rock = ['Blues Rock', 'Country Rock', 'Folk Rock', 'Rock & Roll', 'Soft Rock', 'Southern Rock']

    if style is not 'All':
        year = st.number_input(':watch: **Year**', min_value=df[df['style']==style]['year'].min(), max_value=2010, step=1, key="year_input")
        df_style = df[df['year']==year].query(f"style == '{style}'")[['artist', 'title', 'rating']]\
                        .sort_values('rating', ascending=False)\
                        .head()\
                        .reset_index(drop=True)
        df_style.index = range(1, len(df_style) + 1)

    else:
        year = st.number_input(':watch: **Year**', min_value=1960, max_value=2010, step=1)
        df_style = df[df['year']==year].query(f"style.isin({roots_rock})")\
                    [['artist', 'title', 'rating']]\
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

        return artist, album, query



    

