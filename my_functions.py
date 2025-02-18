def check_duplicates_coordinates(df):
    if df['latitude'].duplicated().sum() == 0:
        print('No duplicates')
    else: 
        duplicates = df['latitude'].duplicated().sum()
        print(f'Found {duplicates} duplicates:')
        print(f'{df[df['latitude'].duplicated()][['city', 'country']]}\n')

        df.drop_duplicates(subset='latitude', inplace=True)
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