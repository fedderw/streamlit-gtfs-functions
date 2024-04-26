import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import streamlit as st
from gtfs_functions import Feed
from gtfs_functions.gtfs_plots import map_gdf
from streamlit_folium import folium_static, st_folium

from app import direction_int_name_map, direction_name_int_map

# call to render Folium map in Streamlit
st.set_page_config(
    layout="wide",
    page_icon="🚌",
    page_title="View scheduled speeds",
)


# App title and description
# st.title("Bus System Explorer App")
st.write(st.session_state)
gtfs_path = st.session_state["gtfs_path"]


@st.cache_data
def load_speeds(_feed):
    # feed = Feed(
    #     gtfs_path,
    #     time_windows=[0, 5, 9, 12, 16, 19, 24],
    #     busiest_date=True,
    # )
    segments_gdf = _feed.segments
    _feed.get_speeds()
    speeds = _feed.avg_speeds
    speeds["speed_mph"] = speeds["speed_kmh"] * 0.621371
    speeds["avg_route_speed_mph"] = speeds["avg_route_speed_kmh"] * 0.621371
    speeds["segment_max_speed_mph"] = (
        speeds["segment_max_speed_kmh"] * 0.621371
    )
    # Map direction_id to direction_name
    # speeds['direction_name'] = speeds['direction_id'].map(direction_int_name_map) if 'direction_id' in speeds.columns else None
    # Python
    if "direction_id" in speeds.columns:
        if set(speeds["direction_id"].unique()) <= {0, 1}:
            speeds["direction_name"] = speeds["direction_id"].map(
                direction_int_name_map
            )
        else:
            speeds["direction_name"] = speeds["direction_id"].apply(
                lambda x: direction_int_name_map.get(x, "NA")
            )
    else:
        speeds["direction_name"] = None
    segments_freq = _feed.segments_freq

    return segments_gdf, speeds, segments_freq


presets = {
    "MDOT MTA Local Bus": "https://feeds.mta.maryland.gov/gtfs/local-bus",
    "Charm City Circulator": "https://transportation.baltimorecity.gov/gtfsfile",
}

st.link_button(
    "Search for more GTFS source feeds", "https://www.transit.land/operators"
)


segments_gdf, speeds, segments_freq = load_speeds(st.session_state.feed)

# Get unique route names
unique_routes = speeds["route_name"].unique()

# Create a multiselect widget
selected_routes = st.multiselect("Select Routes", unique_routes, ["All lines"])

# Filter the DataFrame based on selected routes
filtered_speeds = speeds[speeds["route_name"].isin(selected_routes)]

# Display the filtered DataFrame
# st.dataframe( pd.DataFrame(speeds.drop(columns='geometry')))

by_hour = filtered_speeds.pivot_table(
    "speed_mph", index=["direction_name", "window"], aggfunc=["mean", "std"]
).reset_index()
by_hour.columns = ["_".join(col).strip() for col in by_hour.columns.values]
by_hour["hour"] = by_hour.window_.apply(lambda x: int(x.split(":")[0]))
by_hour.sort_values(by="hour", ascending=True, inplace=True)
# Scatter
fig = px.line(
    by_hour,
    x="window_",
    y="mean_speed_mph",
    template="simple_white",
    error_y="std_speed_mph",
    #    color ='direction_name_',
    facet_col="direction_name_",
)

fig.update_yaxes(rangemode="tozero")

# Add better titles to the plot
fig.update_layout(
    title="Average speed by time window",
    xaxis_title="Time window",
    yaxis_title="Average speed (mph)",
    legend_title="Direction",
    showlegend=True,
    template="simple_white",
    height=600,
    width=1000,
    # margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig)

st.dataframe(pd.DataFrame(filtered_speeds.drop(columns="geometry")))
st.dataframe(by_hour)
