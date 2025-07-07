import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Job Dataset Insights", layout='wide')
st.title("📊 AI Job Dataset Insights")

# Load Dataset
df = pd.read_csv("Ai_job.csv")

# Parse dates safely
df['posting_date'] = pd.to_datetime(df['posting_date'], errors='coerce')
df['application_deadline'] = pd.to_datetime(df.get('application_deadline'), errors='coerce')

# Data Preview
st.subheader("🔍 Data Preview")
st.dataframe(df.head())

# 1️⃣ Experience Level Distribution
st.subheader("1️⃣ What is the distribution of experience levels across all jobs?")
grouped = df.groupby(['job_title', 'experience_level']).size().reset_index(name='count')
fig1 = px.bar(
    grouped,
    x='job_title',
    y='count',
    color='experience_level',
    title="Experience Level by Job Title",
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig1.update_layout(xaxis_title="Job Title", yaxis_title="Count", xaxis_tickangle=45)
st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Most Common Employment Type in AI Job Titles
st.subheader("2️⃣ Which employment type is most common in AI job postings?")
ai_job_filtered = df[df['job_title'].str.contains("AI", case=False, na=False)]
group2 = ai_job_filtered.groupby(['job_title', 'employment_type']).size().reset_index(name='count')
fig2 = px.bar(
    group2,
    x='job_title',
    y='count',
    color='employment_type',
    title="Employment Type by AI Job Title",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig2.update_layout(xaxis_title="Job Title", yaxis_title="Count", xaxis_tickangle=45)
st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Top 10 Countries or Regions for AI Jobs
st.subheader("3️⃣ What are the top 10 countries or regions for AI job postings (by company location)?")
top_countries = df['company_location'].value_counts().head(10).reset_index()
top_countries.columns = ['company_location', 'count']
fig3 = px.bar(
    top_countries,
    x='company_location',
    y='count',
    title="Top 10 Countries/Regions for AI Jobs",
    color='company_location',
    color_discrete_sequence=px.colors.sequential.Plasma
)
fig3.update_layout(showlegend=False, xaxis_title="Country", yaxis_title="Number of Jobs")
st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Company Size Posting Most Jobs
st.subheader("4️⃣ Which company size is posting the most jobs?")
posting = df['company_size'].value_counts().reset_index()
posting.columns = ['company_size', 'count']
fig4 = px.bar(
    posting,
    x='company_size',
    y='count',
    title="Jobs by Company Size",
    color='company_size',
    color_discrete_sequence=px.colors.qualitative.Vivid
)
fig4.update_layout(showlegend=False, xaxis_title="Company Size", yaxis_title="Job Postings")
st.plotly_chart(fig4, use_container_width=True)

# 5️⃣ Average Remote Ratio
st.subheader("5️⃣ What is the average remote ratio across companies?")
top_10 = df.groupby("company_name")["remote_ratio"].mean().sort_values(ascending=False).head(10).reset_index()
fig5 = px.bar(
    top_10,
    x="company_name",
    y="remote_ratio",
    title="Top 10 Companies with Highest Average Remote Ratio",
    color="remote_ratio",
    color_continuous_scale="rainbow"
)
fig5.update_layout(xaxis_title="Company Name", yaxis_title="Average Remote Ratio", xaxis_tickangle=45)
st.plotly_chart(fig5, use_container_width=True)

# 6️⃣ Most Common Employee Residences
st.subheader("6️⃣ What are the top 5 most common employee residences in AI jobs?")
top5 = ai_job_filtered['employee_residence'].value_counts().head(5)
fig6 = px.pie(
    values=top5.values,
    names=top5.index,
    title="Top 5 Most Common Employee Residences",
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig6, use_container_width=True)

# 7️⃣ Job Postings Over Time
st.subheader("7️⃣ How has the number of job postings changed over time?")
jobs_by_month = df['posting_date'].dt.to_period("M").value_counts().sort_index()
jobs_by_month.index = jobs_by_month.index.astype(str)
fig7 = px.line(
    x=jobs_by_month.index,
    y=jobs_by_month.values,
    title="Job Postings Over Time",
    markers=True
)
fig7.update_layout(xaxis_title="Month", yaxis_title="Number of Postings")
st.plotly_chart(fig7, use_container_width=True)

# 8️⃣ Time Between Post Date and Application Deadline
st.subheader("8️⃣ Average time between post date and application deadline across companies")
df['diff_days'] = (df['application_deadline'] - df['posting_date']).dt.days
group_by_company = df.groupby("company_name")["diff_days"].mean().sort_values(ascending=False).head(10).reset_index()
fig8 = px.bar(
    group_by_company,
    x="company_name",
    y="diff_days",
    title="Average Time Between Post Date and Deadline by Company",
    color="diff_days",
    color_continuous_scale="Agsunset"
)
fig8.update_layout(xaxis_title="Company", yaxis_title="Avg Days", xaxis_tickangle=45)
st.plotly_chart(fig8, use_container_width=True)

# 9️⃣ Seasonal Trends in Job Postings
st.subheader("9️⃣ Are there seasonal trends in AI job postings?")
df['posting_month'] = df['posting_date'].dt.month_name()
posting_jobs = df['posting_month'].value_counts().reset_index()
posting_jobs.columns = ['Month', 'Count']
posting_jobs = posting_jobs.sort_values(by='Count', ascending=False)
fig9 = px.line(
    posting_jobs,
    x='Month',
    y='Count',
    title='Monthly Trends in Job Postings',
    markers=True
)
fig9.update_layout(xaxis_title="Month", yaxis_title="Number of Posts")
st.plotly_chart(fig9, use_container_width=True)

# 🔟 Most Frequent Skills
st.subheader("🔟 Which skills are most frequently required in AI job postings?")
if 'required_skills' in df.columns:
    df['required_skills'] = df['required_skills'].apply(lambda x: x.split(',') if pd.notnull(x) else [])
    Top_10_skill = df.explode("required_skills")['required_skills'].value_counts().head(10).reset_index()
    Top_10_skill.columns = ['Skill', 'Count']
    fig10 = px.bar(
        Top_10_skill,
        x='Skill',
        y='Count',
        title="Top 10 Skills Required in AI Job Postings",
        color='Count',
        color_continuous_scale='Inferno'
    )
    fig10.update_layout(xaxis_title="Skill", yaxis_title="Count")
    st.plotly_chart(fig10, use_container_width=True)
else:
    st.warning("⚠️ 'required_skills' column not found in dataset.")
