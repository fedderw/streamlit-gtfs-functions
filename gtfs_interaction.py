from gtfs_functions_sample import Feed

# Define a function to create and process GTFS feed objects
def create_feed(gtfs_url, start_date=None, end_date=None, time_windows=None):
    """
    Initialize a GTFS Feed object and parse routes and stops.
    Args:
        gtfs_url (str): URL or path to the GTFS zip file.
        start_date (str): Start date for the feed data processing.
        end_date (str): End date for the feed data processing.
        time_windows (list): List of time windows for frequency analysis.

    Returns:
        dict: Dictionary containing routes and stops DataFrames.
    """
    # Create a Feed object with or without a date range
    feed = Feed(gtfs_url, start_date=start_date, end_date=end_date, time_windows=time_windows)

    # Parse routes and stops from the feed
    routes = feed.routes
    stops = feed.stops

    return {'routes': routes, 'stops': stops}
