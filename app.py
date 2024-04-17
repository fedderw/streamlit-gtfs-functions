import streamlit as st
from gtfs_functions_sample import Feed

from gtfs_functions.gtfs_plots import map_gdf
import pandas as pd

# App title and description
st.title('Bus System Explorer App')
st.write('Explore the speed and frequency of a bus system')
# Read the gtfs feed and perform analysis
gtfs_feed_url = st.text_input("https://feeds.mta.maryland.gov/gtfs/local-bus")
date = st.date_input('Select Date')
feed = Feed(gtfs_feed_url)
# User input components
# gtfs_feed_url = st.text_input('Enter Static GTFS Feed URL')
# date = st.date_input('Select Date')

# # Customize time range
# time_windows = [0, 6, 9, 15.5, 19, 22, 24]
# selected_start_time = st.select_slider('Select Start Time', options=time_windows, format_func=lambda x: f'{int(x)}:00')
# selected_end_time = st.select_slider('Select End Time', options=time_windows, format_func=lambda x: f'{int(x)}:00')

# Filter routes
# available_routes = feed(gtfs_feed_url).routes.route_id.unique()
# selected_routes = st.multiselect('Select Routes', available_routes)

# Read the gtfs feed using the provided URL
# gtfs_feed = feed(gtfs_feed_url, time_windows=time_windows)

# Your logic here to use the user inputs and apply the gtfs_functions library to get the desired results

# For example:
# Calculate stop frequencies for the selected date and time range
stop_freq_df = feed.stops_freq
# Filter the stop frequencies based on the selected routes
# filtered_stop_freq_df = stop_freq_df[stop_freq_df.route_id.isin(selected_routes)]
# Display the stop frequencies on a map using gtfs_functions plotting function
map_gdf(stop_freq_df, 'ntrips', ["#d13870", "#e895b3", '#55d992', '#3ab071', '#0e8955', '#066a40'], ['min_per_trip'], ['frequency: '], [10, 20, 30, 40, 120, 200])

# Additional visualizations using plotly and other libraries
# You can add more visualizations based on the specific data returned by the gtfs_functions library

# The rest of the visualization code based on the gtfs_functions library examples and other customizations can be incorporated here
