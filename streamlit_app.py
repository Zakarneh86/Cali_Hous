import streamlit as st
import json
import os
import ModelDep
import datetime
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#os.system('streamlit run webApp.py')

class WebApp():
    def __init__(self):
        self.Price = 0.0
        with open('Columns.json', 'r') as file:
            columns = json.load(file)
        self.cityList = columns["City"]
        self.levelsList = columns["Levels"]
        self.homeTypeList = columns["HomeType"]

        st.title('California Housing Price Predector')
        self.pageColumns = st.columns((1,1))

        with self.pageColumns[0]:
             self.homeType = st.selectbox(label= 'Select Home Type', options=self.homeTypeList, key=1)
             self.City = st.selectbox('Select City', options = self.cityList, key=2)
             self.level = st.selectbox('Select Number of Stories', options=self.levelsList, key=3)
             self.yearBuilt = st.select_slider('Select Year Built', options=range(1850,2025), key=4)
             self.livingArea = st.slider('Select Level Area',min_value=100, max_value=6000, step=10, key=5)
             self.bedRooms = st.slider('How Many Bedrooms', min_value=1, max_value=15, key=6)
             self.bathRooms = st.slider('How Many Bathrooms', min_value=1, max_value=15, key=7)

        with self.pageColumns[1]:
             self.hasParking = st.radio('Parking', options={'Yes': True, 'No':False}, horizontal=True, key=8)
             self.hasGarage = st.radio('Garage', options={'Yes': True, 'No':False}, horizontal=True, key=9)
             self.hasPool = st.radio('Pool', options={'Yes': True, 'No':False}, horizontal=True, key=10)
             self.hasSpa = st.radio('Spa', options={'Yes': True, 'No':False}, horizontal=True, key=11)
             self.datePosting = st.date_input('When to Buy', value=None, key=12)
             self.button = st.button('Predict', key=13)
             self.predictedPrice = st.empty()

    
    def fitchData(self):
        homeType = self.homeType
        city = self.City
        level = self.level
        yearBuilt = self.yearBuilt
        livingArea = self.livingArea
        bedRooms = self.bedRooms
        bathRooms = self.bathRooms
        hasParking = self.hasParking
        hasGarage = self.hasGarage
        hasPool = self.hasPool
        hasSpa = self.hasSpa
        datePosting = self.datePosting

        if homeType == 'Single Family':
            home = 'SINGLE_FAMILY'
        elif homeType == 'Condo':
            home = 'CONDO'
        elif homeType == 'Townhouse':
            home = 'TOWNHOUSE'

        parking = 1 if hasParking == 'Yes' else 0
        garage = 1 if hasGarage == 'Yes' else 0
        pool = 1 if hasPool == 'Yes' else 0
        spa = 1 if hasSpa == 'Yes' else 0

        age = 2022-yearBuilt

        month = datePosting.month
        if month in [6,7,8]:
            season = 'summer'
        elif month in [9,10,11]:
            season = 'fall'
        elif month in [12,1,2]:
            season = 'winter'
        elif month in [3,4,5]:
            season = 'spring'
        
        df = pd.DataFrame([[level,home, season, city, yearBuilt, livingArea, bathRooms, bedRooms, parking, garage, pool, spa, age ]],columns=['levels', 'homeType', 'postingSeason', 'city', 'yearBuilt','livingAreaValue', 'bathrooms', 'bedrooms', 'parking', 'hasGarage','pool', 'spa', 'Age'])
        return df, True
    
    def printPrice(self, price):
        self.predictedPrice.write(f'Predicted Price: {price} USD')
        

web = WebApp()
model = ModelDep.Model()
model.get_dpnds()
if web.button:
    df, dataFitched = web.fitchData()
    if dataFitched:
        X = model.data_encoding(df)
        price = model.predict(X)
        web.printPrice(price)


