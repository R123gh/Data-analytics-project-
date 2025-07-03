import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title='Flight Data Insights', layout='wide')
st.title("✈️ Flight Data Insights Dashboard")

# Load dataset
df = pd.read_csv("Flight_Price_Dataset_of_Bangladesh_Cleaned.csv")

# Convert datetime columns
df['Departure Date & Time'] = pd.to_datetime(df['Departure Date & Time'])
df['Arrival Date & Time'] = pd.to_datetime(df['Arrival Date & Time'])

# Dataset Preview
st.subheader("📄 Dataset Preview")
st.dataframe(df.head(10))

# Booking Source
st.subheader("🧾 Most Booked Sources")
booking_source = df['Booking Source'].value_counts().reset_index()
booking_source.columns = ['Source', 'Count']
fig1 = px.bar(booking_source, x='Source', y='Count', title='Booking Sources', color='Count')
st.plotly_chart(fig1, use_container_width=True)

# Class Usage
st.subheader("💺 Most Frequently Used Travel Class")
class_count = df['Class'].value_counts().reset_index()
class_count.columns = ['Class', 'Count']
fig2 = px.bar(class_count, x='Class', y='Count', title='Class Usage by Passengers', color='Count')
st.plotly_chart(fig2, use_container_width=True)

# Airline Usage
st.subheader("🛫 Flights per Airline")
airline_count = df['Airline'].value_counts().reset_index()
airline_count.columns = ['Airline', 'Count']
fig3 = px.bar(airline_count, x='Airline', y='Count', title='Flights by Airline', color='Count')
st.plotly_chart(fig3, use_container_width=True)

# Monthly Flights
st.subheader("📅 Flights by Month")
df['Month'] = df['Departure Date & Time'].dt.month_name()
monthly_flights = df['Month'].value_counts().reindex([
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
])
monthly_df = pd.DataFrame({
    'Month': monthly_flights.index,
    'Flights': monthly_flights.values
})
fig4 = px.line(monthly_df, x='Month', y='Flights', markers=True, title='Number of Flights per Month')
st.plotly_chart(fig4, use_container_width=True)

# Heatmap: Arrival Hour vs Day
st.subheader("⏱️ Flight Arrival Heatmap (Hour vs Day)")
df['Arrival_Hour'] = df['Arrival Date & Time'].dt.hour
df['Arrival_Day'] = df['Arrival Date & Time'].dt.day_name()
heatmap_data = df.groupby(['Arrival_Day', 'Arrival_Hour']).size().reset_index(name='Flight_Count')
fig5 = px.density_heatmap(
    heatmap_data,
    x='Arrival_Hour',
    y='Arrival_Day',
    z='Flight_Count',
    color_continuous_scale='YlGnBu',
    title='Flight Arrivals by Hour and Day'
)
st.plotly_chart(fig5, use_container_width=True)

# Top 10 Busiest Routes
st.subheader("🔁 Top 10 Busiest Routes")
df['Most_routes'] = df['Source Name'] + ' -> ' + df['Destination Name']
routes = df['Most_routes'].value_counts().head(10).reset_index()
routes.columns = ['Route', 'Count']
fig6 = px.bar(routes, x='Count', y='Route', orientation='h', title='Top 10 Most Frequent Routes', color='Count')
st.plotly_chart(fig6, use_container_width=True)

# Busiest Airports (Arrivals + Departures)
st.subheader("🛬 Top 10 Busiest Airports (Arrivals + Departures)")
all_airports = pd.concat([
    df['Source Name'].rename('Airport'),
    df['Destination Name'].rename('Airport')
])
airport_traffic = all_airports.value_counts().head(10).reset_index()
airport_traffic.columns = ['Airport', 'Total Flights']
fig7 = px.bar(airport_traffic, x='Total Flights', y='Airport', orientation='h',
              title='Top 10 Busiest Airports', color='Total Flights')
st.plotly_chart(fig7, use_container_width=True)
