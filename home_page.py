# Import packages
from PIL import Image
import requests
from io import BytesIO
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import altair as alt
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Set up paage
st.set_page_config(layout="wide")


# Title and further information
st.write("### Welcome to the Chronic Kidney Disease App")
st.markdown("*This app looks at Chronic Kidney Disease (CKD) prevalance in England and provides visualisations of kidney disease over time, a geographical breakdown of prevalance, and summary statistics.*") 
st.markdown("*Prevalance is calculated as the number of 18+ adults diagnosed with Chronic Kidney Disease divided by the number of 18+ registered patients.*")
st.markdown("*Please allow a few moments for each page to run.*")

# Set up columns 
col1, col2 = st.columns(2)

# Add content
with col1:

    # Add image
    image_url = "https://specials-images.forbesimg.com/imageserve/1012405368/960x0.jpg"  # Replace with your actual otter image URL
    # Make a request to get the image
    response = requests.get(image_url)

    # Open the image using Pillow
    image = Image.open(BytesIO(response.content))

    # Resize the image by setting the height to 400px (adjust as needed)
    new_height = 600
    new_width = int(image.width * (new_height / image.height))

    # Resize the image
    image_resized = image.resize((new_width, new_height))

    # Display the resized image
    st.image(image_resized)

with col2:
    
    # Provide information about the app and what it does/shows
    st.write("### Time Series: ")
    st.markdown("*Visualize Chronic Kidney Disease prevalance over time by NHS defined area.*")

    st.write("### Map Visual: ")
    st.markdown("*Visualise Chronic Kidney Disease prevalance geographically to understand areas where incidences have increased.*")
    
    st.write("### Insights & Recommendations: ")
    st.markdown('*Understand summary statistics as well as the completeness and reliability of the data.*')

    

# Note to provide information about where the data is coming from
st.markdown("*This app uses data from the NHS Quality and Outcomes Framework*")
