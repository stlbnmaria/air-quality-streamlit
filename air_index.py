import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

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

st.title(f"Air Quality Index in {option_state}")

# KPIs
st.subheader(f"KPIs for {option_time}")
col0, col1, col2, col3 = st.columns(4)
col0.metric(
    "\# Measuring Stations",
    date_time["County"].nunique(),
    date_time["County"].nunique() - date_prev["County"].nunique(),
)
med_aqi = int(round(date_time["Median AQI"].mean(), 0))
col1.metric(
    "Median AQI",
    med_aqi,
    med_aqi - int(round(date_prev["Median AQI"].mean(), 0)),
)
good_days = int(round(date_time["Good Days"].mean(), 0))
col2.metric(
    "\# Good Days",
    good_days,
    good_days - int(round(date_prev["Good Days"].mean(), 0)),
)
unhealth_days = int(
    round(date_time["Unhealthy Days"].mean(), 0)
    + round(date_time["Very Unhealthy Days"].mean(), 0)
    + round(date_time["Hazardous Days"].mean(), 0)
)
unhealth_days_prev = int(
    round(date_prev["Unhealthy Days"].mean(), 0)
    + round(date_prev["Very Unhealthy Days"].mean(), 0)
    + round(date_prev["Hazardous Days"].mean(), 0)
)
col3.metric(
    "\# Unhealthy+ Days",
    unhealth_days,
    unhealth_days - unhealth_days_prev,
)

col01, col11 = st.columns(2)
# map of measuring locations for the air quality index
# TODO: fix map refresh issue - streamlit bug, look into pydeck
col01.subheader(f"Locations of Measuring Stations in {option_time}")
col01.map(date_time)

col11.subheader(f"Distribution of Rating of Days in {option_time}")
data_bar = round(date_time.loc[:, "Good Days":"Hazardous Days"].mean(), 0).astype(int)
data_bar.rename(
    index={
        "Good Days": "Good",
        "Moderate Days": "Moderate",
        "Unhealthy for Sensitive Groups Days": "Unhealthy for Sensitive Groups",
        "Unhealthy Days": "Unhealthy",
        "Very Unhealthy Days": "Very Unhealthy",
        "Hazardous Days": "Hazardous",
    },
    inplace=True,
)
data_bar = data_bar.reset_index()
data_bar.columns = ["Rating", "Number of Days"]
data_bar["Rating"] = pd.Categorical(
    data_bar.Rating,
    ordered=True,
    categories=[
        "Good",
        "Moderate",
        "Unhealthy for Sensitive Groups",
        "Unhealthy",
        "Very Unhealthy",
        "Hazardous",
    ],
)
data_bar = data_bar.sort_values("Rating")
fig = px.pie(
    data_bar,
    values="Number of Days",
    names="Rating",
    hole=0.3,
    color_discrete_sequence=px.colors.diverging.Fall,
)
fig.update_traces(textposition="inside")
fig.update_layout(uniformtext_minsize=10, uniformtext_mode="hide")
fig.update_layout(
    legend=dict(
        orientation="h",
        x=0.1,
        xanchor="left",
    )
)
col11.plotly_chart(fig, use_container_width=True)

# development of the daily air quality per state
# TODO: change ticks in x-axis
st.subheader(
    f"Median AQI per County ({min(data_year['Year'])} - {max(data_year['Year'])})"
)
st.line_chart(data_state, x="Year", y="Median AQI", color="County")

# option to show and inspect raw data (for the daily only the first 10k rows are displayed)
st.subheader(
    f"Raw Data for all States ({min(data_year['Year'])} - {max(data_year['Year'])})"
)
option = st.selectbox("Select periodicity of the data:", ("None", "Daily", "Yearly"))
if option == "Daily":
    st.write(
        "This prompt is limited to 50k rows to ensure the speed of the application."
    )
    st.dataframe(data_day.iloc[:50000, :])
if option == "Yearly":
    st.dataframe(data_year)
