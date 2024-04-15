import streamlit as st
from gtfs_functions import Feed

# Display a title on the Streamlit dashboard
st.title('Maryland MTA Bus and Charm City Circulator Dashboard')

# Specify GTFS data paths for the feeds
ccc_gtfs_path = 'https://transportation.baltimorecity.gov/gtfsfile'
mta_gtfs_path = 'https://feeds.mta.maryland.gov/gtfs/local-bus'

# Create Feed objects for both the CCC and MDOT MTA Local Bus
ccc_feed = Feed(ccc_gtfs_path, start_date='2023-10-01', end_date='2023-10-31')
mta_feed = Feed(mta_gtfs_path, start_date='2023-10-01', end_date='2023-10-31')

# Generate data frames for routes and stops using the Feed object
ccc_routes = ccc_feed.routes
mta_routes = mta_feed.routes
ccc_stops = ccc_feed.stops
mta_stops = mta_feed.stops

# Create a multi-select box for users to select which data sets to view
data_selection = st.multiselect('Select data to view:', ['CCC Routes', 'MTA Routes', 'CCC Stops', 'MTA Stops'])

# Conditionally display data based on user selection
if 'CCC Routes' in data_selection:
    st.write('CCC Routes')
    st.dataframe(ccc_routes)

if 'MTA Routes' in data_selection:
    st.write('MTA Routes')
    st.dataframe(mta_routes)

if 'CCC Stops' in data_selection:
    st.write('CCC Stops')
    st.dataframe(ccc_stops)

if 'MTA Stops' in data_selection:
    st.write('MTA Stops')
    st.dataframe(mta_stops)
