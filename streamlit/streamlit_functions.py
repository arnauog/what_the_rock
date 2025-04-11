import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import time
import requests
from bs4 import BeautifulSoup
import regex as re

def spoti_open(query):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    import time
    import webbrowser

    client_id = st.secrets['client_id']
    client_secret = st.secrets['client_secret']

    #Initialize SpotiPy with user credentials
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = client_id,
                                                            client_secret = client_secret))
    opensong = sp.search(q=query, limit=1)
    browser = opensong['tracks']['items'][0]['album']['external_urls']['spotify']
    album_id = browser.split('album/')[1]
    # st.markdown(f"[Listen on Spotify]({browser})")
    spotify_url = 'https://open.spotify.com/embed/album/' + album_id + '?utm_source=generator'

    # Embed the iframe using HTML
    components.html(
        f"""
        <iframe style="border-radius:12px" 
                src="{spotify_url}" 
                width="100%" 
                height="700" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy"></iframe>
        """,
        height=700
    )

    webbrowser.open(browser)


def get_style(df, subgenre, col2):
    style = st.selectbox(':musical_note: **Style**', ['Select a style']+list(df[df['subgenre']==subgenre]['style'].unique()))
    
    if style != 'Select a style': 
        year, artist, album, query, df_style = display_top_albums(df, subgenre, style)

        if query != 'No albums':
            if st.button('Search'):
                st.dataframe(df_style)
                st.write(f'**{album}** by **{artist}** was the top {style} album of {year}')
                album_cover = show_album_cover(query)

                with col2: 
                    try:
                        spoti_open(query)
                    except:
                        st.image(album_cover, width=400)


def display_top_albums(df, subgenre, style):
        year = st.number_input(':watch: **Year**', min_value=df[df['style']==style]['year'].min(), max_value=2010, step=1)
        df_style = df[df['year']==year].query(f"style == '{style}'")[['artist', 'title', 'rating', 'votes']]\
                        .sort_values('rating', ascending=False)\
                        .head()\
                        .reset_index(drop=True)
        df_style.index = range(1, len(df_style) + 1)

        if len(df_style)>0:
            artist = df_style.head(1)['artist'].values[0]
            album = df_style.head(1)['title'].values[0]
            query = artist + ' ' + album
            return year, artist, album, query, df_style
        else:
            st.write('Try another style or year')
            artist = ''
            album = ''
            query = 'No albums'
            return year, artist, album, query, df_style


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

    
def create_folium_map(df, country, subgenre):
    import folium
    from folium import Map
    from folium.plugins import HeatMap

    df = pd.read_csv('Datasets/df_country.csv')

    uk_lat = 53.909290891215214
    uk_lon = -2.1608240239505117 
    us_lat = 38.09612098863635 
    us_lon = -96.48185032372986 

    maps = {f"United Kingdom": Map(location=[uk_lat, uk_lon], zoom_start=6),  # Example coordinates
            "United States": Map(location=[us_lat, us_lon], zoom_start=5)}

    # Select the correct DataFrame
    df = df[df['country']==country]
    
    # create the subset of the subgenre
    subset_df = df[df['subgenre'] == subgenre]

    # create the FeatureGroup
    subset_df_group = folium.FeatureGroup(name = f'{subgenre}: {subset_df.shape[0]}') 

    # the subset is the subgenre and we i només ens interessen 2 columnes: les coordenades
    HeatMap(data = subset_df[['latitude', 'longitude']]).add_to(subset_df_group) 

    # Add the FeatureGroup to the correct map
    maps[country].add_child(subset_df_group)


def bandcamp_albums(artist):
        # create empty lists
    titles_list = []
    album_length_list = []
    album_length_clean = []
    tracks_list = []
    prices_list = []
    prices_currency = []
    years_list = []
    artist_clean = artist.lower().replace(' ', '')

    try:
        url = f'https://{artist_clean}.bandcamp.com/music'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        location = soup.select('div p span', class_="location secondaryText")[1].text
        print(f"{artist_clean} - {location}")

        releases = soup.select('#music-grid li a p')

        if len(releases) > 0:
            for i in releases:
                title = i.text.replace('\n', '').strip()
                print(title)
                title_changed = (
                    title.replace('(', '')
                        .replace(')', '')
                        .replace('[', '')
                        .replace(']', '')
                        .replace(' / ', '-')
                        .replace("'", '')
                        .replace('"', '')
                        .replace('& ', '')
                        .replace('feat.', 'feat')
                        .replace('Pt.', 'pt')
                        .replace(',', '')
                        .replace(' - ', '-')    
                        .replace(' ', '-')
                        .lower()
                )
                titles_list.append(title)

                try:
                    url = f'https://{artist_clean}.bandcamp.com/album/{title_changed}'
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, "html.parser")
                    if "Sorry, that something isn’t here" not in soup.text:
                        try:
                            price = soup.select('span > span.base-text-color')[0].text
                            prices_currency.append(price)
                            prices_list.append(float(price.replace('$', '').replace('€', '').replace('£', '')))
                        except: 
                            free = soup.select('#trackInfoInner > ul > li.buyItem.digital > div.ft > h4 > button')
                            # if len(free) > 0:
                            price = '0'
                            prices_currency.append(0)
                            prices_list.append(0)
                        release_date = soup.select('#trackInfoInner > div.tralbumData.tralbum-credits')
                        year = release_date[0].text.strip().split(', ')[1][:4]
                        years_list.append(year)
                        songs_table = soup.select('table', class_='track_list track_table')[1]('span')
                        tracks = len(songs_table)//2
                        tracks_list.append(tracks)
                        song_durations = []
                        minutes_list = []
                        seconds_list = []

                        soup2 = BeautifulSoup(str(songs_table), "html.parser")
                        durations = [span.get_text(strip=True) for span in soup2.find_all("span", class_="time secondaryText")]

                        for i in durations:
                            try:
                                minutes, seconds = map(int, i.split(':'))
                                minutes_list.append(minutes)
                                seconds_list.append(seconds)
                                song_duration_minutes = minutes + seconds/60
                                song_durations.append(song_duration_minutes)
                            except:
                                pass

                        minutes_total = sum(minutes_list) + (sum(seconds_list)//60)
                        seconds_rest = sum(seconds_list)%60

                        if minutes_total < 60:
                            album_length = str(f'{minutes_total}:{seconds_rest:02}')
                        else:
                            hours = minutes_total // 60
                            minutes_rest = minutes_total % 60
                            album_length = str(f'{hours}:{minutes_rest:02}:{seconds_rest:02}')
                            
                        album_length_list.append(round(sum(song_durations), 2))
                        album_length_clean.append(album_length)
                    else:
                        print('This is not an album')
                        album_length_list.append(np.nan)
                        album_length_clean.append(np.nan)
                        prices_currency.append(np.nan)
                        prices_list.append(np.nan)
                        years_list.append(np.nan)
                        tracks_list.append(np.nan)
                except: 
                    print("Couldn't find the album")
                    album_length_list.append(np.nan)
                    album_length_clean.append(np.nan)
                    prices_currency.append(np.nan)
                    prices_list.append(np.nan)
                    years_list.append(np.nan)
                    tracks_list.append(np.nan)
        else:
            title = soup.select('#name-section > h2')[0].text.replace('\n', '').strip()
            titles_list.append(title)
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                try:
                    price = soup.select('span > span.base-text-color')[0].text
                    prices_currency.append(price)
                    prices_list.append(float(price.replace('$', '').replace('€', '').replace('£', '')))
                except:
                    free = soup.select('#trackInfoInner > ul > li.buyItem.digital > div.ft > h4 > button')
                    # if len(free) > 0:
                    price = '0'
                    prices_currency.append(0)
                    prices_list.append(0)
                release_date = soup.select('#trackInfoInner > div.tralbumData.tralbum-credits')
                year = release_date[0].text.strip().split(', ')[1][:4]
                years_list.append(year)
                try:
                    songs_table = soup.select('table', class_='track_list track_table')[1]('span')
                    tracks = len(songs_table)//2
                    tracks_list.append(tracks)
                    song_durations = []
                    minutes_list = []
                    seconds_list = []

                    soup2 = BeautifulSoup(str(songs_table), "html.parser")
                    durations = [span.get_text(strip=True) for span in soup2.find_all("span", class_="time secondaryText")]

                    for i in durations:
                        try:
                            minutes, seconds = map(int, i.split(':'))
                            minutes_list.append(minutes)
                            seconds_list.append(seconds)
                            song_duration_minutes = minutes + seconds/60
                            song_durations.append(song_duration_minutes)
                        except:
                            pass

                    minutes_total = sum(minutes_list) + (sum(seconds_list)//60)
                    seconds_rest = sum(seconds_list)%60

                    if minutes_total < 60:
                        album_length = str(f'{minutes_total}:{seconds_rest:02}')
                    else:
                        hours = minutes_total // 60
                        minutes_rest = minutes_total % 60
                        album_length = str(f'{hours}:{minutes_rest:02}:{seconds_rest:02}')
                        
                    album_length_list.append(round(sum(song_durations), 2))
                    album_length_clean.append(album_length)
                except:
                    album_length_list.append(np.nan)
                    album_length_clean.append(np.nan)
            except: 
                print("Couldn't find the album")
                album_length_list.append(np.nan)
                album_length_clean.append(np.nan)
                prices_currency.append(np.nan)
                prices_list.append(np.nan)
                years_list.append(np.nan)
                tracks_list.append(np.nan)

    except:
        titles_list.append(np.nan)
        tracks_list.append(np.nan)
        print(f"{artist_clean} - Maybe this artist doesn't have a bandcamp page")

        # check if there are any valid values in price_list, sometimes there are albums but they can't be bought
    if pd.Series(prices_list).notna().any():
        # Create a DataFrame with the results

        df_bandcamp = pd.DataFrame({'year': years_list
                                    , 'title': titles_list
                                    , 'length': album_length_clean
                                    , 'duration': album_length_list
                                    , 'tracks': tracks_list
                                    , 'price': prices_currency
                                    , 'price_float': prices_list})

        df_bandcamp['price/min'] = np.where(df_bandcamp['duration'].notna(), 
        round(df_bandcamp[f'price_float'] / df_bandcamp['duration'], 3), 0)

        df_bandcamp.dropna(subset=f'price_float', inplace=True)
        df_bandcamp.drop(columns=['duration', 'price_float'], inplace=True)
        df_bandcamp['tracks'] = df_bandcamp['tracks'].astype(int)
        df_bandcamp.sort_values('price/min', inplace=True)
        df_bandcamp.reset_index(drop=True, inplace=True)
        return df_bandcamp