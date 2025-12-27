import streamlit as st

def show():
    st.title("⚙️ Device Control")

    device = st.selectbox(
        "Select Device",
        ["Air Conditioner", "Fan", "Light", "Washing Machine"]
    )

    power = st.toggle("Power ON / OFF")

    mode = st.selectbox(
        "Operating Mode",
        ["Normal", "Eco", "Turbo"]
    )

    if device == "Air Conditioner":
        temp = st.slider("Temperature (°C)", 16, 30)

    st.success(f"{device} settings updated (Demo)")
