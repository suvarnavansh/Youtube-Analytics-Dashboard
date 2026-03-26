import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

# 🎨 Premium UI Styling
st.markdown(
    """
    <style>

    /* Background */
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* Main container */
    .block-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 0 20px 20px 0;
    }

    /* Buttons */
    .stDownloadButton button {
        border-radius: 10px;
        background-color: #00c6ff;
        color: black;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("📊 YouTube Analytics Dashboard")

# Load data
df = pd.read_csv("youtube_data.csv")

# Convert date
df['published'] = pd.to_datetime(df['published'])

# Engagement Rate
df['engagement_rate'] = ((df['likes'] + df['comments']) / df['views']) * 100

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Channel filter
if 'channel' in df.columns:
    selected_channels = st.sidebar.multiselect(
        "Select Channel",
        options=df['channel'].unique(),
        default=df['channel'].unique()
    )
    df = df[df['channel'].isin(selected_channels)]

# Date filter
date_range = st.sidebar.date_input("Select Date Range", [])

if len(date_range) == 2:
    df = df[(df['published'] >= str(date_range[0])) & 
            (df['published'] <= str(date_range[1]))]

# Search filter
video_search = st.sidebar.text_input("Search Video Title")

if video_search:
    df = df[df['title'].str.contains(video_search, case=False)]

# Metrics
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Views", int(df['views'].sum()))
col2.metric("Total Likes", int(df['likes'].sum()))
col3.metric("Total Comments", int(df['comments'].sum()))
col4.metric("Avg Engagement (%)", round(df['engagement_rate'].mean(), 2))

# Channel comparison
if 'channel' in df.columns:
    st.subheader("📊 Channel Performance Comparison")

    channel_perf = df.groupby('channel')[['views', 'likes', 'comments']].sum().reset_index()

    fig0 = px.bar(channel_perf, x='channel', y='views',
                  title="Total Views by Channel", color='views')
    st.plotly_chart(fig0, use_container_width=True)

# Top videos
st.subheader("🔥 Top Performing Videos")

top_videos = df.sort_values(by='views', ascending=False).head(10)

fig1 = px.bar(top_videos, x='views', y='title', orientation='h',
              title="Top 10 Videos by Views", color='views')

st.plotly_chart(fig1, use_container_width=True)

# Engagement scatter
st.subheader("💡 Views vs Engagement")

fig2 = px.scatter(df, x='views', y='engagement_rate',
                  size='likes',
                  color='channel' if 'channel' in df.columns else None,
                  hover_name='title',
                  title="Views vs Engagement Rate")

st.plotly_chart(fig2, use_container_width=True)

# Trend
st.subheader("📈 Views Trend Over Time")

df_sorted = df.sort_values(by='published')

fig3 = px.line(df_sorted, x='published', y='views',
               color='channel' if 'channel' in df.columns else None,
               title="Views Over Time")

st.plotly_chart(fig3, use_container_width=True)

# Upload dataset
st.subheader("📂 Upload Your Own Dataset")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    new_df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded data:", new_df.head())

# Download
st.subheader("⬇️ Download Filtered Data")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='youtube_filtered_data.csv',
    mime='text/csv'
)