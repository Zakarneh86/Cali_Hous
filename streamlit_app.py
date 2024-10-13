import streamlit as st
import json
import os
import ModelDep
import datetime
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
import time

def dataPrep(homeType, level, yearBuilt, county, city, postal_code, livingArea, bedrooms, bathrooms, hasParking, hasGarage, hasPool, hasSpa, datePosting):
    
    #HomeType
    if homeType == 'Single Family':
            home = 'SINGLE_FAMILY'
    elif homeType == 'Condo':
        home = 'CONDO'
    elif homeType == 'Townhouse':
        home = 'TOWNHOUSE'
    
    # Boolean Data (Parking, Garage, Pool, Spa & Pets)
    parking = 1 if hasParking == 'Yes' else 0
    garage = 1 if hasGarage == 'Yes' else 0
    pool = 1 if hasPool == 'Yes' else 0
    spa = 1 if hasSpa == 'Yes' else 0

    # Age and Age Category
    age = datetime.datetime.now().year - yearBuilt
    if age <= 5:
        ageCat = 'N'
    elif 6 <= age <= 20:
        ageCat = 'RN'
    elif 21 <= age <= 50:
        ageCat = 'MA'
    elif 51 <= age <= 100:
        ageCat = 'O'
    else:
        ageCat = 'VO'
    
    #Posting Season
    month = datePosting.month
    if month in [6,7,8]:
        season = 'summer'
    elif month in [9,10,11]:
        season = 'fall'
    elif month in [12,1,2]:
        season = 'winter'
    elif month in [3,4,5]:
        season = 'spring'
    
    #Postal Code
    try:
        postal_code = int(postal_code)
    except:
        postal_code = 0
    
    df = pd.DataFrame([[home, level, ageCat, season, county, city, postal_code, livingArea, bathrooms, bedrooms, parking, garage, pool, spa, age]],
                      columns = ['homeType', 'levels', 'ageCat', 'postingSeason', 'county', 'city', 'zipcode', 'livingAreaValue','bathrooms', 'bedrooms',
                                  'parking', 'hasGarage', 'pool', 'spa', 'Age'] )

    return df, True


#st.title('California Housing Price Evaluation', )
hide_st_style = """
<h1 style='text-align: center; color: black;'>California Housing Price Evaluation</h1>
<style>
#MainMenue {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
#GithubIcon {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html= True)

geolocator = Nominatim(user_agent="myGeocoder")

latitude, longitude = 37.7749, -122.4194  # San Francisco

with st.container(border=True):
    st.title("Select Location")
    # Create a map centered around the starting point
    with st.container(border=True):
        out1 = st.empty()
        #out2 = st.empty()
        out3 = st.empty()
        out4 = st.empty()
        out1.write(f"**City:**")
        #out2.write(f"**County:**")
        out3.write(f"**Street:**")
        out4.write(f"**Zip Code:**")
    
    with st.container(border=True, height =410):
        map_data =[]
        try:
            geoAPIKey = st.secrets(["openGateAPIKey "])
            gmaps = OpenCageGeocode(key =geoAPIKey)
            m = folium.Map(location=[latitude, longitude], zoom_start=13)
            m.add_child(folium.LatLngPopup())
            map_data = st_folium(m, width=700, height=400)
        except:
            st.write('Error Connecting to Map Provider')
        
        # Check if a location was clicked
        if map_data and map_data['last_clicked']:
            clicked_lat = map_data['last_clicked']['lat']
            clicked_lng = map_data['last_clicked']['lng']

            # Display clicked latitude and longitude
            #st.write(f"Clicked Location: Latitude = {clicked_lat}, Longitude = {clicked_lng}")

            # Perform reverse geocoding using Google Maps API
            reverse_geocode_result = gmaps.reverse_geocode(clicked_lat, clicked_lng)

            if reverse_geocode_result:
                # Get formatted address from the first result
                components = reverse_geocode_result[0]['components']
                #st.write(f"**Address:** {components}")

                # Extract more detailed information (city, street, zip, etc.)
                # Extract the city
                city = components.get('city', 'N/A')
                if city!='N/A':
                    out1.write(f"**City:** {city}")
                
                # Extract the county (administrative_area_level_2 equivalent in OpenCage is "county")
                county = components.get('county', 'N/A')
                '''if county:
                    out2.write(f"**County:** {county}")'''
                
                # Extract the street (equivalent to "road" in OpenCage)
                street = components.get('road', 'N/A')
                house = components.get('house_number', 'N/A')
                if street !='N/A' and house !='N/A':
                    out3.write(f"**Street Address:** {house} {street}")
                elif street !='N/A' and house =='N/A':
                    out3.write(f"**Street Address:** {street}")    
                
                # Extract the postal code
                postal_code = components.get('postcode', 'N/A')
                if postal_code:
                    out4.write(f"**Zip Code:** {postal_code}")
            else:
                st.write("No address found for the given coordinates.")

with open('Columns.json', 'r') as file:
            columns = json.load(file)
levelsList = columns["Levels"]
homeTypeList = columns["HomeType"]

with st.sidebar:
    with st.container():  # container1
        homeType = st.selectbox(label='Select Home Type', options=homeTypeList, key=1)
        level = st.selectbox('Select Number of Stories', options=levelsList, key=3)
        yearBuilt = st.select_slider('Select Year Built', options=range(1850, (datetime.datetime.now().year + 1)), key=4)
        livingArea = st.slider('Select Living Area', min_value=100, max_value=6000, step=10, key=5)
        bedRooms = st.slider('How Many Bedrooms', min_value=1, max_value=15, key=6)
        bathRooms = st.slider('How Many Bathrooms', min_value=1, max_value=15, key=7)

    with st.container():  # container2
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            hasParking = st.radio('Parking', options=['Yes', 'No'], horizontal=True, key=8)
        with col2:
            hasGarage = st.radio('Garage', options=['Yes', 'No'], horizontal=True, key=9)
        with col3:
            hasPool = st.radio('Pool', options=['Yes', 'No'], horizontal=True, key=10)
        with col4:
            hasSpa = st.radio('Spa', options=['Yes', 'No'], horizontal=True, key=11)
        with col5:
            hasPetsAllowed= st.radio('Pets', options=['Yes', 'No'], horizontal=True, key=14)

    with st.container():  # container3
        datePosting = st.date_input('When to Buy', value=datetime.datetime.now(), key=12)
        button = st.button('Predict', key=13)
        predicted = st.empty()

model = ModelDep.Model()
dataReady = False
dataEncoded = False

#Fitch Data from Web Page
if button:
    df, dataReady = dataPrep(homeType, level, yearBuilt, county, city, postal_code, livingArea, bedRooms, bathRooms, hasParking, hasGarage, hasPool, hasSpa, datePosting)

#Encode Data
if dataReady:
    model.get_dpnds()
    X, dataEncoded = model.data_encoding(df)
    dataReady = False
    button = False

#Predict Price
if dataEncoded:
    price = model.predict(X)
    predicted.write(f'Predicted Price is: {price}')
