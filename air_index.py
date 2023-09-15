import streamlit as st
import pandas as pd
import numpy as np

DATE_COLUMN = 'date/time'
DATA_DAILY = 'data/aqi_daily_1980_to_2021.csv'
DATA_YEARLY = 'data/aqi_yearly_1980_to_2021.csv'

@st.cache_data
def load_data():
    data_year = pd.read_csv(DATA_YEARLY)
    data_day = pd.read_csv(DATA_DAILY)
    return data_year, data_day

st.title('Air Quality Index (1980-2021)')


data_load_state = st.text('Loading data...')
data_year, data_day = load_data()
data_load_state.text("Done! (using st.cache_data)")

option = st.selectbox('Show raw data', ('None', 'Daily', 'Yearly'))
if option == 'Daily':
    st.dataframe(data_day.iloc[:10000,:])
if option == 'Yearly':
    st.dataframe(data_year)
