import streamlit as st 
import pandas as pd 
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title='Ecommerence Data Insights', layout='wide')
st.title("🛒 Ecommerence Data Insights Dashboard")

df = pd.read_csv("Ecommerence cleaned data.csv") 

st.subheader("📊 Data Set Preview")
st.dataframe(df.head())

st.subheader("1️⃣ Which Platform is Used the Most?")
platform = df['Platform'].value_counts().reset_index()
platform.columns = ['Platform', 'Count']
fig1 = px.bar(platform, x='Platform', y='Count', title='Most Used Platforms',
              color='Count', color_continuous_scale='Plasma', template='plotly_dark')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("2️⃣ Product Category Distribution")
product = df['Product Category'].value_counts().reset_index()
product.columns = ['Product Category', 'Count']
fig2 = px.pie(product, names='Product Category', values='Count', title='Product Category Share')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3️⃣ Service Rating Distribution")
service = df['Service Rating'].value_counts().reset_index()
service.columns = ['Service Rating', 'Count']
fig3 = px.bar(service, x='Service Rating', y='Count', title='Rating Distribution (1 to 5)',
              color='Count', color_continuous_scale='Viridis', template='plotly_white')
st.plotly_chart(fig3, use_container_width=True)

st.subheader("4️⃣ Delivery Delay Insights")
delay = df['Delivery Delay'].value_counts().reset_index()
delay.columns = ['Delivery Delay', 'Count']
fig4 = px.bar(delay, x='Delivery Delay', y='Count', title='Delivery Delay Distribution',
              color='Count', color_continuous_scale='Cividis', template='ggplot2')
st.plotly_chart(fig4, use_container_width=True)

st.subheader("5️⃣ Refund Requested Distribution")
refund = df['Refund Requested'].value_counts().reset_index()
refund.columns = ['Refund Requested', 'Count']
fig5 = px.pie(refund, names='Refund Requested', values='Count', title='Refund Requested Pie')
st.plotly_chart(fig5, use_container_width=True)

st.subheader("6️⃣ Order Value by Product Category")
fig6 = px.box(df, x='Product Category', y='Order Value (INR)', color='Product Category',
              title='Order Value Distribution by Product Category', template='seaborn')
st.plotly_chart(fig6, use_container_width=True)

st.subheader("7️⃣ Correlation Heatmap of Numeric Columns")
numeric_cols = df[['Delivery Time (Minutes)', 'Order Value (INR)', 'Service Rating', 'Platform_numeric']]
corr = numeric_cols.corr()
fig7 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', title='Correlation Heatmap')
st.plotly_chart(fig7, use_container_width=True)
