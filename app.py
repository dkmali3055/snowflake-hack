import streamlit as st
import pandas as pd
from query_data import fetch_festival_data, fetch_tourism_data
from forecast import forecast_tourism

st.title("Cultural Calendar & Tourism Forecast")

state = st.selectbox("Select State", ["Rajasthan", "Maharashtra", "Kerala", "Tamil Nadu", "West Bengal"])

st.header(f"Festivals in {state}")
festivals = fetch_festival_data(state)


st.dataframe(festivals[['EVENT_NAME', 'START_DATE', 'END_DATE', 'ATTENDEES', 'EVENT_TYPE']])

st.header(f"Tourism Forecast for {state}")
forecast_df = forecast_tourism(state)
st.line_chart(forecast_df.set_index('ds')['yhat'])

st.write("Showing forecast for domestic visitors for next 12 months")
