import streamlit as st
import pandas as pd

st.title("Energy Analytics")

data = pd.DataFrame({
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Energy Usage (kWh)": [5, 4, 6, 3, 4]
})

st.bar_chart(data.set_index("Day"))
