# Import packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from PIL import Image
from io import BytesIO
import altair as alt
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pydeck as pdk

st.set_page_config(layout="wide")
# Page title and explanation
st.write("### Average Chronic Kidney Disease Prevalence % Over Time")
st.markdown("*This graph shows a record of chronic kidney disease prevalence over time for selected Sub ICB locations. It allows visual comparison across geographies and years.*")

# Load data from session state

if 'data' in st.session_state:
    df = st.session_state.data.copy()  # Access correctly
    df['Sub ICB Loc name'] = df['Sub ICB Loc name'].str.split(' ICB').str[0].str.strip()
    df['Location'] = df['Sub ICB Loc name']
else:
    st.error("Data not loaded. Please return to the home page to initialize.")
    st.stop()


# Location dropdown filter (slicer)
locations = sorted(df['Location'].unique())
selected_locations = st.multiselect(
    "Select Sub ICB Location(s):",
    options=locations,
    default=[],  # Show first 3 by default or leave as [] for blank
    placeholder="Choose location(s)..."
)



# Filter and plot
if selected_locations:
    filtered_df = df[df['Location'].isin(selected_locations)]

    prevalence_by_year_loc = (
        filtered_df.groupby(['Year', 'Location'])['Prevalence (%)']
        .mean()
        .unstack()
    )

    # Plotting
    
    
    fig, ax = plt.subplots(figsize=(16, 6))
    prevalence_by_year_loc.plot(ax=ax, marker='o', linewidth=2, markersize=4)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Average Prevalence (%)', fontsize=12)
    ax.grid(False)
    fig.patch.set_facecolor('#F7F7F7')
    ax.set_facecolor('#F7F7F7')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.legend(title='Location', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.4)
    ax.xaxis.grid(False)  # Optional: turn off vertical grid lines
    st.pyplot(fig)

    
else:
    st.info("Please select at least one location to view data.")

# Note to provide information about where the data is coming from
# Note to provide information about where the data is coming from
st.markdown("*This app uses data from the NHS Quality and Outcomes Framework*")
