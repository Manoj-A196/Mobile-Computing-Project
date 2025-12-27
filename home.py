import streamlit as st

def show():
    st.title("🏠 Home Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Connected Devices", "4")
    col2.metric("Power Consumption", "1402 W")
    col3.metric("Energy Saved", "25%")

    st.info("💡 Suggestion: Enable Eco Mode to reduce energy usage")
