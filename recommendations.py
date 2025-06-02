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
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.write("### Insights & Recommendations")
st.markdown("*This page provides an overview of statistics related to Chronic Kidney Disease.*")
st.markdown("*Summary statistics are provided alongside geographical locations showing top locations for Chronic Kidney Disease in the UK. Finally some data quality observations are made for clarity as well as potential recommendations for future work.*")

# get session state data
df = st.session_state.data
col1, col2 = st.columns(2)
textColor = "#333333"  


# Please create a top 5 places by prevlance % of ckd
with col1:
    st.write("### Top 5 Areas by CKD Prevalence (%)")
    df_ckd = df[df['Year'] == '2023-24'].copy()
    df_ckd['Prevalence (%)'] = pd.to_numeric(df_ckd['Prevalence (%)'], errors='coerce')
    df_top5 = (
        df_ckd.groupby('Sub ICB Loc name')['Prevalence (%)']
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    st.dataframe(df_top5, use_container_width=True)

# Add recommendations
with col2:
    
    st.write("### Recommendations & Next Steps")
    st.markdown("""
    - **Regional Hotspots** *Clearly Chronic Kidney Disease is affected regionally and this warrants further exploration*.
    - **Inequality Exploration** *Due to the above, it is also worth exploring how inequalities potentially impact on Chronic Kidney Disease*.
    - **Predictive Analytics** *Access to further patient data, could facilitate predictive work to look at which individuals are at risk*.
    - **Integrate Other Datasets** *The integration of other datasets would faciliate more accurate reporting and thus more conclusive insights*.
    - **Causal Inference** *An exploration of reasons as to why certain individuals are likely to experience Chronic Kidney Disease could also highlight individuals at risk*. 
    """)

# Add data information 
col1, col2 = st.columns(2)
with col1:
    st.write("**Data Information**")
    st.markdown('*Data has been cleaned to remove null values as well as those records missing a date. The data is available to the public and is accessed through the NHS Quality and Outcomes Framework and is available [here](https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/general-practice-data-hub/quality-outcomes-framework-qof).*')


# Add contact and project information
with col2:
    st.write("**Contact and Project Information**")
    st.markdown("*For all contact enquiries please email: barnabyrumbold@hotmail.com*")
    st.markdown("*Collaboration is more than welcome, please find the GitHub repository [here](https://github.com/BarnabyRumbold/ckd_app)*")


# Note to provide information about where the data is coming from
st.markdown("*This app uses data from the NHS Quality and Outcomes Framework*")
