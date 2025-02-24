import numpy as np
import pandas as pd
from pandas import json_normalize

from bs4 import BeautifulSoup
import requests 
import time
import re

# pip install geopy
from geopy.geocoders import Nominatim

import warnings
warnings.filterwarnings("ignore")
from my_functions import *


def get_origins_wikipedia(df, start_index, final_index):
    df = pd.read_csv('Datasets/df_rock_ratings.csv')
    artists = df['artist'].unique()

    try:
    # import the DataFrame with the locations whose coordinates I already have
        df_coordinates_scraped = pd.read_csv('Datasets/df_coordinates.csv')
        print('Bingo! df_coordinates.csv found \n')
    except: 
        print('df_coordinates.csv not found \n')

    artists_list = []
    origin_list = []
    count=0
    scraped=0

    for index in artists[start_index:final_index]:

        name_changed = index.replace(' ', '_')
        name_changed_band = name_changed + ('_(band)')
        name_changed_musician = name_changed + ('_(musician)')

        try:
            url = f"https://en.wikipedia.org/wiki/{name_changed_band}"
            response = requests.get(url).content
            soup = BeautifulSoup(response, "html.parser")

            table = soup.select('#mw-content-text > div.mw-content-ltr.mw-parser-output > table.infobox')

            location = table[0].text.split('Origin')[1].split('Genres')[0]
            count+=1
            
        # save info in lists
            artists_list.append(index)  
            origin_list.append(location)
            scraped+=1
            print(f'{scraped}/{count} - {name_changed_band}: {location}')

        except:
            try:
                url = f"https://en.wikipedia.org/wiki/{name_changed}"
                response = requests.get(url).content
                soup = BeautifulSoup(response, "html.parser")
                table = soup.select('#mw-content-text > div.mw-content-ltr.mw-parser-output > table.infobox')

                try:
                    location = table[0].text.split('Origin')[1].split('Genres')[0]
                    count+=1 
    
                # save info in lists
                    artists_list.append(index)  
                    origin_list.append(location)
                    scraped+=1
                    print(f'{scraped}/{count} - {name_changed}: {location}')

                except:
                    text = table[0].text

                    # Step 1: Extract the part after 'Born'
                    after_born = text.split("Born", 1)[1]

                    text_age = re.search("aged", after_born)

                    if text_age:
                        # This means the artist is dead
                        location = re.split(r'(19\d{2})', after_born)[4].split('Died')[0].strip()
                    else:
                        try:
                            text = re.split(r'(19\d{2})', after_born)[4].split(')')[1]

                            if "Other\xa0names" in text:
                                location = text.split('Other\xa0names')[0]
                            else:
                                if "Citizenship" in text:
                                    location = text.split('Citizenship')[0]
                                else:
                                    if "Genres" in text:
                                        location = text.split('Genres')[0]
                                    else:
                                        if "Occupations" in text:
                                            location = text.split('Occupations')[0]
                                        else:
                                            location = np.nan
                        except:  
                            location = np.nan
                    count+=1

                # save info in lists
                    artists_list.append(index)  
                    origin_list.append(location)
                    scraped+=1
                    print(f'{scraped}/{count} - {name_changed} (individual): {location}')

            except:
                try:
                    url = f"https://en.wikipedia.org/wiki/{name_changed_musician}"
                    response = requests.get(url).content
                    soup = BeautifulSoup(response, "html.parser")
                    table = soup.select('#mw-content-text > div.mw-content-ltr.mw-parser-output > table.infobox')

                    try:
                        location = table[0].text.split('Origin')[1].split('Genres')[0]
                        count+=1 
        
                    # save info in lists
                        artists_list.append(index)  
                        origin_list.append(location)
                        scraped+=1
                        print(f'{scraped}/{count} - {name_changed}: {location}')

                    except:
                        text = table[0].text

                        # Step 1: Extract the part after 'Born'
                        after_born = text.split("Born", 1)[1]

                        text_age = re.search("aged", after_born)

                        if text_age:
                            # This means the musician is dead
                            location = re.split(r'(19\d{2})', after_born)[4].split('Died')[0].strip()
                        else:
                            try:
                                text = re.split(r'(19\d{2})', after_born)[4].split(')')[1]

                                if "Other\xa0names" in text:
                                    location = text.split('Other\xa0names')[0]
                                else:
                                    if "Citizenship" in text:
                                        location = text.split('Citizenship')[0]
                                    else:
                                        if "Genres" in text:
                                            location = text.split('Genres')[0]
                                        else:
                                            if "Occupations" in text:
                                                location = text.split('Occupations')[0]
                                            else:
                                                location = np.nan
                            except:  
                                location = np.nan
                        count+=1

                    # save info in lists
                        artists_list.append(index)  
                        origin_list.append(location)
                        scraped+=1
                        print(f'{scraped}/{count} - {name_changed} (musician): {location}')

                except:
                    try:
                        url = f"https://es.wikipedia.org/wiki/{name_changed}"
                        response = requests.get(url).content
                        soup = BeautifulSoup(response, "html.parser")

                        table = soup.select('#mw-content-text > div.mw-content-ltr.mw-parser-output > table.infobox')
                        location = table[0].text.split('Origen\n')[1].split(' Información')[0]
                        count+=1    
        
                    # save info in lists
                        artists_list.append(index)  
                        origin_list.append(location)
                        scraped+=1
                        print(f'{scraped}/{count} - {name_changed} (español): {location}')

                    except:
                        count+=1
                        print(f'{scraped}/{count} - {index}: error')
                        artists_list.append(index) 
                        origin_list.append(np.nan)

        if len(artists_list) != len(origin_list):
            print('different lengths')
            break

    df_artists_origins = pd.DataFrame({'artist': artists_list
                             , 'origin': origin_list})
    
    return df_artists_origins


def get_new_artists(df_artists_origins):
    # import the df with the artists' origins already scraped
    df_artists_origins_scraped = pd.read_csv('Datasets/df_artists_origins.csv')

    if df_artists_origins['origin'].isna().sum() == 0:        
        print("No null values, but let's take a look just in case there are weird locations")

    else: 
    # take a look at the df with the new artists and make sure there are non null values in origin (when it couldn't find it in Wikipedia)
        print(f'{df_artists_origins['origin'].isna().sum()} nulls ({round(df_artists_origins['origin'].isna().sum() / df_artists_origins.shape[0]*100, 2)} %)')
    
    # subset of the new artists I just got, wether there are null values or not
    df_new_artists = df_artists_origins[~df_artists_origins['artist'].isin(df_artists_origins_scraped['artist'].values)]

    return df_new_artists   # so I can take a look at it and then continue


def export_artists_origins_concat(df_new_artists):
    # import the df with the artists' origins already scraped
    df_artists_origins_scraped = pd.read_csv('Datasets/df_artists_origins.csv')

    # concat with the df I just got
    df_artists_origins_concat = pd.concat([df_artists_origins_scraped, df_new_artists])
    df_artists_origins_concat.drop_duplicates(inplace=True)     # just in case
    df_artists_origins_concat.reset_index(drop=True, inplace=True)

    # export all the artists and their origins to a .csv file (the ones I got plus the new artists)
    df_artists_origins_concat.to_csv('Datasets/df_artists_origins.csv', index=False)
    print('df_artists_origins_concat exported to .csv')
    print(df_artists_origins_concat.shape)


def get_coordinates_geopy(df_new_artists):
    
    # replace special characters for spaces
    df_new_artists['origin_clean'] = df_new_artists['origin'].str.replace('.', '')
    df_new_artists['origin_clean'] = df_new_artists['origin_clean'].str.replace(r'\[\d+\]', '', regex=True)

    # run the function that gets the coordinates from the origins from Geopy
    geolocator = Nominatim(user_agent="music_analysis", timeout=10)

    # if they are 'dirty' origins that after the cleaning, they result in the same 'origin_clean'
    df_unique = df_new_artists[['origin', 'origin_clean']].drop_duplicates() 
    unique_origins = df_unique['origin'].values
    unique_origins_clean = df_unique['origin_clean'].values

    country_list = []
    city_list = []
    latitude_list = []
    longitude_list = []
    address_list = []
    count = 0

    for origin in unique_origins_clean:
        count+=1
        time.sleep(1)
        location = geolocator.geocode(origin)

        print(f'{count}/{len(unique_origins_clean)} - {location.address}')  

    # save the info in lists
        country_list.append(location.address.split(', ')[-1])
        city_list.append(origin.split(', ')[0])
        latitude_list.append(location.latitude)
        longitude_list.append(location.longitude)
        address_list.append(location.address)

    df_coordinates = pd.DataFrame({'country': country_list
                                , 'city': city_list
                                , 'origin': unique_origins
                                , 'origin_clean': unique_origins_clean
                                , 'latitude': latitude_list
                                , 'longitude': longitude_list
                                , 'address': address_list})
    df_coordinates.sort_values(['country', 'city'], inplace=True) # sort by country and city
    df_coordinates.reset_index(drop=True, inplace=True)

    return df_coordinates


def export_coordinates_concat(df_coordinates):
    # import the last df that contains the coordinates of the unique origins
    df_coordinates_scraped = pd.read_csv('Datasets/df_coordinates.csv')
    print(f"df_coordinates_scraped: {df_coordinates_scraped.shape}\n")

    # concat with the df of the coordinates I just got
    df_coordinates_concat = pd.concat([df_coordinates_scraped, df_coordinates])
    df_coordinates_concat.sort_values(['country', 'city'], inplace=True) # sort by country and city
    df_coordinates_concat.reset_index(drop=True, inplace=True)

    # look for duplicates in the origin, between the locations I had already gotten and the new ones
    check_duplicates_origins(df_coordinates_concat)
    new_origins = df_coordinates_concat.shape[0] - df_coordinates_scraped.shape[0]
    print(f"Merged artists with coordinates! Found {new_origins} new locations")

    # save it in a csv file (the coordinates I had plus the ones from the new artists I just got)
    df_coordinates_concat.to_csv('Datasets/df_coordinates.csv', index=False)
    print('df_coordinates_concat exported to .csv')


def merge_origins_coordinates(df_new_artists):
    # import the last df that contains the coordinates of the unique origins
    df_coordinates_concat = pd.read_csv('Datasets/df_coordinates.csv')

    # merge with the previous df with the artists
    df_artists_origins_coordinates = pd.merge(df_new_artists, df_coordinates_concat, on=['origin'])
    df_artists_origins_coordinates.drop(columns=['origin', 'origin_clean_x', 'origin_clean_y'], inplace=True)

    # import the df that contains info of the artists and the coordinates of their origins
    df_artists_origins_coordinates_scraped = pd.read_csv('Datasets/df_artists_origins_coordinates.csv')

    # concat to get the df with all the artists, origins and their coordinates
    df_artists_origins_coordinates_concat = pd.concat([df_artists_origins_coordinates_scraped, df_artists_origins_coordinates])
    df_artists_origins_coordinates_concat.reset_index(drop=True, inplace=True)

    # save it in a csv file
    df_artists_origins_coordinates_concat.to_csv('Datasets/df_artists_origins_coordinates.csv', index=False)
    print("Exported to a .csv file")

    return df_artists_origins_coordinates_concat