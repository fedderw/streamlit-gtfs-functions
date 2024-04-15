import streamlit as st
import geopandas as gpd
from gtfs_functions.gtfs_plots import map_gdf

# Define a function to display geographic data in Streamlit using Geopandas and mapping functions
def display_geographic_data(gdf, title, color_column, tooltip_vars):
    """
    Display geographic data on a Streamlit map.
    Args:
        gdf (Geodataframe): Geodataframe containing the geographic data.
        title (str): Title of the map.
        color_column (str): Column name to base the color on.
        tooltip_vars (list): List of column names to display as tooltips.
    """
    # Set the title of the map section
    st.subheader(title)

    # Plot the geodataframe using Streamlit's map function
    st.map(gdf)

    # Optionally, use advanced mapping to add tooltips and color based on variables
    map_gdf(gdf=gdf, variable=color_column, tooltip_var=tooltip_vars)
