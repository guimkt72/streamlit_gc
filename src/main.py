import streamlit as st
import pandas as pd
from data_read import get_data

# Add caching to prevent reloading data on every interaction
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    try:
        df = get_data()  # Now reading from Excel file
        if df is None or df.empty:
            st.error("Could not load data from Excel file")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Initialize session state for data if not exists
if 'data' not in st.session_state:
    st.session_state.data = None

# Add a refresh button
if st.button('Refresh Data'):
    st.session_state.data = None

# Load data if not in session state
if st.session_state.data is None:
    st.session_state.data = load_data()

# Only show the dashboard if we have data
if st.session_state.data is not None:
    df = st.session_state.data
    
    st.title("Game Statistics Dashboard")

    # Define metrics that can be plotted
    metrics = {
        'KDR': 'kdr',
        'ADR': 'adr',
        'Kills': 'matou',
        'Deaths': 'morreu',
        'Multi Kills': 'multikills',
        'First Kills': 'firstkills',
        'Headshot Rate': 'headshotrate',
        'Bombs Planted': 'bomb_planted',
        'Bombs Defused': 'bomb_defused',
        'Matches Played': 'matches',
        'Kills Per Map': 'killsPerMap',
        'Deaths Per Map': 'deatchsPerMap',
        'First Kills Per Map': 'firstKillsPerMap',
        'Bombs Planted Per Map': 'bombPlantedPerMap',
        'Bombs Defused Per Map': 'bombDefusedPerMap'
    }

    # Let user select the metric to analyze with friendly names
    selected_metric_name = st.selectbox("Select metric to analyze", list(metrics.keys()))
    selected_metric = metrics[selected_metric_name]

    # Group the data by month and player, calculating the mean of the selected metric
    grouped_df = df.groupby(['mes', 'nome'])[selected_metric].mean().reset_index()

    # Pivot the data to create a format suitable for plotting
    pivot_df = grouped_df.pivot(index='mes', columns='nome', values=selected_metric)

    # Create the plot using Streamlit's native line chart
    st.subheader(f"{selected_metric_name} by Player Over Time")
    st.line_chart(pivot_df)

    # Show summary statistics
    st.subheader("Summary Statistics")
    summary_df = df.groupby('nome')[selected_metric].agg(['mean', 'min', 'max']).round(2)
    summary_df.columns = ['Average', 'Minimum', 'Maximum']
    st.write(summary_df)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)