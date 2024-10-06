import streamlit as st
import json
import os
import ModelDep
import datetime
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

with open('Columns.json', 'r') as file:
            columns = json.load(file)
cityList = columns["City"]
levelsList = columns["Levels"]
homeTypeList = columns["HomeType"]


col1, col2 =st.columns([1, 4])
sidebar = st.sidebar

with sidebar:
    homeType = st.selectbox(label= 'Select Home Type', options=homeTypeList, key=1)
    City = st.selectbox('Select City', options = cityList, key=2)
    level = st.selectbox('Select Number of Stories', options=levelsList, key=3)
    yearBuilt = st.select_slider('Select Year Built', options=range(1850,(datetime.datetime.now().year +1)), key=4)
    livingArea = st.slider('Select Level Area',min_value=100, max_value=6000, step=10, key=5)
    bedRooms = st.slider('How Many Bedrooms', min_value=1, max_value=15, key=6)
    bathRooms = st.slider('How Many Bathrooms', min_value=1, max_value=15, key=7)
    hasParking = st.radio('Parking', options={'Yes': True, 'No':False}, horizontal=True, key=8)
    hasGarage = st.radio('Garage', options={'Yes': True, 'No':False}, horizontal=True, key=9)
    hasPool = st.radio('Pool', options={'Yes': True, 'No':False}, horizontal=True, key=10)
    hasSpa = st.radio('Spa', options={'Yes': True, 'No':False}, horizontal=True, key=11)
    datePosting = st.date_input('When to Buy', value=None, key=12)
    button = st.button('Predict', key=13)