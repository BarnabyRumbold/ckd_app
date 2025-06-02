# Import packages

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from shapely.geometry import shape

# Set page layout
st.set_page_config(layout="wide")
st.write("### Average Chronic Kidney Disease % Prevalence (2023–2024)")
st.markdown(
    "*This visual shows CKD prevalence geographically for 2023–24. This helps highlight areas with higher or lower average rates of CKD based on NHS data.*"
)
st.markdown("*Please allow a few moments for this page to run.*")

# Get data
if 'data' not in st.session_state or 'geojson' not in st.session_state:
    st.error("Data or GeoJSON not loaded.")
    st.stop()
    


@st.cache_data
def filter_group_data(data):
    df_2324 = data[data['Year'] == '2023-24'].copy()
# Strip & uppercase codes & names to ensure consistency
    df_2324['Sub ICB Loc ONS code'] = df_2324['Sub ICB Loc ONS code'].astype(str).str.strip().str.upper()
    df_2324['Sub ICB Loc name'] = df_2324['Sub ICB Loc name'].astype(str).str.strip()
# Ensure Prevalence (%) is numeric
    df_2324['Prevalence (%)'] = pd.to_numeric(df_2324['Prevalence (%)'], errors='coerce')
# Filter out rows with null Prevalence
    df_2324 = df_2324.dropna(subset=['Prevalence (%)'])
    df_grouped = (
        df_2324.groupby(['Sub ICB Loc ONS code', 'Sub ICB Loc name'])['Prevalence (%)']
        .mean()
        .reset_index()
    )
    return df_grouped

df_grouped = filter_group_data(st.session_state.data)
# Get all codes from GeoJSON
geojson_codes = {
    feature['properties']['SICBL22CD']
    for feature in st.session_state.geojson['features']
}


min_val = 0
max_val = max(10, df_grouped['Prevalence (%)'].max())  # ensure enough room

# Process geojson codes with consistent formatting
geojson = st.session_state.geojson

geojson_codes = set()
for feature in geojson['features']:
    code = feature['properties'].get('SICBL22CD')
    if code:
        geojson_codes.add(str(code).strip().upper())


# Enforce formatting on df_grouped codes (again, just to be safe)
df_grouped['Sub ICB Loc ONS code'] = df_grouped['Sub ICB Loc ONS code'].str.strip().str.upper()
df_grouped['Sub ICB Loc name'] = df_grouped['Sub ICB Loc name'].str.replace(r' ICB.*', '', regex=True)

# Plot

fig = px.choropleth_mapbox(
    df_grouped,
    geojson=geojson,
    locations='Sub ICB Loc ONS code',
    color='Prevalence (%)',
    featureidkey="properties.SICBL22CD",
    hover_name='Sub ICB Loc name',
    hover_data={
        'Prevalence (%)': ':.2f',
        'Sub ICB Loc ONS code': False  # hide the code in tooltip just in case
    },
    color_continuous_scale="YlGnBu",
    range_color=(min_val, max_val),
    mapbox_style="carto-positron",
    center={"lat": 53.5, "lon": -1.5},
    zoom=5,
    opacity=0.7,
)
fig.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0},
    coloraxis_colorbar=dict(title="Avg CKD Prevalence (%)", ticksuffix="%"),
)

st.plotly_chart(fig, use_container_width=True)
# Note to provide information about where the data is coming from
st.markdown("*This app uses data from the NHS Quality and Outcomes Framework*")
