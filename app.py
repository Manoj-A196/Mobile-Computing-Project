import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Energy Scheduler Demo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state.users = {}  # store registered users

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Login"

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

# ---------------- REGISTER PAGE ----------------
def register_page():
    st.title("📝 Register")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if username and password:
            if username in st.session_state.users:
                st.error("User already exists")
            else:
                st.session_state.users[username] = password
                st.success("Registration successful! Please login.")
                st.session_state.page = "Login"
                st.rerun()
        else:
            st.error("All fields required")

    st.button("Go to Login", on_click=lambda: set_page("Login"))

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "Dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.button("Register New User", on_click=lambda: set_page("Register"))

# ---------------- DASHBOARD ----------------
def dashboard():
    st.sidebar.title("⚡ Fusion Smart")
    st.sidebar.caption(f"User: {st.session_state.username}")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Appliances", "Analytics", "Logout"]
    )

    if menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.rerun()

    elif menu == "Dashboard":
        energy_dashboard()

    elif menu == "Appliances":
        appliance_dashboard()

    elif menu == "Analytics":
        analytics_dashboard()

# ---------------- ENERGY DASHBOARD ----------------
def energy_dashboard():
    st.markdown('<div class="title">Energy Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Overview</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            values=[214, 86],
            hole=0.7,
            marker_colors=["#22c55e", "#334155"],
            textinfo="none"
        ))
        fig.update_layout(height=230, margin=dict(t=0,b=0,l=0,r=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Total Cost**  \n$214")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Cost Increase", "5.42%", "+$11")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        usage = pd.DataFrame({
            "Day": list(range(1, 8)),
            "kWh": [120, 150, 180, 220, 260, 300, 350]
        })
        fig = px.line(usage, x="Day", y="kWh", markers=True)
        fig.update_layout(height=230)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- APPLIANCE SELECTION ----------------
def appliance_dashboard():
    st.markdown('<div class="title">Appliance Statistics</div>', unsafe_allow_html=True)

    appliance = st.selectbox(
        "Choose Appliance",
        ["Air Conditioner", "Fan", "Light", "Washing Machine", "EV Charger"]
    )

    appliance_data = {
        "Air Conditioner": 1800,
        "Fan": 70,
        "Light": 40,
        "Washing Machine": 500,
        "EV Charger": 2200
    }

    power = appliance_data[appliance]
    eco_power = int(power * 0.7)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Normal Mode Power", f"{power} W")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Eco Mode Power", f"{eco_power} W")
        st.markdown('</div>', unsafe_allow_html=True)

    st.success(f"Eco mode saves {power - eco_power} W energy")

# ---------------- ANALYTICS ----------------
def analytics_dashboard():
    st.markdown('<div class="title">Carbon Footprint</div>', unsafe_allow_html=True)

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=47,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#22c55e"}
        },
        title={"text": "kWh / Sqft"}
    ))
    gauge.update_layout(height=350)
    st.plotly_chart(gauge, use_container_width=True)

    st.success("🌱 Green energy usage is within optimal range")

# ---------------- HELPER ----------------
def set_page(name):
    st.session_state.page = name

# ---------------- ROUTING ----------------
if not st.session_state.logged_in:
    if st.session_state.page == "Register":
        register_page()
    else:
        login_page()
else:
    dashboard()
