import streamlit as st

st.set_page_config(page_title="Smart Energy Scheduler", layout="wide")

# -------- SESSION STATE --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------- SIDEBAR NAVIGATION --------
st.sidebar.title("Smart Energy Scheduler")

if st.session_state.logged_in:
    page = st.sidebar.radio(
        "Navigate",
        ["Home", "Devices", "Analytics", "Logout"]
    )
else:
    page = "Login"

# -------- PAGE ROUTING --------
if page == "Login":
    import login
    login.show()

elif page == "Home":
    import home
    home.show()

elif page == "Devices":
    import devices
    devices.show()

elif page == "Analytics":
    import analytics
    analytics.show()

elif page == "Logout":
    st.session_state.logged_in = False
    st.success("Logged out successfully")
    st.rerun()
