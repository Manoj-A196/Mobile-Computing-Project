import streamlit as st

st.set_page_config(page_title="Smart Energy Scheduler", layout="wide")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Login", "Home", "Devices", "Analytics"]
)

if page == "Login":
    import login
elif page == "Home":
    import home
elif page == "Devices":
    import devices
elif page == "Analytics":
    import analytics
