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


st.title("Air Quality Index (1980-2021)")
data_year, data_day = load_data()

# map of measuring locations for the air quality index
st.subheader("Locations of Measuring Stations")
filtered_data = data_year[data_year["Year"] == max(data_year["Year"])]
st.map(filtered_data)

# development of the daily air quality per state
st.subheader("Yearly Air Quality per State")
option_timeseries = st.selectbox(
    "Which state do you want to inspect?", np.unique(data_year["State"])
)
data_state = data_year[data_year["State"] == option_timeseries].reset_index()
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
