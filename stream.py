import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📈 Auto Chart Generator from CSV")


uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(numeric_cols) >= 2:
        st.subheader("📊 Correlation Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

  
    date_cols = df.select_dtypes(include=['datetime64', 'object']).columns
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col])
            df = df.sort_values(by=col)
            st.subheader(f"📈 Line Chart: {numeric_cols[0]} over {col}")
            st.line_chart(df.set_index(col)[numeric_cols[0]])
            break
        except:
            continue

   
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    for col in cat_cols:
        if df[col].nunique() < 20:
            st.subheader(f"📊 Bar Chart: Avg {numeric_cols[0]} by {col}")
            bar_data = df.groupby(col)[numeric_cols[0]].mean().sort_values()
            st.bar_chart(bar_data)
            break
