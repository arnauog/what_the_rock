import streamlit as st
from streamlit_functions import *
import pandas as pd
import numpy as np

st.title('Code behind the project')

st.subheader('A look at all the work done to get the results')

tab1, tab2 = st.tabs(['Data Gathering', 'Data Cleaning'])

with tab1:
    st.title('Data Gathering') 

    col1, col2, col3 = st.columns([0.1, 0.4, 0.5])

    with col1:
        topic = st.radio(' ', ['Discogs API', 'Ratings', 'Origin'])

        if topic == 'Discogs API':
            with col2:
                st.image("streamlit/logos/Discogs1.jpg")
                st.write("For me, it was really important that I could get information from internet, not only analyze it.")
                st.write("I didn't even check on the internet if there were some public available datasets, I wanted to create my own to have more control of the data and prove I could get information on my own.")
                st.write("After doing some research, I decided to get the data from the **Discogs API**, which provides **all the releases**, not just one from every album.")
                st.write("https://www.discogs.com")
            with col3:
                st.image('streamlit/images/Discogs_releases.png')
                st.image("streamlit/images/Discogs_get_masters_function.png")
            with col2:
                st.write("The topic, rock music, was too broad, so first I decided to focus on **artists from the United Kingdom**, birth of many influential and key bands on rock history.")
                st.write("I finished getting data from all the rock releases in the UK from 1960 in about a week,\n"
                    "and I realized most of the releases were from bands from the US, so I decided to get **United States** releases as well.")
                st.write("I ended up with a bit more than 11.000 albums")
                st.divider()
                st.subheader('Features')
                st.write("I wanted to analyze the **evolution of rock music**, so I got albums from 1960, when it started.")
                st.write("The **features** I wanted to get were:")
                st.write("- ``artist``\n- ``title``\n- ``year``\n"
                    "- ``album_length`` and ``tracks`` to get the average length of the song\n"
                    "- ``origin`` city of origin of the artist. I couldn't get a value, but a sentence where usually I had info of the artist origin (``artist_profile``)\n"
                    "- ``styles``\n- Info from ``ratings`` of the album, which the API didn't provide and **I had to get from another website**.")
                st.write("Each release relates to a **``master_id``**, where I got the main data from.  \n"
                    "However, many releases had a ``master_id = 0``, in which case I would get the info from the page of the ``release_id``.  \n"
                    "For every year I got I saved the data in a dataframe, so I would not lose the data if for some reason the code had crashed in the middle of a year,\n"
                    "and to check if I had gotten that album already or not (checking the ``master_id`` and the combination of ``artist`` and ``title``).")
                st.write("This was extremely important in the end, when I was getting only about 25% of the releases I was checking on the API.")
            with col3:
                st.image("streamlit/images/Discogs_get_masters_print.png")
                st.image("streamlit/images/Top_styles_2002_USA.png")
            with col2:
                st.divider()
                st.subheader("API limitations")
                st.write("There's a limit of 100 results per page and 100 pages, meaning 10.000 total releases.  \n"
                         "In the USA, from 1995 there were more than 10.000 releases from each year, so I decided to **iterate over ``styles`` as well**, which meant 2 things:")
                st.write("- The code took much longer, because I was checking the same album for all the different styles. It is quite common that an album had different styles.")
                st.code('plt.figure(figsize=(10, 20))\n'
                        'sns.barplot(data=data, y="style", x="albums", palette="Blues_r")\n'
                        'plt.xlabel("Number of Albums")\n'
                        'plt.ylabel("Style")\n'
                        'plt.title("Most common styles in 2002 USA")\n'
                        'plt.show()')
                st.write("- I could not get all the possible styles, there were too many, so at that point (I had gotten all releases from the UK and US releases from 1960 until 1994),\n"
                    "I analyzed the most common styles, from the years I had scraped and from a sample year of USA releases, in this case 2002,\n"
                    "and **kept only the most important ones**, dropping styles like *experimental, acoustic, indie pop, lo-fi, jazz-rock, industrial, avantgarde*, etc.")
                st.code('''styles_to_get = [
    "Alternative Rock", "Indie Rock", "Pop Rock", "New Wave", 
    "Emo", "Post Rock", "Shoegaze", "Hard Rock", 
    "Heavy Metal", "Death Metal", "Thrash", "Black Metal", "Doom Metal", 
    "Metalcore", "Progressive Metal", "Stoner Rock", "Speed Metal", "Nu Metal", 
    "Prog Rock", "Psychedelic Rock", "Art Rock", "Classic Rock", "Space Rock", 
    "Symphonic Rock", "Punk", "Hardcore", "Post-Punk", "Post-Hardcore", 
    "Pop Punk", "Grunge", "Garage Rock", "Folk Rock", "Blues Rock", "Rock & Roll", 
    "Soft Rock", "Country Rock", "Southern Rock"
]''')
                st.write("In the end, getting the US releases for a year between 2000 and 2010 took about **9h**.  \n"
                    "I decided to stop at 2010, since I didn't have much time left and I had already **50 years** to analyze, more than enough.")


        if topic == 'Ratings':
            with col2: 
                st.image('streamlit/logos/SputnikMusicLogo.jpg')
                st.write("https://www.sputnikmusic.com/")
                st.write("I checked many music websites to get the ratings via an API or webscraping, but in many there was no API or webscraping was banned, like in *Rate Your Music*.  \n"
                    "In the end I found ***SputnikMusic***, from where I could scrape with **BeautifulSoup** the ``ratings`` and ``votes`` from all the albums.")

                st.write("Luckily the webscraping was super easy, since every album had an **id** and I had to just modify the url.")
                st.write("https://www.sputnikmusic.com/soundoff.php?albumid=26400")
                st.code('''for id in range(start_id+1,start_id+1000):
    count+=1
    url = f'https://www.sputnikmusic.com/soundoff.php?albumid={id}'
    response = requests.get(f"{url}")
    soup = BeautifulSoup(response.content, "html.parser")''')
                
                st.write("This also meant that I could not simply scrape the pages of every artist, which told me directly all the information I wanted (title, year, rating and votes),  \n"
                    "but instead I had to calculate the mean rating with all the votes, though it was not that complicated.")
                st.code("""    # Get ratings
    rating = soup.select('font.reviewheading b')
    ratings_list = []

    for r in rating:
        if len(r.text) == 3:  # Only consider ratings with 3 characters (like '4.5')
            ratings_list.append(r.text)

    # Convert to float
    rating_floats = [float(num) for num in ratings_list]
    
    if rating_floats:
        number_of_votes = len(rating_floats) # calculate the number of votes
        number_of_votes_list.append(number_of_votes) # save it in a list')""")

                st.write("I would say there were only 2 problems:\n  "
                    "- There were all kinds of releases, not just studio albums, but also **compilations and live albums**,\n"
                    "which I didn't want and I couldn't tell them apart during the scraping, so I had to drop them later, with not perfect results.  \n"
                    "- In many albums there were not a lot of votes, and I decided it didn't make sense to consider albums with low number of votes,\n"
                    "since the mean rating would not be realistic, so I dropped albums with less than 20 votes, which turned out to be most of the albums.  \n"
                    "In a way, this was a filter to keep only the most popular and important albums in rock history.")
                st.code("df_ratings_top = df_ratings[df_ratings['votes']>=20]")
                
            with col3:
                st.image("streamlit/images/SputnikMusic_main.png")
                st.image("streamlit/images/sputnik_album_ratings.png")
        
        if topic == 'Origin':
            with col2:
                st.header("City of origin")
                st.write("I wanted to represent the geographical evolution of rock history in the US and the UK, "
                "so I needed more information about the origins of the artists, not just the country.")

                st.divider()
                st.subheader("Wikipedia scraping")
                st.write("I started scraping with **BeautifulSoup** the origins of the artists, but as I initially suspected, I faced 2 big problems:")
                st.write("- Not all the artists have a Wikipedia page  \n"
                    "- Some artists didn't specify the city, only the country")
                st.write("Also some artists had more than one city, or the code took the city but also other information, so I had to clean these ones as well.")

                st.divider()
                st.subheader("``artist_profile``")
                st.write("Remember I got this information from the API? Well, it was quite useful in this process of searching for the cities that didn't provide Wikipedia.")
                
                st.code("""# look for the albums of the artist in the original df to check it's the correct artist
df[df['artist']=='Big Kids'.strip()].sort_values('year').head()
                        """)
                
                st.write("First I searched for the artist and if I wanted to get the full ``artist_profile`` I searched for the index:")
                st.image("streamlit/images/artist_profile.PNG")

            with col3: 
                col4, col5 = st.columns([0.3,0.7])
                with col4:
                    st.image("streamlit/logos/Wikipedia.jpg")
                with col5:
                    st.image("streamlit/images/wikipedia_origin_us.png")

                st.code("""    for index in artists_to_do[start_index:final_index]:

        name_changed = index.replace(' ', '_')
        name_changed_band = name_changed + ('_(band)')
        name_changed_musician = name_changed + ('_(musician)')
        name_changed_singer = name_changed + ('_(singer)')

        try:
            url = f'https://en.wikipedia.org/wiki/{name_changed_band}'
            response = requests.get(url).content
            soup = BeautifulSoup(response, 'html.parser')

            table = soup.select('#mw-content-text > div.mw-content-ltr.mw-parser-output > table.infobox')

            location = table[0].text.split('Origin')[1].split('Genres')[0]
            count+=1
            
        # save info in lists
            artists_list.append(index)  
            origin_list.append(location)
            scraped+=1
            print(f'{scraped}/{count} - {name_changed_band}: {location}')""")

            with col2:
                st.divider()
                st.subheader("Rate Your Music")
                st.write("This is the website from where I originally wanted to get all the data, but their API hasn't been released yet and scraping is forbidden.")
                st.write("So at least in these artists I could manually check if there was more information of the origin, which in many times there was.")
                st.write("For the few bands where I couldn't get info of the city neither in Wikipedia, the Discogs API (``artist_profile``) nor in Rate Your Music,\n"
                    "I manually searched on Google and usually found them after some time of research.")
                st.write("When I found an artist from a country different than the US or the UK, I appended it to a list I had created to keep all these foreign artists separated.")
                
                st.code("""artists_to_remove = ['Monsters of Folk', 'Shrinebuilder', 'The Joe Perry Project', 'Boygenius',
                     'Scar the Martyr', 'Gordian Knot', 'Rock Star Supernova']

for artist in artists_to_remove:
        artists_usa.remove(artist)
        print(f'{artist} removed')
                        """)
                
                st.code("df_new_artists = df_new_artists[~df_new_artists['artist'].isin(artists_to_remove)]")
                st.video('streamlit/images/np where wrong origins 3 artist to remove.mp4')
                st.write("This way I knew exactly which artists I had gotten already the origin and which ones still not.")
                
                st.code("""df_final = pd.read_csv('Datasets/df_final.csv')
unique_artists = df_final[df_final['year']<2011]['artist'].unique()

df_artists_origins = pd.read_csv('Datasets/df_artists_origins.csv')
artists = df_artists_origins['artist'].unique()
artists_to_do = []

for artist in unique_artists:
    if artist not in artists and artist not in artists_to_remove:
        artists_to_do.append(artist)
                        """)

                st.divider()
                st.image("streamlit/logos/GeoPy.jpg", width=200)
                st.write("Thanks to this library I could find the coordinates of every city.")
                st.write("First I tested it just printing them, where I found more wrong locations and found that GeoPy doesn't recognize places like *Cumbria* or *Middlesex*.")

            with col3:                 
                st.image("streamlit/images/RYM_origin.png")
                st.image("streamlit/images/np where real origins wikipedia.jpg")
                st.write(" ")
                st.write(" ")
                st.video('streamlit/images/np where wrong origins 2.mp4')
                st.write("I had some techniques to quickly find the wrong locations.")
                st.code("""# print abnormally short origins and visually check if they are correct
for index, row in df_new_artists.iterrows():
    if len(row['origin']) < 10:
        print(index, row['origin'])""")
                st.code("""# I create a new column to calculate the lenght of the origin, if it's long it probably didn't scrap correctly Wikipedia
df_new_artists["origin_length"] = df_new_artists["origin"].str.len()
long_strings = df_new_artists[df_new_artists["origin_length"]>40] # create a df based on these long origins
long_strings # display the df so I can copy the parts I am interested in""")

                st.write(" ")
                st.write(" ")
                st.write("There were many artists that had squared brackets in their origins from Wikipedia.")
                st.image("streamlit/images/wikipedia_origins_claudators.png")
                st.code("""origin = "Kirkland, Washington"

origin_clean = re.sub(r'\[\d+\]', '', origin).replace('.', '')
location = geolocator.geocode(origin_clean)
print(f"{location.address}")
print(location.latitude, location.longitude)""")
                
            with col2:
                st.write(" ")
                st.divider()
                st.header("State")
                st.write("Apart from the city, I needed info from the state, which I got from the GeoPy address.")
                st.subheader('United States')
                st.write("I initially thought a simple split would do, but it was not that simple, so I had to apply **Regex**.")
                st.subheader('United Kingdom')
                st.write("For the UK it was more tricky. I couldn't get the info directly from the Geopy address like I did with the US, so I searched for a **public dataframe** with info about cities and regions.")
                st.write("But it was not that simple. 96 artists didn't have their city in the regions df, with meant some of the following:  \n"
                "- Their city was just not there.  \n"
                "- My city was incorrect.  \n"
                "- The public dataframe didn't include cities from Northern Ireland.")
                st.write("There were more problems. After merging, there were **510 extra rows**, which meant that there were **cities with the same name in the UK**.  \n"
                "So I searched for each of these cities and dropped from the public dataset the 'wrong' cities, the ones that were not my artist's origin city.")
                
            with col3:
                st.write(" ")
                st.code("""def extract_state(location):
    # Case 1: Full format with county and optional ZIP
    match = re.search(r'([\w\s]+),\s([\w\s]+),\s([\w\s]+)(?:,\s\d+)?,\sUnited States$', location)
    if match:
        return match.group(3)  # Extract state from 3rd capture group
    
    # Case 2: City and state only (no county, no ZIP)
    match = re.search(r'([\w\s]+),\s([\w\s]+),\sUnited States$', location)
    if match:
        return match.group(2)  # Extract state from 2nd capture group

    # Case 3: State only (e.g., "New Jersey, United States")
    match = re.search(r'([\w\s]+),\sUnited States$', location)
    if match:
        return match.group(1)  # Extract state from 1st capture group

    return None  # No match found""")
                
                st.image("streamlit/images/uk_repeated_cities.png")

            with col2:
                st.write(" ")
                st.divider()
                st.header("Population")
                st.write("I though it would be interesting to analyze if there were some particular cities with a big musical scene,\n"
                "but I couldn't simply get the cities with the most releases, because it's gonna be obviously the biggest cities, like Los Angeles and London.")
                st.write("First I wanted to get the cities population, which I did with a dataset from Kaggle, but then I realized there were many cities missing, in both countries.")
                st.write("So in the end I got the **state/region population**, a much better way since there are much fewer and I know the exact number, unlike cities.")
                st.write("For the UK, I chose Scotland, Wales, Northern Ireland and the 11 regions of England.")

            with col3:
                st.image("streamlit/images/city_population_missing.png")


with tab2:
    st.title('Data Cleaning') 

    col1, col2, col3 = st.columns([0.11, 0.4, 0.49])

    with col1:
        topic = st.radio(' ', ['Album length', 'Styles'])
        
        if topic == 'Album length':
            with col2:
                st.header("Album length")
                st.write("Around 20% of the albums didn't have info of the ``album_length``, so I went to get it somewhere else.  \n"
                "I gotta admit it was way longer and difficult than what I expected.")
            
            with col3:
                st.image("streamlit/images/album_length_0_percentage.jpg")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.image("streamlit/logos/Spotify.png", width=200)
                st.write(" ")   
                st.image("streamlit/images/spotipy_special_editions.jpg")
                st.write(" ")

            with col2:
                st.divider()
                st.subheader("Spotipy")
                st.write("First I started with **Spotipy**, the Spotify API, which apparently got me quite good results, but when I looked closer, there were 2 issues:  \n"
                "- It couldn't find the length from all the albums  \n"
                "- Even when it found the length, sometimes it was another version (expanded, extended, anniversary, etc) longer than the original, so I ended up with a bunch of albums with a lot of songs and long runtimes.")
                st.image("streamlit/images/spotipy_boxplot_album_length.png")
                st.image("streamlit/images/spotipy_boxplot_tracks.png")

                st.divider()
                st.subheader("Wikipedia")
                st.write("So I decided to scrap the length from **Wikipedia**, which turned out to be quite easy to code, quite effective and very fast.")

            with col3:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.code("""
            url = f"https://en.wikipedia.org/wiki/{title_changed}"
            response = requests.get(url).content
            soup = BeautifulSoup(response, "html.parser")

            table = soup.select('#mw-content-text > div.mw-content-ltr.mw-parser-output > table.infobox')
            length = table[0].text.split('Length')[1].split('Label')[0]
            minutes, seconds = map(int, length.split(':'))
            duration_minutes = round(minutes + seconds/60, 2)

        # save info in lists
            lengths_list.append(duration_minutes)
            scraped+=1
""")
                
            with col2:
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.divider()
                st.subheader("Discogs API")
                st.write("With the albums I couldn't scrape from Wikipedia, I decided to check again on the **Discogs API**.  \n"
                "It couldn't find the album length on the master release page, but there were several releases of every album, so I created a function to search for the ``artist`` and ``title``, and get the album length of the first 5 releases, which turned out to be quite effective.")

            with col3:
                st.write(" ")
                st.code("""        # Iterate over the first 5 results
        for i in range(min(5, len(data['results']))):
            time.sleep(1)
            release_id = data['results'][i]['id']
            url2 = f"https://api.discogs.com/releases/{release_id}"
            response = requests.get(url2, headers=headers)
            data2 = response.json()

            try:
                tracklist = data2['tracklist']
                album_length = get_album_length(tracklist)
                if album_length > 0:
                    album_lengths.append(album_length)
            except KeyError:
                print(f"Tracklist not found for release {release_id}")
                continue

        # Choose a length for the album
        if album_lengths:
            average_length = round(sum(album_lengths) / len(album_lengths), 2)
            lengths_list.append(average_length)
            scraped+=1
        else:
            lengths_list.append(0)""")    
                
            with col2:
                st.write("Out of the 3 methods, maybe Wikipedia was the best, because it was easy to code, very fast and **doesn't have any limitation**, unlike the APIs from Discogs or Spotify.\n"
                "From the last one I got banned twice for a period of almost a full day.")
                st.write("There were around 80 albums it couldn't find the length in neither of these places, so I had to look them up manually.  \n"
                "I did many merges and concats until finally get my dataset with info of the ``album_length`` of all the albums.")
                
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.write(" ")
                st.divider()
                st.subheader("Manual cleaning")
                st.write("Still, there were many that were super long, like 2h. In some cases this was the actual length, but in others not, in some cases it was compilations, live albums, just wrong length, etc.")
                st.image("streamlit/images/long_album_length.jpg")
                st.write("I only checked some of them, like the longest 50, because it's a process I could do for days and I wanted to have enough time to analyze the data.")
                st.write("Finally, I decided to check the most prolific artists and see if I detected live albums and compilations, which I did.")

                st.write("I also detected that some data was missing, and I found out it's because the titles were slightly different in the dataframes (from Discogs and from SputnikMusic), like *Honky Château* vs *Honky Chateau*, so I decided to add these albums manually.")
                st.image("streamlit/images/grateful_dead_2.jpg")
                st.write("One particular case was ***Grateful Dead***, which appearead as *The Grateful Dead* in Discogs, so I had no data at all from them.")

            with col3:
                st.image("streamlit/images/live_albums.jpg", width=600)

        if topic == 'Styles':
            with col2:
                st.header("Styles")
                st.write("A bit more than 200 albums didn't have info of ``styles``.  \n"
                "It's a relatively small amount that I could have manually searched for the styles in some other website.")
            
                st.divider()
                st.subheader("Discogs API")
                st.write("However, I thought that even though the main release has no styles, maybe I would find some style in the other releases.")

                st.image("streamlit/images/styles_empty_discogs_master.png")
                st.write(" ")
                st.image("streamlit/images/styles_empty_discogs_release.png")

                st.write("I could find most of the missing styles with this code, and the rest, less than 20, I searched them manually.")

            with col3:
                st.code("""for master_id in df_styles_missing['master_id'].values:
    time.sleep(1)
    count+=1
    url = "https://api.discogs.com/database/search"

    # Define parameters for artist search
    params = {'master_id': master_id}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # create an empty list
    styles_list = []
                    
    # iterate over all the releases
    for i in range(len(data['results'])):
        style = data['results'][i]['style'] # get the style(s)
        if style: 
            styles_list.append(style)
        else:
            styles_list.append(np.nan)

    try:
        most_common_style = pd.Series(styles_list).value_counts().idxmax()
        print(f"{count} - {most_common_style}")
    except:
        print(f'{count} - No styles found')
        most_common_style = np.nan

    most_common_styles.append(most_common_style""")

