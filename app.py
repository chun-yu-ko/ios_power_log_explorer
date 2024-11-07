# Import necessary libraries
import sqlite3
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# Display the title in the Streamlit web app
st.title("iOS Devlice Log Explorer")

# Allow user to upload a .plsql file, restricting to the 'plsql' file type
uploaded_file = st.file_uploader("Please Upload .plsql file", type = "plsql")

# If a file is uploaded, proceed with processing
if uploaded_file is not None:

    # Save the uploaded file temporarily for SQLite connection
    with open("/tmp/uploaded_file.plsql", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Connect to the uploaded SQLite database file
    connection = sqlite3.connect("/tmp/uploaded_file.plsql")

    # Retrieve data from specific tables in the SQLite database
    battery_ui = pd.read_sql_query("SELECT * FROM PLBatteryAgent_EventBackward_BatteryUI", connection)
    app_run_time = pd.read_sql_query("SELECT * FROM PLAppTimeService_Aggregate_AppRunTime", connection)
    nodes = pd.read_sql_query("SELECT * FROM PLAccountingOperator_EventNone_Nodes", connection)
    root_node_energy = pd.read_sql_query("SELECT * FROM PLAccountingOperator_Aggregate_RootNodeEnergy", connection)
    
    # Close the SQLite connection
    connection.close()

    # Display node options for selection
    node_options = nodes["Name"].unique()
    selected_node = st.selectbox("Select a Node", node_options)

    # Process battery data
    battery_ui = battery_ui.sort_values(["timestamp"]).assign(
        datetime=lambda x: pd.to_datetime(x["timestamp"], unit="s"),
        state=lambda x: x["IsCharging"].map({0: "Not Charging", 1: "Charging"}),
        battery=lambda x: x["Level"],
        battery_start=lambda x: x["Level"][x["state"].ne(x["state"].shift())],
        battery_low=lambda x: x["battery"].apply(lambda x: x if x <= 20 else None)
    ).filter(["datetime", "state", "battery", "battery_start", "battery_low"])

    # Process app runtime data for specific intervals and app
    app_run_time = app_run_time.query("timeInterval == 3600 and BundleID == @selected_node").assign(
        datetime=lambda x: pd.to_datetime(x["timestamp"], unit="s"),
        background_duration=lambda x: x["BackgroundTime"],
        foreground_duration=lambda x: x["ScreenOnTime"]
    ).filter(["datetime", "background_duration", "foreground_duration"]).sort_values(["datetime"])

    # Filter node ID associated with the target node name
    # node_id = nodes.query("Name == 'com.getcubo.app'")["ID"].values[0]
    node_id = nodes.query("Name == @selected_node")["ID"].values[0]

    # Process energy usage data for the root node linked to the target node ID
    root_node_energy = pd.merge(
        root_node_energy.query("NodeID == @node_id and timeInterval == 3600"),
        nodes.filter(["ID", "Name"]),
        left_on="RootNodeID",
        right_on="ID"
    ).\
    sort_values(["Name", "timestamp"]).\
    assign(
        datetime=lambda x: pd.to_datetime(x["timestamp"], unit="s"),
        log_energy = lambda x: np.log10(x["Energy"]),
        previous_datetime = lambda x: x.groupby(["Name"])["datetime"].shift(1)
    ).\
    filter(["previous_datetime", "datetime", "Name", "log_energy"]).\
    query("previous_datetime.notna() and log_energy > 0").\
    reset_index(drop=True)
    
    # Create a timeline plot for root node energy consumption
    fig_timeline = px.timeline(root_node_energy, x_start = "datetime", x_end = "previous_datetime", y = "Name", color = "log_energy", color_continuous_scale = "OrRd")

    # Add multiple subplots to display battery and app runtime data
    fig = make_subplots(rows = 3, cols = 1, figure = fig_timeline, shared_xaxes = True, vertical_spacing = 0, row_heights = [0.4, 0.3, 0.3])


    fig = fig.\
    add_trace(
        go.Scatter(
            x = battery_ui["datetime"], y = battery_ui["battery"],
            fill = "tozeroy", fillcolor = "rgba(3, 166, 120, .5)",
            mode = "none", name = "", showlegend = False
            ), row=2, col=1
        ).\
    add_trace(
        go.Scatter(
            x = battery_ui["datetime"], y = battery_ui["battery"],
            line = dict(color = "rgba(3, 166, 120, 1)", width = 1),
            mode = "lines", name="Battery Level", showlegend = False
            ), row=2, col=1
        ).\
    add_trace(
        go.Scatter(
            x = battery_ui["datetime"], y = battery_ui["battery_start"],
            marker = dict(
                color = battery_ui["state"].map({"Charging": "#267365", "Not Charging": "#F28705"}),
                line = dict(color = "white", width = 1),
                symbol = "circle", size = 6
                ),
            mode = "markers", name = "Battery Status", text = battery_ui["state"], showlegend = False
            ), row=2, col=1
        ).\
    add_trace(
        go.Scatter(
            x = app_run_time["datetime"], y = app_run_time["background_duration"] + app_run_time["foreground_duration"],
            line = dict(color = "rgba(150, 255, 175, 1)", width = 1, shape = "hv"),
            mode = "lines", name = "Background", fill = None, showlegend = False
            ), row=3, col=1
        ).\
    add_trace(
        go.Scatter(
            x = app_run_time["datetime"], y = app_run_time["foreground_duration"],
            line = dict(color = "rgba(150, 255, 175, 1)", width = 1, shape = "hv"),
            mode = "lines", name = "Background", showlegend = False,
            fill = 'tonexty', fillcolor = "rgba(150, 255, 175, 1)"
            ), row=3, col=1
        ).\
    add_trace(
        go.Scatter(
            x = app_run_time["datetime"], y = app_run_time["foreground_duration"],
            line = dict(color = "rgba(255, 82, 74, 1)", width = 1, shape = "hv"),
            mode = "lines", name = "Foreground", showlegend = False,
            fill = 'tozeroy', fillcolor = "rgba(255, 82, 74, 1)"
            ), row=3, col=1
        ).\
    update_layout(
    template="plotly_dark",
    width = 1200,
    height = 900,
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis = dict(title = None),
    xaxis2 = dict(title = None),
    yaxis=dict(title="Node Energy", gridcolor="rgba(128, 128, 128, 0.1)"),
    yaxis2=dict(title="Battery", gridcolor="rgba(128, 128, 128, 0.1)"),
    yaxis3=dict(title="Duration (s)", gridcolor="rgba(128, 128, 128, 0.1)")
    ).\
    update_coloraxes(showscale=False)

    # Display the final figure in Streamlit
    st.plotly_chart(fig)
