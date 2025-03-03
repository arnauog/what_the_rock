import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

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
        fig, ax = plt.subplots(figsize=(5,5))
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
        st.header('Price per model')
        price_per_model = df.pivot_table(values="price", index="model", aggfunc='mean').sort_values(['price'], ascending=False).astype({'price': int}) # mean price per model
        fig, ax = plt.subplots(figsize=(10,20))
        sns.barplot(data=price_per_model, y='model', x='price')
        st.pyplot(fig)

elif selection == 'Search for styles':
    st.title('Best albums of every rock style')
    st.image('https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cm9jayUyMGNvbmNlcnR8ZW58MHx8MHx8fDA%3D')
    st.subheader('Features :mag:')

    subgenre = st.selectbox(':musical_note: **Subgenre**', [None, 'Roots Rock', 'Classic Rock', 'Metal', 'Punk', 'Indie Rock'])
    if subgenre is None:
        st.write("Please select a subgenre.")
    else: # show the rest of the features once the user has selected a brand

        # define the different models depending on the brand selected
        if subgenre == 'Roots Rock':
            st.image('https://i.ytimg.com/vi/SQUNCM7oHj8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAJHyeUPUJjpCAYNJe8rRS3KFiH4A')
            style = st.radio(':oncoming_automobile: **Model**', [None, "Folk Rock", "Blues Rock", "Rock & Roll", "Soft Rock", "Country Rock", "Southern Rock"])
            if style is None:
                pass
            elif model =='Citan':
                st.image('images/van_models/Mercedes-Benz/Citan.jpg')
            elif model =='Marco Polo':
                st.image('images/van_models/Mercedes-Benz/Marco Polo.jpg')
            elif model =='Sprinter':
                st.image('images/van_models/Mercedes-Benz/Sprinter.jpg')
            elif model =='T':
                st.image('images/van_models/Mercedes-Benz/T.jpg')
            elif model =='V':
                st.image('images/van_models/Mercedes-Benz/V.jpg')
            elif model =='Viano':
                st.image('images/van_models/Mercedes-Benz/Viano.jpg')
            else:
                st.image('images/van_models/Mercedes-Benz/Vito.jpg')

        elif brand == 'Hyundai':
            st.image('images/logos/Hyundai.jpg')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'H-1', 'Staria'])
            if model is None:
                pass
            elif model =='H-1':
                st.image('images/van_models/Hyundai/H-1.jpg')
            else:
                st.image('images/van_models/Hyundai/Staria.jpg')

        elif brand == 'Nissan':
            st.image('images/logos/Nissan.png')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'NV200', 'NV300', 'NV400', 'Townstar', 'Primastar'])
            if model is None:
                pass
            elif model =='NV200':
                st.image('images/van_models/Nissan/NV200.png')
            elif model =='NV300':
                st.image('images/van_models/Nissan/NV300.jpg')
            elif model =='NV400':
                st.image('images/van_models/Nissan/NV400.png')
            elif model =='Townstar':
                st.image('images/van_models/Nissan/Townstar.jpg')
            else:
                st.image('images/van_models/Nissan/Primastar.jpg')

        elif brand == 'Volkswagen':
            st.image('images/logos/Volkswagen.png')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Caddy', 'Crafter', 'Grand California', 'Multivan', 'T4', 'T5', 'T6', 'T7'])
            if model is None:
                pass
            elif model =='Caddy':
                st.image('images/van_models/Volkswagen/Caddy.jpg')
            elif model =='Crafter':
                st.image('images/van_models/Volkswagen/Crafter.jpg')
            elif model =='Grand California':
                st.image('images/van_models/Volkswagen/Grand California.jpg')
            elif model =='Multivan':
                st.image('images/van_models/Volkswagen/Multivan.jpg')
            elif model =='T4':
                st.image('images/van_models/Volkswagen/T4.jpg')
            elif model =='T5':
                st.image('images/van_models/Volkswagen/T5.jpeg')
            elif model =='T6':
                st.image('images/van_models/Volkswagen/T6.jpg')
            else:
                st.image('images/van_models/Volkswagen/T7.jpg')

        elif brand == 'Toyota':
            st.image('images/logos/Toyota.png')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Proace'])
            if model is None:
                pass
            else:
                st.image('images/van_models/Toyota/Proace.jpg')

        elif brand == 'Ford':
            st.image('images/logos/Ford.png')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Connect', 'Custom', 'Transit'])
            if model is None:
                pass
            elif model =='Connect':
                st.image('images/van_models/Ford/Connect.jpg')
            elif model =='Custom':
                st.image('images/van_models/Ford/Custom.jpg')
            else:
                st.image('images/van_models/Ford/Transit.jpg') 

        elif brand == 'Opel':
            st.image('images/logos/Opel.jpg')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Combo', 'Movano', 'Vivaro', 'Zafira'] )
            if model is None:
                pass
            elif model =='Combo':
                st.image('images/van_models/Opel/Combo.jpg')
            elif model =='Movano':
                st.image('images/van_models/Opel/Movano.jpg')
            elif model =='Vivaro':
                st.image('images/van_models/Opel/Vivaro.jpg')
            else:
                st.image('images/van_models/Opel/Zafira.jpg')

        elif brand == 'Peugeot':
            st.image('images/logos/Peugeot.jpg')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Boxer', 'Partner', 'Rifter', 'Traveller'])
            if model is None:
                pass
            elif model =='Boxer':
                st.image('images/van_models/Peugeot/Boxer.jpg')
            elif model =='Partner':
                st.image('images/van_models/Peugeot/Partner.png')
            elif model =='Rifter':
                st.image('images/van_models/Peugeot/Rifter.jpg')
            else:
                st.image('images/van_models/Peugeot/Traveller.jpg')

        elif brand == 'Citroën':
            st.image('images/logos/Citroen.png')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Berlingo', 'Jumper', 'Jumpy', 'SpaceTourer'])
            if model is None:
                pass
            elif model =='Berlingo':
                st.image('images/van_models/Citroën/Berlingo.png')
            elif model =='Jumper':
                st.image('images/van_models/Citroën/Jumper.png')
            elif model =='Jumpy':
                st.image('images/van_models/Citroën/Jumpy.jpg')
            else:
                st.image('images/van_models/Citroën/SpaceTourer.png')

        elif brand == 'Renault':
            st.image('images/logos/Renault.jpg')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Kangoo', 'Master', 'Trafic'])
            if model is None:
                pass
            elif model =='Kangoo':
                st.image('images/van_models/Renault/Kangoo.jpg')
            elif model =='Master':
                st.image('images/van_models/Renault/Master.jpg')
            else:
                st.image('images/van_models/Renault/Trafic.jpg')

        elif brand == 'Fiat':
            st.image('images/logos/Fiat.jpg')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Doblo', 'Ducato', 'Fiorino', 'Qubo', 'Scudo', 'Talento'])
            if model is None:
                pass
            elif model =='Doblo':
                st.image('images/van_models/Fiat/Doblo.jpg')
            elif model =='Ducato':
                st.image('images/van_models/Fiat/Ducato.jpg')
            elif model =='Fiorino':
                st.image('images/van_models/Fiat/Fiorino.jpg')
            elif model =='Qubo':
                st.image('images/van_models/Fiat/Qubo.png')
            elif model =='Scudo':
                st.image('images/van_models/Fiat/Scudo.jpg')
            else:
                st.image('images/van_models/Fiat/Talento.jpg')

        elif brand == 'Dacia':
            st.image('images/logos/Dacia.png')
            model = st.radio(':oncoming_automobile: **Model**', [None, 'Dokker'])
            if model is None:
                pass
            else:
                st.image('images/van_models/Dacia/Dokker.jpg')

        if model in model_expensive:
            model_price_value = 2
        elif model in model_medium:
            model_price_value = 1
        else:
            model_price_value = 0

        # rest of the features
        if model is None:
            st.write("Please select a model.")
        else: # show the rest of the features once the user has selected a brand
            age = st.number_input(':calendar: Age of the van', min_value=1, max_value=30, step=1)
            km = st.number_input(':straight_ruler: Mileage in km:', min_value=0, max_value=1000000, step=1)
            
            fuel_input = st.radio(':fuelpump: Fuel:', ['Diesel', 'Gasoline'])
            fuel_dict = {'Diesel': 0, 'Gasoline': 1}
            fuel_value = fuel_dict[fuel_input]

            power_cv = st.number_input(':horse: Horsepower in cv:', min_value=50, step=1)
            consumption = st.number_input(':heavy_dollar_sign: Consumption in L/100km:', min_value=4.0, step=0.1, format="%.1f")

            owners_input = st.radio(':key: Previous owners:', ['One', 'More than one'])
            owners_dict = {'One': 0, 'More than one': 1}
            owners_value = owners_dict[owners_input]

            doors_input = st.radio(':door: Does it have both rear doors:', ['Yes', 'No, only the right one'])
            doors_dict = {'Yes': 1, 'No, only the right one': 0}
            rear_doors = doors_dict[doors_input]

            cargo_input = st.radio(':package: Is it a cargo van?', ['Yes', 'No'])
            cargo_dict = {'Yes': 1, 'No': 0}
            cargo_value = cargo_dict[cargo_input]

            size_big = ['Grand California', 'Sprinter', 'Crafter', 'Transit', 'Movano', 'Ducato', 'Master', 'Boxer', 'NV400', 'Jumper']
            size_medium = ['Marco Polo', 'V', 'T7', 'Multivan', 'Staria', 'T6', 'Zafira', 'Traveller', 'SpaceTourer', 'Vito', 'Proace', 'Custom', 'Primastar', 'Trafic', 'NV300', 'Viano',
                        'Talento', 'H-1', 'Vivaro', 'T5', 'Jumpy', 'Scudo', 'T4']
            size_small = ['T', 'Townstar', 'Caddy', 'Rifter', 'Citan', 'Connect', 'Combo', 'Berlingo', 'Dokker', 'NV200', 'Kangoo', 'Partner', 'Doblo', 'Fiorino', 'Qubo']

            if model in size_big:
                van_size = 2
            elif model in size_medium:
                van_size = 1
            else:
                van_size = 0

            # Machine Learning model
            df = pd.read_csv('Datasets/df_final.csv')
            numericals = df.select_dtypes(np.number)  # Select numerical variables
            y = numericals['price']
            X = numericals.drop(columns=['price'])
            X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.85, random_state=42)

            # Scale the features
            scaler = StandardScaler()
            scaled_X_train = scaler.fit_transform(X_train)
            scaled_X_test = scaler.transform(X_test)

            # Make the prediction with the trained KNN model
            knn_reg = KNeighborsRegressor(n_neighbors=5, weights='distance', metric='manhattan')
            knn_reg.fit(scaled_X_train, y_train)

            input_features = [age, km, power_cv, consumption, fuel_value, owners_value, rear_doors, cargo_value, brand_price_value, model_price_value, van_size]

            # Scale the input (same scaling transformation as for training data)
            input_data = scaler.transform([input_features])
            prediction = knn_reg.predict(input_data)

            st.header(f'This van would cost:')

            if st.button('Calculate price'):
                # print the predicted price
                st.header(f'This van would cost {prediction[0].astype(int)} €')

            # let's put a funny image depending on the price
                if prediction > 50000:
                    st.image('https://i2.cdn.turner.com/money/dam/assets/130926155851-breaking-bad-cash-640x360.jpg')
                elif prediction < 15000:
                    st.image('https://i.pinimg.com/originals/d4/77/d6/d477d6acbd276d21705048626822c009.gif')
                else: 
                    st.image('https://miro.medium.com/v2/resize:fit:1000/0*UVhb_mFUjRECuaWm.gif')




