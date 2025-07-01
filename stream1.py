import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
st.set_page_config(page_title="🏏 IPL Cricket Insights", layout="wide")
st.title("🏏 IPL 2025 Match Analysis Dashboard")

# Load static dataset directly
df = pd.read_csv("Cricket_data_set.csv")  # 👈 make sure this file is in same folder
df['date'] = pd.to_datetime(df['date'])   # Convert to datetime

# Overview
st.subheader("🔍 Dataset Preview")
st.dataframe(df.head())

# Match Result Distribution
st.subheader("🏆 Match Results Distribution")
st.bar_chart(df['match_result'].value_counts())

# Toss Decision Chart
st.subheader("🎯 Toss Decisions")
st.bar_chart(df['toss_decision'].value_counts())

# Toss Win vs Match Win
st.subheader("🤝 Toss Win = Match Win")
fig1, ax1 = plt.subplots()
sns.countplot(x='toss_win_match_win', data=df, palette='Set2', ax=ax1)
ax1.set_title("Toss Win Match Win Relationship")
st.pyplot(fig1)

# Top Scorers
st.subheader("🔥 Top 10 Scorers")
top_scorers = df['top_scorer'].value_counts().head(10)
st.bar_chart(top_scorers)

# Balls Left Distribution
st.subheader("🕒 Balls Left Distribution")
fig2, ax2 = plt.subplots()
df['balls_left'].dropna().astype(int).hist(bins=20, color='orange', edgecolor='black', ax=ax2)
ax2.set_title("Distribution of Balls Left in Matches")
st.pyplot(fig2)

# First vs Second Innings Score Comparison
st.subheader("📊 First vs Second Innings Score")
fig3, ax3 = plt.subplots()
sns.scatterplot(data=df, x='first_innings_score', y='second_innings_score', hue='match_result', ax=ax3)
st.pyplot(fig3)

# Wide Ball Runs Over Time
st.subheader("📅 Wide Ball Runs Trend")
wide_trend = df.groupby(df['date'].dt.date)['wide ball runs'].sum()
st.line_chart(wide_trend)

# Footer
st.markdown("---")
st.markdown("📊 Built by Raghav Sharma using Streamlit, pandas, matplotlib, seaborn.")
