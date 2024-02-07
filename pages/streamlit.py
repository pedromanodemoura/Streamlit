# -*- coding: utf-8 -*-
"""
Created on Mon May  8 11:14:53 2023

@author: c20460
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import random, string
import json
import pyperclip
import folium
from streamlit_folium import st_folium, folium_static

rent_data = pd.read_csv('./rent_data.csv')

rent_text = ''
m = folium.Map(location=[rent_data.latitude.mean(), rent_data.longitude.mean()], 
                 zoom_start=3, control_scale=True)

sw = [i - 0.005 for i in rent_data[['latitude', 'longitude']].min().values.tolist()]
ne = [i + 0.005 for i in rent_data[['latitude', 'longitude']].max().values.tolist()]
m.fit_bounds([sw, ne])

for i, row in rent_data.iterrows():

    row_text = f'''<div>
    <h3><a href="{row['url']}">{row['address']}</a></h3>
    <p><b>Type:</b> {row['type']}</p>
    <p><b>Price:</b> {row['price']}</p>
    <p><b>Bedrooms:</b> {row['bedrooms']}</p>
    <p><b>Bathrooms:</b> {row['bathrooms']}</p>
    <p><b>Area:</b> {'' if pd.isna(row['area']) else row['area']}</p>
    </div>'''
    
    rent_text += row_text + '<br>'

    if pd.isna(row['latitude']):
        continue

    #Setup the content of the popup
    iframe = folium.IFrame(row_text, height=220, width = 310)
    
    #Initialise the popup using the iframe
    popup = folium.Popup(iframe, min_width=300, max_width=450)
    
    #Add each row to the map
    folium.Marker(location=[row['latitude'],row['longitude']],
                  popup = popup, c=row['address']).add_to(m)
                  

st_data = folium_static(m, width=700)

st.markdown(rent_text, unsafe_allow_html=True)


    

