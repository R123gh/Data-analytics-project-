import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="🏏 IPL Cricket Insights", layout="wide")
st.title("🏏 IPL 2025 Match Analysis Dashboard")

# Load dataset
df = pd.read_csv("Cricket_data_set.csv")  # Ensure this file is in the same folder
df['date'] = pd.to_datetime(df['date'])

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
teams = sorted(set(df['team1']).union(df['team2']))
selected_teams = st.sidebar.multiselect("Select Teams", teams, default=teams)

# Filter dataset
filtered_df = df[(df['team1'].isin(selected_teams)) | (df['team2'].isin(selected_teams))]

# Dataset Preview
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head(10))

# 1. Venues hosting most matches
st.subheader("🏟️ Top 3 Venues Hosting the Most Matches")
venues = df['venue'].value_counts().reset_index().head(3)
venues.columns = ['Venue', 'Count']
fig1 = px.bar(venues, x='Venue', y='Count', color='Venue',
              title="Top 3 Venues by Match Count", text='Count')
fig1.update_traces(textposition='outside')
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# 2. Toss wins and decisions
st.subheader("🧢 Toss Decisions by Teams")
toss_df = df.groupby(['toss_winner', 'toss_decision']).size().reset_index(name='Count')
fig2 = px.bar(toss_df, x='toss_winner', y='Count', color='toss_decision',
              title="Toss Decisions by Teams", barmode='group')
fig2.update_layout(xaxis_title='Teams', yaxis_title='Toss Count')
st.plotly_chart(fig2, use_container_width=True)

# 3. Match win percentage by team
st.subheader("🏆 Match Win Percentage by Team")
all_teams = pd.concat([df['team1'], df['team2']])
total_matches = all_teams.value_counts()
match_wins = df['toss_winner'].value_counts()
win_df = pd.DataFrame({
    'Team': total_matches.index,
    'Matches Played': total_matches.values,
    'Matches Won': match_wins.reindex(total_matches.index).fillna(0).values
})
win_df['Win %'] = (win_df['Matches Won'] / win_df['Matches Played']) * 100
win_df = win_df.sort_values(by='Win %', ascending=False)

fig3 = px.bar(win_df, x='Team', y='Win %', color='Team',
              title="Match Win Percentage by Team", text='Win %')
fig3.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig3.update_layout(showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

# 4. Average first vs second innings scores
st.subheader("📊 First vs Second Innings Scores")
if 'first_innings_score' in df.columns and 'second_innings_score' in df.columns:
    innings_df = pd.DataFrame({
        'First Innings': df['first_innings_score'],
        'Second Innings': df['second_innings_score']
    }).melt(var_name='Innings', value_name='Score')

    fig4 = px.box(innings_df, x='Innings', y='Score', color='Innings',
                  title="Boxplot: First vs Second Innings Score")
    st.plotly_chart(fig4, use_container_width=True)

    avg_first = df['first_innings_score'].mean()
    avg_second = df['second_innings_score'].mean()
    st.markdown(f"📌 **Average First Innings Score:** `{avg_first:.2f}` | **Average Second Innings Score:** `{avg_second:.2f}`")
else:
    st.warning("❌ Required columns 'first_innings_score' and 'second_innings_score' not found.")

# 5. Top Performers
st.subheader("🎖️ Top Performers")

col1, col2 = st.columns(2)

with col1:
    pom = df['player_of_the_match'].value_counts().head(10).reset_index()
    pom.columns = ['Player', 'Count']
    fig5 = px.bar(pom, x='Count', y='Player', orientation='h',
                  title="Top 10 Players of the Match", color='Count', color_continuous_scale='sunset')
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    if 'top_scorer' in df.columns:
        top_scorers = df['top_scorer'].value_counts().head(10).reset_index()
        top_scorers.columns = ['Player', 'Count']
        fig6 = px.bar(top_scorers, x='Count', y='Player', orientation='h',
                      title="Top 10 Top Scorers", color='Count', color_continuous_scale='Blues')
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.warning("❌ Column 'top_scorer' not found in dataset.")
        
# 6. Trend in Wide Ball Runs Over Time
st.subheader("📈 Wide Ball Runs Over Time")
if 'wide ball runs' in df.columns and 'date' in df.columns:
    wide_df = df.groupby(df['date'].dt.date)['wide ball runs'].sum().reset_index()
    wide_df.columns = ['Date', 'Wide Runs']
    fig_wide = px.line(wide_df, x='Date', y='Wide Runs', title="Daily Wide Ball Runs Trend", markers=True)
    st.plotly_chart(fig_wide, use_container_width=True)
else:
    st.warning("Columns 'wide ball runs' or 'date' not found.")

# 7. Impact of Balls Left on Match Results
st.subheader("⏳ Balls Left vs Match Result")
if 'balls_left' in df.columns and 'match_result' in df.columns:
    balls_outcome = df.groupby('match_result')['balls_left'].mean().reset_index()
    balls_outcome.columns = ['Match Result', 'Avg Balls Left']
    fig_balls = px.bar(balls_outcome, x='Match Result', y='Avg Balls Left', color='Match Result',
                       title="Average Balls Left by Match Result", text='Avg Balls Left')
    fig_balls.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    st.plotly_chart(fig_balls, use_container_width=True)
else:
    st.warning("Columns 'balls_left' or 'match_result' not found.")

# 8. Bowlers with Best Bowling Figures Most Often
st.subheader("🎯 Bowlers with Best Bowling Figures")
if 'best_bowling' in df.columns:
    best_bowlers = df['best_bowling'].value_counts().head(10).reset_index()
    best_bowlers.columns = ['Figures', 'Count']
    fig_bowlers = px.bar(best_bowlers, x='Figures', y='Count', color='Count',
                         title="Top 10 Best Bowling Figures", text='Count')
    fig_bowlers.update_traces(textposition='outside')
    st.plotly_chart(fig_bowlers, use_container_width=True)
else:
    st.warning("Column 'best_bowling' not found.")

# 9. Relationship Between Wickets Taken and Runs Conceded
st.subheader("📉 Wickets Taken vs Runs Conceded")
if 'best_bowling_wickets1' in df.columns and 'best_bowling_runs' in df.columns:
    fig_relation = px.scatter(df, x='best_bowling_wickets1', y='best_bowling_runs', trendline='ols',
                              title="Wickets vs Runs Conceded", color='best_bowling_wickets1',
                              labels={'best_bowling_wickets1': 'Wickets', 'best_bowling_runs': 'Runs Conceded'})
    st.plotly_chart(fig_relation, use_container_width=True)
else:
    st.warning("Columns 'best_bowling_wickets1' or 'best_bowling_runs' not found.")



# Section 10: Toss Winner vs Match Winner
st.subheader("🧢📊 Toss Winner vs Match Winner")

# Check if required columns are present
required_columns = {'toss_winner', 'match_winner'}
if required_columns.issubset(df.columns):
    # Create a new column to check if toss winner also won the match
    df['toss_win_match_win'] = (df['toss_winner'] == df['match_winner']).astype(int)

    # Count outcomes
    toss_outcome = df['toss_win_match_win'].value_counts().reset_index()
    toss_outcome.columns = ['Won After Toss?', 'Count']
    toss_outcome['Won After Toss?'] = toss_outcome['Won After Toss?'].map({1: 'Yes', 0: 'No'})

    # Plot pie chart
    fig_toss = px.pie(
        toss_outcome,
        names='Won After Toss?',
        values='Count',
        title="How Often Do Teams Win After Winning the Toss?",
        hole=0.4
    )
    st.plotly_chart(fig_toss, use_container_width=True)

else:
    st.warning("Required columns 'toss_winner' and/or 'match_winner' not found in the dataset.")



# Footer
st.markdown("---")
st.markdown("📊 Built by **Raghav Sharma** using `Streamlit`, `Pandas`, and `Plotly` 🎯")
