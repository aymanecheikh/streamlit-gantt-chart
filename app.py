import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

data = pd.read_excel("Technical Ticket Analysis.xlsx")

# Convert date columns to datetime format
data['Start Date'] = pd.to_datetime(data['Start Date'], errors='coerce')
data['End Date'] = pd.to_datetime(data['End Date'], errors='coerce')
data['End Date'] = data['End Date'] + pd.Timedelta(days=1)

# Drop rows with invalid dates (NaT)
data = data.dropna(subset=['Start Date', 'End Date'])

# Streamlit App
st.title("Interactive Gantt Chart")

# Filter by Tag
tags = ["All"] + list(data["Tag"].unique())
selected_tag = st.selectbox("Filter by Tag:", tags)

# Filter data based on selected tag
filtered_data = data if selected_tag == "All" else data[data["Tag"] == selected_tag]

# Create the Gantt chart
if not filtered_data.empty:
    fig = px.timeline(
        filtered_data,
        x_start="Start Date",
        x_end="End Date",
        y="Name",
        color="Tag",
        title=f"Gantt Chart - {selected_tag if selected_tag != 'All' else 'All Tags'}",
    )
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="Date")

    window_width = st.columns((1,))[0]._parent._parent._get_delta_path
    if window_width and window_width < 768:
        fig.update_layout(
            autosize=True,
            height=400,
            margin=dict(l=5, r=5, t=20, b=5),
            font=dict(size=10),
        )
    elif window_width and window_width < 1200:
        fig.update_layout(
            autosize=True,
            height=500,
            margin=dict(l=10, r=10, t=30, b=10),
            font=dict(size=12),
        )
    else:
        fig.update_layout(
            autosize=True,
            height=600,
            margin=dict(l=15, r=15, t=40, b=15),
            font=dict(size=14),
        )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No tasks available for the selected tag.")