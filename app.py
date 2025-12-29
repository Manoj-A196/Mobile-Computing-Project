import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Energy Scheduler Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DARK THEME STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
[data-testid="stSidebar"] {
    background-color: #020617;
}
.card {
    background-color: #020617;
    padding: 20px;
    border-radius: 15px;
    color: white;
}
.title {
    color: #e5e7eb;
    font-size: 26px;
    font-weight: 600;
}
.subtitle {
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚡ Fusion Smart")
st.sidebar.caption("Energy Dashboard")

menu = st.sidebar.radio(
    "",
    ["Dashboard", "Appliances", "Analytics"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.markdown('<div class="title">Energy Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Monthly overview</div>', unsafe_allow_html=True)
    st.markdown("")

    col1, col2, col3 = st.columns(3)

    # COST PREDICTED
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            values=[214, 86],
            hole=0.7,
            marker_colors=["#22c55e", "#334155"],
            textinfo="none"
        ))
        fig.update_layout(
            height=220,
            margin=dict(t=0,b=0,l=0,r=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Total Cost**  \n$214")
        st.markdown('</div>', unsafe_allow_html=True)

    # CHANGE IN COST
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Change in Cost**")
        st.metric("Increase", "5.42%", "+$11")
        bar_df = pd.DataFrame({
            "Month": ["May", "June"],
            "Cost": [203, 214]
        })
        fig = px.bar(bar_df, x="Month", y="Cost", color="Month")
        fig.update_layout(height=200, margin=dict(t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # USAGE ESTIMATE
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Usage Estimate**")
        usage = pd.DataFrame({
            "Day": list(range(1, 8)),
            "kWh": [120, 150, 180, 220, 260, 300, 350]
        })
        fig = px.line(usage, x="Day", y="kWh", markers=True)
        fig.update_layout(height=220)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- APPLIANCES ----------------
elif menu == "Appliances":
    st.markdown('<div class="title">Active Appliances</div>', unsafe_allow_html=True)
    st.markdown("")

    appliances = {
        "Heating & AC": 1.4,
        "EV Charge": 0.9,
        "Plug Loads": 0.8,
        "Refrigeration": 0.7,
        "Lighting": 0.4
    }

    df = pd.DataFrame({
        "Appliance": appliances.keys(),
        "Usage (kWh)": appliances.values()
    })

    fig = px.bar(
        df,
        x="Usage (kWh)",
        y="Appliance",
        orientation="h",
        color="Appliance"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    st.markdown('<div class="title">Carbon Footprint</div>', unsafe_allow_html=True)
    st.markdown("")

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
