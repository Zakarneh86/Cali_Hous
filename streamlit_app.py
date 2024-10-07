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
import googlemaps

with st.container(border=True, height=800):
    geolocator = Nominatim(user_agent="myGeocoder")

    st.title("Map to Select Location")

    gmaps = googlemaps.Client(key ='AIzaSyBcCiJ1cZaPWUOxZPQwNA3onKGRcKe_mMY')

    latitude, longitude = 37.7749, -122.4194  # San Francisco
    # Create a map centered around the starting point
    m = folium.Map(location=[latitude, longitude], zoom_start=13)
    m.add_child(folium.LatLngPopup())
    clicked_location = st_folium(m, width=700, height=500)
    # Check if a location was clicked
    if clicked_location and clicked_location['last_clicked']:
        lat = clicked_location['last_clicked']['lat']
        lon = clicked_location['last_clicked']['lng']
        st.write(f"**lon:** {lon} **lat**: {lat}")
        # Perform reverse geocoding to get address information
        try:
            location = gmaps.reverse("{}, {}".format(lat, lon), exactly_one=False, language="en")
        except:
            location = None

        if location:
            address = location.address
            st.write(f"**Address:** {address}")

            # Extract details from the address
            address_details = location.raw['address']
            
            city = address_details.get('city', '')
            county = address_details.get('county', '')
            street = address_details.get('road', '')
            zip_code = address_details.get('postcode', '')

            st.write(f"**City:** {city}")
            st.write(f"**County:** {county}")
            st.write(f"**Street:** {street}")
            st.write(f"**Zip Code:** {zip_code}")
        else:
            st.write("No address found for this location.")


with open('Columns.json', 'r') as file:
            columns = json.load(file)
cityList = columns["City"]
levelsList = columns["Levels"]
homeTypeList = columns["HomeType"]

with st.sidebar:
    with st.container():  # container1
        homeType = st.selectbox(label='Select Home Type', options=homeTypeList, key=1)
        level = st.selectbox('Select Number of Stories', options=levelsList, key=3)
        yearBuilt = st.select_slider('Select Year Built', options=range(1850, (datetime.datetime.now().year + 1)), key=4)
        livingArea = st.slider('Select Level Area', min_value=100, max_value=6000, step=10, key=5)
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
