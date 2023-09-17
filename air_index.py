import streamlit as st
import pandas as pd
import numpy as np
import datetime

DATE_COLUMN = "date/time"
DATA_DAILY = "data/aqi_daily_1980_to_2021.csv"
DATA_YEARLY = "data/aqi_yearly_1980_to_2021.csv"


@st.cache_data
def load_data():
    data_year = pd.read_csv(DATA_YEARLY)
    data_day = pd.read_csv(DATA_DAILY)
    data_year.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)
    return data_year, data_day


st.set_page_config(layout="wide")
st.title("EPA Air Quality Index")
data_year, data_day = load_data()

with st.sidebar:
    st.subheader("Filter Options")
    option_state = st.selectbox("State:", np.unique(data_year["State"]))

    option_time = st.slider(
        "Year:", min(data_year["Year"]), max(data_year["Year"]), 2020
    )

data_state = data_year[data_year["State"] == option_state].reset_index(drop=True)
date_time = data_state[data_state["Year"] == option_time].reset_index(drop=True)
date_prev = data_state[data_state["Year"] == (option_time - 1)].reset_index(drop=True)

# KPIs
st.subheader(f"KPIs for {option_state}")
col0, col1, col2, col3 = st.columns(4)
col0.metric(
    "\# Measuring Stations",
    date_time["County"].nunique(),
    date_time["County"].nunique() - date_prev["County"].nunique(),
)
col1.metric(
    "Median AQI",
    int(date_time["Median AQI"].mean()),
    int(date_time["Median AQI"].mean() - date_prev["Median AQI"].mean()),
)
col2.metric(
    "\# Good Days",
    int(date_time["Good Days"].mean()),
    int(date_time["Good Days"].mean() - date_prev["Good Days"].mean()),
)
col3.metric(
    "\# Unhealthy Days",
    int(date_time["Unhealthy Days"].mean()),
    int(date_time["Unhealthy Days"].mean() - date_prev["Unhealthy Days"].mean()),
)

# development of the daily air quality per state
st.subheader(f"Median AQI per County in {option_state}")
st.line_chart(data_state, x="Year", y="Median AQI", color="County")

# map of measuring locations for the air quality index
# TODO: fix map refresh issue - streamlit bug, look into pydeck
st.subheader(f"Locations of Measuring Stations in {option_state}")
st.map(date_time)

# option to show and inspect raw data (for the daily only the first 10k rows are displayed)
st.subheader("Raw Data for all States")
option = st.selectbox(
    "Select periodicity of the data:", ("None", "Daily", "Yearly")
)
if option == "Daily":
    st.write("This prompt is limited to 50k rows to ensure the speed of the application.")
    st.dataframe(data_day.iloc[:50000, :])
if option == "Yearly":
    st.dataframe(data_year)
