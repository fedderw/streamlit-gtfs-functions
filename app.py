import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from gtfs_functions import Feed
from gtfs_functions.gtfs_plots import map_gdf
from streamlit_folium import folium_static, st_folium
import plotly.express as px

# call to render Folium map in Streamlit
st.set_page_config(
    layout="wide",
    page_icon="🚌",
    page_title="GTFS Explorer App",
)

direction_name_int_map = {"Outbound": 0, "Inbound": 1}
direction_int_name_map = {0: "Outbound", 1: "Inbound"}


# App title and description
st.title("Bus System Explorer App")
st.write("Explore the speed and frequency of a bus system")
# Read the gtfs feed and perform analysis
# Function to read the GTFS feed and return the feed object
# You should cache your pygwalker renderer, if you don't want your memory to explode
@st.cache_resource
def get_feed(gtfs_feed_url):
    return Feed(
        gtfs_feed_url,
        time_windows=[0, 5, 9, 12, 16, 19, 24],
        busiest_date=True,
    )

@st.cache_data
def load_data(_feed):
  
    feed.get_files()
    stop_freq = feed.stops_freq
    # Get trips per hour by extracted the integers from the window column that are in format "5:00-6:30"
    stop_freq["window_start"] = stop_freq.window.str.extract(r"(\d+):").astype(int)
    stop_freq["window_end"] = stop_freq.window.str.extract(r"-(\d+):").astype(int)
    stop_freq["tph"] = stop_freq.ntrips / (
        stop_freq.window_end - stop_freq.window_start
    )
    line_freq = feed.lines_freq
    # segments_gdf = feed.segments
    # feed.get_speeds()
    # speeds = feed.avg_speeds
    # speeds['speed_mph'] = speeds['speed_kmh'] * 0.621371
    # speeds['avg_route_speed_mph'] = speeds['avg_route_speed_kmh'] * 0.621371
    # speeds['segment_max_speed_mph'] = speeds['segment_max_speed_kmh'] * 0.621371
    # segments_freq = feed.segments_freq




    return stop_freq, line_freq

presets = {"MDOT MTA Local Bus":"https://feeds.mta.maryland.gov/gtfs/local-bus","Charm City Circulator":"https://transportation.baltimorecity.gov/gtfsfile"}

gtfs_path = st.text_input(
    r"GTFS Static URL", "https://feeds.mta.maryland.gov/gtfs/local-bus"
)
st.link_button("Search for more source feeds","https://www.transit.land/operators")
feed = get_feed(f"{gtfs_path}")
stop_freq, line_freq = load_data(feed)




# Create a streamlit multiselect for the unique values in direction and window

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

fig = px.histogram(
    gdf, 
    x='min_per_trip', 
    title='Stop frequencies',
    template='simple_white', 
    nbins =20)

# Update titles to be more readable
fig.update_layout(
    xaxis_title_text='Minutes per trip',
    yaxis_title_text='Number of stops',
    bargap=0.1
)

# Show the direction and the window in the title
fig.update_layout(title_text=f"Stop frequencies for {direction_int_name_map[selected_direction]} direction and {selected_window} window")

# Display the histogram in Streamlit
st.plotly_chart(fig)

# New Section to show line frequencies
st.write("Line Frequencies")


gdf = line_freq.loc[(condition_dir & condition_window),:].reset_index()

m = map_gdf(
  gdf = gdf,
  variable = 'ntrips',
  colors = ["#d13870", "#e895b3" ,'#55d992', '#3ab071', '#0e8955','#066a40'],
  tooltip_var = ['route_name'] ,
  tooltip_labels = ['Route: '],
  breaks = [10, 20, 30, 40, 120, 200]

)


# Display the map in Streamlit
st_data = folium_static(m, height=600)

fig = px.histogram(
    gdf, 
    x='min_per_trip', 
    title='Line frequencies',
    template='simple_white', 
    nbins =20)

# Update titles to be more readable
fig.update_layout(
    xaxis_title_text='Headways',
    yaxis_title_text='Number of lines',
    bargap=0.1
)

# Show the direction and the window in the title
fig.update_layout(title_text=f"Line frequencies for {direction_int_name_map[selected_direction]} direction and {selected_window} window")


st.plotly_chart(fig)
