import streamlit as st

st.title("Home Dashboard")

st.metric("Connected Devices", "4")
st.metric("Current Power Usage", "1402 W")
st.metric("Energy Saved Today", "25%")

st.info("Suggestion: Enable Eco Mode to save more energy")
