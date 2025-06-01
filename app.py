# This file sets up the app and also does the initial data scrape using an API

# Import packages
import streamlit as st
import pandas as pd
import requests
import numpy as np
import io
import json

# Set up pages
pg = st.navigation([
    st.Page("home_page.py", title="Welcome"),
    st.Page("over_time.py", title="Time Series"),
    st.Page("map_visual.py", title="Map Visual"),
    # st.Page("inequalities.py", title="Inequalities"),
    # st.Page("co-morbidities.py", title="Comorbidity Correlation"),
    st.Page("recommendations.py", title="Insights & Recommendations")
])

# URLs and settings
url2324 = 'https://files.digital.nhs.uk/6F/C5E86E/qof-2324-prev-ach-pca-hd-prac.xlsx'
url2223 = 'https://files.digital.nhs.uk/7A/E3DBEA/qof-2223-prev-ach-pca-hd-prac.xlsx'
url2122 = 'https://files.digital.nhs.uk/8A/57C8D5/qof-2122-prev-ach-pca-hd-prac.xlsx'
sheet_name = 'CKD'
geojson_path = 'SICBL_JUL_2022_EN_BFC_-801026854211353459.geojson'

# Function to load data
@st.cache_data
def load_ckd_data(url, sheet_name):
    response = requests.get(url)
    response.raise_for_status()
    with io.BytesIO(response.content) as data:
        df = pd.read_excel(data, sheet_name=sheet_name, header=11)
        df.columns = df.columns.str.strip().str.replace('\n', '').str.replace('\r', '')
        df['Prevalence (%)'] = pd.to_numeric(df['Prevalence (%)'], errors='coerce')
        df = df[['Sub ICB Loc ONS code', 'Practice name', 'Prevalence (%)', 'Sub ICB Loc name']].copy()
        df = df.dropna()
        df['Sub ICB Loc ONS code'] = df['Sub ICB Loc ONS code'].astype(str).str.strip().str.upper()
    return df

if 'kidney_data' not in st.session_state:
    try:
        # Load and clean CKD data
        df_2324 = load_ckd_data(url2324, sheet_name)
        df_2223 = load_ckd_data(url2223, sheet_name)
        df_2122 = load_ckd_data(url2122, sheet_name)

        df_2324['Year'] = '2023-24'
        df_2223['Year'] = '2022-23'
        df_2122['Year'] = '2021-22'

        df_all_years = pd.concat([df_2324, df_2223, df_2122], ignore_index=True).dropna()

        st.session_state.data = df_all_years
        st.session_state.kidney_data = True

        # Load and clean GeoJSON
        with open(geojson_path, "r") as f:
            geojson_data = json.load(f)

        for feature in geojson_data['features']:
            code = feature['properties'].get('SICBL22CD', '')
            feature['properties']['SICBL22CD'] = str(code).strip().upper()

        st.session_state.geojson = geojson_data
        st.session_state.geojson_codes = {
            feature['properties']['SICBL22CD'] for feature in geojson_data['features']
        }

    except Exception as e:
        st.error(f"Failed to load data: {e}")

# Run the selected page
pg.run()