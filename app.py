import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

# Example data
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
    fig.update_layout(width=500)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No tasks available for the selected tag.")