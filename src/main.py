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
    
    st.title("Dashboard Player Analysis - CS2")

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

    # Add multi-select for players
    all_players = sorted(df['nome'].unique())
    selected_players = st.multiselect(
        "Select players to analyze",
        options=all_players,
        default=all_players  # Initially select all players
    )

    # Filter the dataframe for selected players
    df_filtered = df[df['nome'].isin(selected_players)]

    # Group the data by month and player, calculating the mean of the selected metric
    grouped_df = df_filtered.groupby(['mes', 'nome'])[selected_metric].mean().reset_index()

    # Pivot the data to create a format suitable for plotting
    pivot_df = grouped_df.pivot(index='mes', columns='nome', values=selected_metric)

    # Create the plot using Streamlit's native line chart
    st.subheader(f"{selected_metric_name} by Player Over Time")
    st.line_chart(pivot_df)

    # Show summary statistics for selected players only
    st.subheader("Resumo estatístico")
    summary_df = df_filtered.groupby('nome')[selected_metric].agg(['mean', 'min', 'max']).round(2)
    summary_df.columns = ['Average', 'Minimum', 'Maximum']
    st.write(summary_df)
#### NEW PART
# Add a divider between sections
    st.markdown("---")
    st.title("Match Analysis Dashboard")

    # Load match data
    from match_data import get_match
    match_df = get_match()

    if match_df is not None:
        # Define metrics for match analysis
        match_metrics = {
            'Kills': 'nb_kill',
            'Assist': 'assist',
            'Deaths': 'death',
            'Damage': 'damage',
            'ADR': 'adr',
            'KDR': 'kdr',
            'Headshot Rate': 'phs',
            'First Kill': 'firstkill',
            'KAST': 'pkast',
            'Hits': 'hits',
            'Level': 'level',
            'Rating': 'rating',
            'Flash Assist': 'flash_assist',
            'Multi Kills': 'multikills'
        }

        # Select match ID
        game_ids = sorted(match_df['game_id'].unique())
        selected_game_ids = st.multiselect(
            "Select matches to analyze",
            options=game_ids,
            default=[game_ids[0]] if game_ids else None
        )

        # Filter by selected matches
        match_df_filtered = match_df[match_df['game_id'].isin(selected_game_ids)]

        # Select players from filtered matches
        match_players = sorted(match_df_filtered['nick'].unique())
        selected_match_players = st.multiselect(
            "Select players to analyze",
            options=match_players,
            default=match_players
        )

        # Select metric for visualization
        selected_match_metric_name = st.selectbox(
            "Select metric to analyze",
            list(match_metrics.keys()),
            key="match_metric"  # Unique key to avoid conflict with previous selectbox
        )
        selected_match_metric = match_metrics[selected_match_metric_name]

        # Filter for selected players
        final_df = match_df_filtered[match_df_filtered['nick'].isin(selected_match_players)]

        # Create visualization
        st.subheader(f"{selected_match_metric_name} by Player and Match")
        
        # Pivot and plot
        pivot_match_df = final_df.pivot(
            index='game_id',
            columns='nick',
            values=selected_match_metric
        )
        st.bar_chart(pivot_match_df)

        # Detailed statistics table
        st.subheader("Match Details")
        
        # Define columns for the detailed table
        display_columns = {
            'game_id': 'Game ID',
            'nick': 'Nick',
            'team': 'Team',
            'updated_at': 'Date',
            'map_name': 'Map',
            'nb_kill': 'Kills',
            'assist': 'Assist',
            'death': 'Deaths',
            'hs': 'HS',
            'damage': 'Damage',
            'adr': 'ADR',
            'kdr': 'KDR',
            'phs': 'HS%',
            'firstkill': 'First Kill',
            'pkast': 'KAST',
            'nb1kill': '1K',
            'nb2kill': '2K',
            'nb3kill': '3K',
            'nb4kill': '4K',
            'nb5kill': '5K',
            'defuse': 'Defuse',
            'bombe': 'Bomb',
            'hits': 'Hits',
            'level': 'Level',
            'flash_assist': 'Flash Assist',
            'multikills': 'Multi Kills',
            'damage_share': 'Damage Share %',
            'kills_share': 'Kills Share %'
        }

        # Create a copy of the filtered DataFrame with renamed columns
        display_df = final_df[display_columns.keys()].copy()
        display_df.columns = display_columns.values()
        
        # Format datetime column
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d %H:%M')
        
        # Round floating point numbers
        float_columns = ['ADR', 'KDR', 'HS%', 'KAST', 'Damage Share %', 'Kills Share %']
        display_df[float_columns] = display_df[float_columns].round(2)

        # Display the table
        st.dataframe(
            display_df.sort_values(['Game ID', 'Team', 'Nick']),
            hide_index=True,
            use_container_width=True
        )

# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
    <p>Developed by Guilherme Oliveira</p>
    <p>Contact: g.soliveira@live.com / @guioliveira72</p>
    </div>
    """, unsafe_allow_html=True)