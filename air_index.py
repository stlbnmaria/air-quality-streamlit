import streamlit as st
import pandas as pd
import numpy as np

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
st.title("Air Quality Index (1980-2021)")
data_year, data_day = load_data()

option_timeseries = st.selectbox(
    "", np.unique(data_year["State"]), label_visibility="collapsed"
)


data_state = data_year[data_year["State"] == option_timeseries].reset_index()
filtered_data = data_state[data_state["Year"] == max(data_state["Year"])].reset_index()

col1, col2, col3 = st.columns(3)
col1.metric("Median AQI", int(filtered_data["Median AQI"].mean()), "1.2 °F")
col2.metric("# Good Days", int(filtered_data["Good Days"].mean()), "-8%")
col3.metric("# Unhealthy Days", int(filtered_data["Unhealthy Days"].mean()), "4%")

# map of measuring locations for the air quality index
st.subheader("Locations of Measuring Stations")
st.map(data_state)

# development of the daily air quality per state
st.subheader("Yearly Air Quality per State")
st.line_chart(data_state, x="Year", y="Median AQI", color="County")

# option to show and inspect raw data (for the daily only the first 10k rows are displayed)
st.subheader("Raw Data")
option = st.selectbox(
    "Which dataset do you want to inspect?", ("None", "Daily", "Yearly")
)
if option == "Daily":
    st.dataframe(data_day.iloc[:10000, :])
if option == "Yearly":
    st.dataframe(data_year)
