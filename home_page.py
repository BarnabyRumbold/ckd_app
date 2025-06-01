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

st.set_page_config(layout="wide")

# st.sidebar.markdown("""
#     <div style="text-align: center;">
#         <img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.forbes.com%2Fsites%2Fhelenleebouygues%2F2019%2F11%2F12%2Fputting-the-science-back-into-science-labs%2F&psig=AOvVaw0gtyu2hNSs0vVwfU-EDGw1&ust=1748704853374000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCKC-uq-_y40DFQAAAAAdAAAAABAE" alt="Logo" width="100"/>
#     </div>
# """, unsafe_allow_html=True)


# Title and further information
st.write("### Welcome to the Chronic Kidney Disease App")
st.markdown("*This app looks at Chronic Kidney Disease (CKD) prevalance in England and provides visualisations of kidney disease over time, a geographical breakdown of prevalance, and summary statistics.*") 
st.markdown("*Prevalance is calculated as the number of 18+ adults diagnosed with Chronic Kidney Disease divided by the number of 18+ registered patients.*")
st.markdown("*Please allow a few moments for each page to run.*")

# Set up columns 
col1, col2 = st.columns(2)

# Add content
with col1:

    # Add otter image
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
