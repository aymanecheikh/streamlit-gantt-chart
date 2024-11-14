import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

device_detection_html = """
<script>
    const isMobile = /Mobi|Android/i.test(navigator.userAgent);
    const deviceType = isMobile ? "Mobile" : "Desktop";
    document.body.setAttribute("data-device-type", deviceType);
    const streamlitEvent = new Event("streamlit:device-type-detected");
    streamlitEvent.deviceType = deviceType;
    window.parent.dispatchEvent(streamlitEvent);
</script>
"""

html(device_detection_html)

# Detect device type
if "device_type" not in st.session_state:
    # Use the body's data attribute to detect the device type
    st.session_state["device_type"] = "Desktop"

device_type = st.session_state["device_type"]
js_code = """
<script>
    window.addEventListener("streamlit:device-type-detected", function(event) {
        fetch(window.location.href + "&device_type=" + event.deviceType)
            .then(response => console.log("Device type sent to Streamlit:", event.deviceType));
    });
</script>
"""
html(js_code)

query_params = st.experimental_get_query_params()
if "device_type" in query_params:
    st.session_state["device_type"] = query_params["device_type"][0]

device_type = st.session_state["device_type"]
st.write(f"Detected Device: {device_type}")

data = pd.read_excel("Technical Ticket Analysis.xlsx")

# Convert date columns to datetime format
data['Start Date'] = pd.to_datetime(data['Start Date'], errors='coerce')
data['End Date'] = pd.to_datetime(data['End Date'], errors='coerce')
data['End Date'] = data['End Date'] + pd.Timedelta(days=1)

# Drop rows with invalid dates (NaT)
data = data.dropna(subset=['Start Date', 'End Date'])

# Streamlit App
st.title("Interactive Gantt Chart")

# Display detected device type
device_type = st.session_state['device_type']
st.write(f"Detected Device: {device_type}")

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

    if device_type == 'Mobile':
        fig.update_layout(
            autosize=True,
            height=400,
            margin=dict(l=5, r=5, t=20, b=5),
            font=dict(size=10),
        )
    else:
        fig.update_layout(
            autosize=True,
            height=600,
            margin=dict(l=10, r=10, t=30, b=10),
            font=dict(size=12),
        )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No tasks available for the selected tag.")