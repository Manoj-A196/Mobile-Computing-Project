import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config("Smart Energy Scheduler", layout="wide")

# ---------------- SESSION STATE INIT ----------------
def init_state():
    defaults = {
        "users": {},
        "logged_in": False,
        "username": "",
        "page": "Login",
        "appliance_state": {}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ---------------- DATA ----------------
APPLIANCES = {
    "Air Conditioner": {"power": 1800, "hours": 6, "eco": 30},
    "Refrigerator": {"power": 150, "hours": 24, "eco": 15},
    "Ceiling Fan": {"power": 70, "hours": 10, "eco": 25},
    "LED Light": {"power": 40, "hours": 8, "eco": 40},
    "Washing Machine": {"power": 500, "hours": 1, "eco": 20},
    "Geyser": {"power": 2000, "hours": 1, "eco": 35}
}

RATE = 6
CO2 = 0.82

# ---------------- STYLES ----------------
st.markdown("""
<style>
.card{background:#020617;padding:18px;border-radius:14px;color:white}
body{background:#0f172a}
</style>
""", unsafe_allow_html=True)

# ---------------- AUTH ----------------
def login():
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in st.session_state.users and st.session_state.users[u] == p:
            st.session_state.logged_in = True
            st.session_state.username = u
            st.session_state.page = "Dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Register"):
        st.session_state.page = "Register"
        st.rerun()

def register():
    st.title("📝 Register")
    u = st.text_input("New Username")
    p = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        if u and p:
            st.session_state.users[u] = p
            st.success("Account created")
            st.session_state.page = "Login"
            st.rerun()
        else:
            st.error("Fill all fields")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("⚡ Energy Overview")

    total_kwh = 0
    for a, d in APPLIANCES.items():
        if st.session_state.appliance_state.get(a, False):
            total_kwh += (d["power"] * d["hours"]) / 1000

    col1, col2, col3 = st.columns(3)
    col1.metric("Active Appliances", sum(st.session_state.appliance_state.values()))
    col2.metric("Daily Energy", f"{total_kwh:.2f} kWh")
    col3.metric("Estimated Cost", f"₹ {total_kwh * RATE:.0f}")

# ---------------- APPLIANCE CONTROL ----------------
def appliance_control():
    st.title("🔌 Appliance Control")

    appliance = st.selectbox("Choose Appliance", APPLIANCES.keys())

    if appliance not in st.session_state.appliance_state:
        st.session_state.appliance_state[appliance] = False

    state = st.toggle("Power ON / OFF", st.session_state.appliance_state[appliance])
    st.session_state.appliance_state[appliance] = state

    d = APPLIANCES[appliance]

    if state:
        daily = (d["power"] * d["hours"]) / 1000
        monthly = daily * 30
        cost = monthly * RATE
        co2 = monthly * CO2
    else:
        daily = monthly = cost = co2 = 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Daily Usage", f"{daily:.2f} kWh")
    c2.metric("Monthly Cost", f"₹ {cost:.0f}")
    c3.metric("CO₂ Emission", f"{co2:.1f} kg")

# ---------------- SCHEDULING ----------------
def scheduling():
    st.title("⏰ Smart Scheduling")

    appliance = st.selectbox("Select Appliance", APPLIANCES.keys())
    start = st.time_input("Start Time")
    end = st.time_input("End Time")
    battery = st.slider("Battery Level (%)", 0, 100, 50)

    if battery < 20:
        st.warning("Battery low → Eco mode recommended")

    if st.button("Apply Schedule"):
        st.success(f"Schedule saved for {appliance} (Demo)")

# ---------------- REPORT ----------------
def report():
    st.title("📊 Energy Summary")

    data = []
    for a, d in APPLIANCES.items():
        if st.session_state.appliance_state.get(a, False):
            kwh = (d["power"] * d["hours"]) / 1000
            data.append([a, kwh])

    if data:
        df = pd.DataFrame(data, columns=["Appliance", "Daily kWh"])
        st.bar_chart(df.set_index("Appliance"))
    else:
        st.info("No active appliances")

# ---------------- NAVIGATION ----------------
def main_app():
    st.sidebar.title("Smart Energy")
    page = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Appliances", "Scheduling", "Report", "Logout"]
    )

    if page == "Dashboard":
        dashboard()
    elif page == "Appliances":
        appliance_control()
    elif page == "Scheduling":
        scheduling()
    elif page == "Report":
        report()
    else:
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.rerun()

# ---------------- ROUTER ----------------
if not st.session_state.logged_in:
    if st.session_state.page == "Register":
        register()
    else:
        login()
else:
    main_app()
