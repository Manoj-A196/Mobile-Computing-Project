import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Energy Scheduler Demo",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Login"

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- STYLES ----------------
st.markdown("""
<style>
body { background-color: #0f172a; }
[data-testid="stSidebar"] { background-color: #020617; }
.card {
    background-color: #020617;
    padding: 20px;
    border-radius: 15px;
    color: white;
}
.title { color: #e5e7eb; font-size: 28px; font-weight: 600; }
.subtitle { color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

# ---------------- APPLIANCE DATABASE ----------------
APPLIANCES = {
    "Air Conditioner": {"power": 1800, "hours": 6, "eco_save": 30},
    "Refrigerator": {"power": 150, "hours": 24, "eco_save": 15},
    "Washing Machine": {"power": 500, "hours": 1, "eco_save": 20},
    "Ceiling Fan": {"power": 70, "hours": 10, "eco_save": 25},
    "LED Light": {"power": 40, "hours": 8, "eco_save": 40},
    "Water Heater (Geyser)": {"power": 2000, "hours": 1, "eco_save": 35},
    "EV Charger": {"power": 2200, "hours": 4, "eco_save": 25},
    "Microwave Oven": {"power": 1200, "hours": 0.5, "eco_save": 15}
}

ELECTRICITY_RATE = 6   # ₹ per kWh
CO2_FACTOR = 0.82     # kg CO₂ per kWh

# ---------------- REGISTER ----------------
def register_page():
    st.title("📝 Register")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        if u and p:
            if u in st.session_state.users:
                st.error("User already exists")
            else:
                st.session_state.users[u] = p
                st.success("Registration successful")
                st.session_state.page = "Login"
                st.rerun()
        else:
            st.error("All fields required")

    st.button("Go to Login", on_click=lambda: set_page("Login"))

# ---------------- LOGIN ----------------
def login_page():
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

    st.button("Register New User", on_click=lambda: set_page("Register"))

# ---------------- DASHBOARD ----------------
def dashboard():
    st.sidebar.title("⚡ Smart Energy")
    st.sidebar.caption(f"User: {st.session_state.username}")

    menu = st.sidebar.radio(
        "Navigation",
        ["Appliance Control", "Logout"]
    )

    if menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.rerun()
    else:
        appliance_dashboard()

# ---------------- APPLIANCE CONTROL DASHBOARD ----------------
def appliance_dashboard():
    st.markdown('<div class="title">Appliance Control & Energy Stats</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Control appliances and monitor energy usage</div>', unsafe_allow_html=True)

    appliance = st.selectbox("Select Appliance", list(APPLIANCES.keys()))

    # ON / OFF TOGGLE
    power_state = st.toggle(f"{appliance} Power", value=True)

    data = APPLIANCES[appliance]

    if power_state:
        power = data["power"]
        hours = data["hours"]
        daily_kwh = (power * hours) / 1000
        monthly_kwh = daily_kwh * 30
        monthly_cost = monthly_kwh * ELECTRICITY_RATE
        eco_kwh = monthly_kwh * (1 - data["eco_save"] / 100)
        co2 = monthly_kwh * CO2_FACTOR
    else:
        daily_kwh = monthly_kwh = monthly_cost = eco_kwh = co2 = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Power Status", "ON ✅" if power_state else "OFF ❌")
        st.metric("Daily Usage", f"{daily_kwh:.2f} kWh")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Monthly Consumption", f"{monthly_kwh:.1f} kWh")
        st.metric("Monthly Cost", f"₹ {monthly_cost:.0f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Eco Saving", f"{data['eco_save']} %")
        st.metric("CO₂ Emission", f"{co2:.1f} kg")
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- USAGE TREND --------
    st.subheader("📈 Weekly Energy Usage Trend")

    if power_state:
        usage = np.random.randint(
            int(daily_kwh * 0.8),
            int(daily_kwh * 1.2),
            size=7
        )
    else:
        usage = [0] * 7

    df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Energy (kWh)": usage
    })

    fig = px.line(df, x="Day", y="Energy (kWh)", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    if power_state:
        st.success(f"Eco mode can save approx {monthly_kwh - eco_kwh:.1f} kWh per month")
    else:
        st.warning("Appliance is OFF. No energy consumption.")

# ---------------- HELPER ----------------
def set_page(p):
    st.session_state.page = p

# ---------------- ROUTING ----------------
if not st.session_state.logged_in:
    if st.session_state.page == "Register":
        register_page()
    else:
        login_page()
else:
    dashboard()
