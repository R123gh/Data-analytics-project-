import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🌦️ Weather Dashboard", layout="wide")
st.title("🌦️  Weather Dashboard")

# ------------------------ City Coordinates ------------------------
city_coords = {
    "Delhi": (28.61, 77.23),
    "Mumbai": (19.07, 72.87),
    "Kolkata": (22.57, 88.36),
    "Shimla": (31.10, 77.17),
    "Ludhiana": (30.91, 75.85),
    "Manali": (32.24, 77.19),
    "Bangalore": (12.97, 77.59),
    "Hyderabad": (17.38, 78.48),
    "Chennai": (13.08, 80.27),
    "Jaipur": (26.91, 75.79),
    "Ahmedabad": (23.03, 72.58),
    "Lucknow": (26.85, 80.95),
    "Indore": (22.72, 75.87),
    "Amritsar": (31.63, 74.87),
    "Chandigarh": (30.74, 76.79),
    "Jalandhar": (31.33, 75.57)
}

# ------------------------ City Selection ------------------------
city = st.selectbox("📍 Select a City", list(city_coords.keys()))

if city:
    lat, lon = city_coords[city]

    # ------------------------ API Call ------------------------
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&hourly=temperature_2m,windspeed_10m,winddirection_10m"
        f"&timezone=auto"
    )
    res = requests.get(url)
    data = res.json()

    # ------------------------ Data Processing ------------------------
    hourly_df = pd.DataFrame({
        "Time": pd.to_datetime(data["hourly"]["time"]),
        "Temperature (°C)": data["hourly"]["temperature_2m"],
        "Wind Speed (km/h)": data["hourly"]["windspeed_10m"],
        "Wind Direction (°)": data["hourly"]["winddirection_10m"]
    })

    # ------------------------ Line Chart: Temperature ------------------------
    st.subheader(f"📈 Hourly Temperature in {city}")
    fig_temp = px.line(hourly_df, x="Time", y="Temperature (°C)", markers=True, color_discrete_sequence=['orange'])
    st.plotly_chart(fig_temp, use_container_width=True)

    # ------------------------ Area Chart: Wind Speed ------------------------
    st.subheader(f"💨 Wind Speed Trend in {city}")
    fig_wind = px.area(hourly_df, x="Time", y="Wind Speed (km/h)", title="Wind Speed Over Time", color_discrete_sequence=['skyblue'])
    st.plotly_chart(fig_wind, use_container_width=True)

    # ------------------------ Heatmap: Temperature by Hour & Day ------------------------
    st.subheader("🔥 Temperature Heatmap (Hourly)")

    temp_pivot = hourly_df.copy()
    temp_pivot["Hour"] = temp_pivot["Time"].dt.hour
    temp_pivot["Day"] = temp_pivot["Time"].dt.date
    heatmap_data = temp_pivot.pivot(index="Day", columns="Hour", values="Temperature (°C)")

    fig, ax = plt.subplots(figsize=(12, 3))
    sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".1f", linewidths=0.1, ax=ax)
    ax.set_title("Temperature Heatmap")
    st.pyplot(fig)

    # ------------------------ Bar Chart: Max/Min Temp ------------------------
    st.subheader("📊 Daily Max and Min Temperature")

    temp_summary = hourly_df.resample("D", on="Time").agg({"Temperature (°C)": ["max", "min"]}).reset_index()
    temp_summary.columns = ["Date", "Max Temp (°C)", "Min Temp (°C)"]

    fig_bar = px.bar(temp_summary, x="Date", y=["Max Temp (°C)", "Min Temp (°C)"],
                     barmode="group", title="Daily Max & Min Temperature")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ------------------------ Dual Y-Axis Line Chart ------------------------
    st.subheader("📈 Compare Temperature and Wind Speed")
    fig_dual = px.line()
    fig_dual.add_scatter(x=hourly_df["Time"], y=hourly_df["Temperature (°C)"],
                         mode='lines', name='Temperature (°C)', line=dict(color='orange'))
    fig_dual.add_scatter(x=hourly_df["Time"], y=hourly_df["Wind Speed (km/h)"],
                         mode='lines', name='Wind Speed (km/h)', line=dict(color='blue'))
    fig_dual.update_layout(title="Temperature vs Wind Speed Over Time", xaxis_title="Time")
    st.plotly_chart(fig_dual, use_container_width=True)

    # ------------------------ Polar Plot: Wind Direction ------------------------
    st.subheader("🧭 Wind Direction Polar Plot")
    fig_polar = px.line_polar(r=hourly_df["Wind Speed (km/h)"],
                              theta=hourly_df["Wind Direction (°)"],
                              title="Wind Direction & Speed", line_close=True)
    st.plotly_chart(fig_polar, use_container_width=True)
