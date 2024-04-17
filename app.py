import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from gtfs_functions import Feed
from gtfs_functions.gtfs_plots import map_gdf
from streamlit_folium import folium_static, st_folium

# call to render Folium map in Streamlit
st.set_page_config(
    layout="wide",
    page_icon="🚌",
    page_title="GTFS Explorer App",
)



# App title and description
st.title("Bus System Explorer App")
st.write("Explore the speed and frequency of a bus system")
# Read the gtfs feed and perform analysis
# Function to read the GTFS feed and return the feed object


@st.cache_data
def load_data(gtfs_feed_url):
    feed = Feed(
        gtfs_feed_url,
        time_windows=[0, 5, 9, 12, 16, 19, 24],
        busiest_date=True,
    )
    feed.get_files()
    stop_freq_df = feed.stops_freq

    return feed, stop_freq_df


gtfs_path = st.text_input(
    r"GTFS Static URL", "https://feeds.mta.maryland.gov/gtfs/local-bus"
)
# st.write(gtfs_path)
# date = st.date_input('Select Date')
feed, stop_freq = load_data(f"{gtfs_path}")
# gtfs_feed_url = st.text_input(r"https://feeds.mta.maryland.gov/gtfs/local-bus")
# feed = load_gtfs_feed(gtfs_path)
# routes = feed.routes
# st.dataframe(routes)

# shapes = feed.shapes
# feed
# feed.files
# feed.get_files()
# feed = Feed(gtfs_feed_url)
# feed = Feed(gtfs_feed_url, time_windows=[0, 6, 10, 12, 16, 19, 24])

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
# st.write(stop_freq_df.info())
# st.dataframe(stop_freq_df.head())
# Filter the stop frequencies based on the selected routes
# filtered_stop_freq_df = stop_freq_df[stop_freq_df.route_id.isin(selected_routes)]
# Display the stop frequencies on a map using gtfs_functions plotting function
# st.write(map_gdf(stop_freq_df, 'ntrips', ["#d13870", "#e895b3", '#55d992', '#3ab071', '#0e8955', '#066a40'], ['min_per_trip'], ['frequency: '], [10, 20, 30, 40, 120, 200]))

# Get trips per hour by extracted the integers from the window column that are in format "5:00-6:30"
stop_freq["window_start"] = stop_freq.window.str.extract(r"(\d+):").astype(int)
stop_freq["window_end"] = stop_freq.window.str.extract(r"-(\d+):").astype(int)
stop_freq["tph"] = stop_freq.ntrips / (
    stop_freq.window_end - stop_freq.window_start
)
# For debugging, print a dataframe showing the unique window_start and window_end values
st.write(stop_freq[['window_start', 'window_end']].drop_duplicates())

# Create a streamlit multiselect for the unique values in direction and window
direction_name_int_map = {"Outbound": 0, "Inbound": 1}
direction_int_name_map = {0: "Outbound", 1: "Inbound"}

selected_direction = st.selectbox(
    "Select Direction", stop_freq.direction_id.unique(), format_func=direction_int_name_map.get
)
selected_window = st.selectbox("Select Time Window", stop_freq.window.unique())

# Apply the selected filters to the dataframe
condition_dir = stop_freq.direction_id == selected_direction
condition_window = stop_freq.window == selected_window

# Filter the dataframe based on the selected filters
gdf = stop_freq.loc[(condition_dir & condition_window), :].reset_index()

# Generate the map based on the filtered dataframe
m = map_gdf(
    gdf=gdf,
    variable="tph",
    colors=["#d13870", "#e895b3", "#55d992", "#3ab071", "#0e8955", "#066a40"],
    tooltip_var=["min_per_trip","tph"],
    tooltip_labels=["Headway: ", "Trips per hour: "],
    breaks=[1, 2, 3, 4, 10, 50],
)

# Display the map in Streamlit
st_data = folium_static(m, height=600)


# Additional visualizations using plotly and other libraries
# You can add more visualizations based on the specific data returned by the gtfs_functions library

# The rest of the visualization code based on the gtfs_functions library examples and other customizations can be incorporated here
