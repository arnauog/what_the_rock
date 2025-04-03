import streamlit as st
from streamlit_functions import *
import pandas as pd
import numpy as np

df = pd.read_csv('Datasets/df_final.csv')
st.title('Best albums of every rock style')

st.markdown("""<style>
    div[data-baseweb="select"] {
        width: 300px !important;  /* Adjust width as needed */}
    </style>
    """,
    unsafe_allow_html=True)

st.markdown("""<style>
div[data-testid="stNumberInput"] {
    width: 200px !important;  /* Adjust width as needed */}
</style>
""",
unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.5, 0.4, 0.1])
with col1:
    subgenre = st.selectbox(':mag: **Subgenre**', ['Select a subgenre']+list(df["subgenre"].unique()))

    if subgenre != 'Select a subgenre':
        get_style(df, subgenre, col2)
