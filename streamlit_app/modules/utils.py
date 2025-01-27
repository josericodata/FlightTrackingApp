import requests
import pandas as pd
from geopy.distance import geodesic
import folium
from folium.plugins import MarkerCluster
import os
from datetime import datetime, timezone

# OpenSky API Base URL
BASE_URL = "https://opensky-network.org/api/states/all"
# OpenFlights URL
OPENFLIGHTS_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat"

# Load airport data
def load_airports():
    url = "https://ourairports.com/data/airports.csv"
    airports = pd.read_csv(url)
    airports = airports[['ident', 'name', 'latitude_deg', 'longitude_deg', 'type']]
    airports = airports[airports['type'] == 'large_airport']  # Filter large airports
    return airports

# Fetch airline data for dropdown
def get_airline_dropdown_data():
    try:
        # Define column names for OpenFlights dataset
        column_names = ["AirlineID", "Name", "Alias", "IATA", "ICAO", "Callsign", "Country", "Active"]

        # Load airline data
        airlines_df = pd.read_csv(
            OPENFLIGHTS_URL,
            header=None,
            names=column_names,
            na_values=["\\N"],
            usecols=["Name", "ICAO", "Active"]
        )

        # Filter only active airlines and drop rows with missing ICAO codes
        airlines_df = airlines_df[(airlines_df["Active"] == "Y") & (airlines_df["ICAO"].notna())]

        # Normalize data and prepare for dropdown
        airlines_df = airlines_df.rename(columns={"ICAO": "ShortName", "Name": "LongName"})
        airlines_df["LongName"] = airlines_df["LongName"].str.strip()

        # Separate airlines starting with numbers
        starts_with_number = airlines_df["LongName"].str[0].str.isnumeric()

        # Sort alphabetically and place numeric starters at the end
        sorted_airlines = pd.concat([
            airlines_df[~starts_with_number].sort_values(by="LongName"),
            airlines_df[starts_with_number].sort_values(by="LongName")
        ]).reset_index(drop=True)

        # Create concatenated column for dropdown
        sorted_airlines["Airline"] = sorted_airlines["LongName"] + " - " + sorted_airlines["ShortName"]

        return sorted_airlines[["ShortName", "Airline"]]
    except Exception as e:
        print(f"Error loading OpenFlights data: {e}")
        return pd.DataFrame(columns=["ShortName", "Airline"])

# Fetch flight data from OpenSky API
def fetch_flight_data():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Filter flights by airline code (callsign prefix)
def filter_by_airline(flights_df, airline_code):
    flights_df = flights_df.copy()
    flights_df.loc[:, 'callsign'] = flights_df['callsign'].str.strip()
    return flights_df[flights_df['callsign'].str.startswith(airline_code, na=False)]

# Find the nearest airport
def find_nearest_airport(lat, lon, airports):
    flight_position = (lat, lon)
    distances = airports.apply(
        lambda row: geodesic(flight_position, (row['latitude_deg'], row['longitude_deg'])).kilometers,
        axis=1
    )
    nearest_index = distances.idxmin()
    nearest_airport = airports.loc[nearest_index]
    return nearest_airport['name'], nearest_airport['ident'], distances[nearest_index]

# Convert Unix timestamps to human-readable time (hour)
def convert_timestamp_to_hour(unix_time):
    if pd.notna(unix_time):
        return datetime.fromtimestamp(int(unix_time), tz=timezone.utc).strftime('%H:%M:%S')
    return None

# Generate flight map with auto-zoom
def generate_flight_map(flights_df, airports):
    if flights_df.empty:
        # If no flights, return a default global map
        return folium.Map(location=[0, 0], zoom_start=2)

    # Calculate the center of all flight coordinates
    center_lat = flights_df['latitude'].mean()
    center_lon = flights_df['longitude'].mean()

    # Create a base map centered on the flights
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)  # Adjust zoom_start as needed
    marker_cluster = MarkerCluster().add_to(m)

    # Local airplane icon path
    plane_icon_url = os.path.join("assets", "images", "airplane.png")

    for _, flight in flights_df.iterrows():
        if pd.notna(flight['latitude']) and pd.notna(flight['longitude']):
            # Find the nearest airport
            nearest_airport, airport_code, _ = find_nearest_airport(
                flight['latitude'], flight['longitude'], airports
            )
            # Popup info
            popup_info = f"""
                <b>Callsign:</b> {flight['callsign']}<br>
                <b>Departing From:</b> {flight['departingFrom']}<br>
                <b>Estimated Arrival:</b> {nearest_airport} ({airport_code})
            """
            # Use the local airplane icon
            icon = folium.CustomIcon(
                icon_image=plane_icon_url,  # Local path to airplane image
                icon_size=(40, 40)  # Adjust size as needed
            )
            # Add marker to the map
            folium.Marker(
                location=[flight['latitude'], flight['longitude']],
                popup=popup_info,
                icon=icon
            ).add_to(marker_cluster)

    return m

def process_flights(selected_airline_code):
    # Load airport data
    airports = load_airports()

    # Fetch OpenSky flight data
    opensky_data = fetch_flight_data()

    if opensky_data and "states" in opensky_data:
        # Define columns and create DataFrame
        columns = [
            "icao24", "callsign", "origin_country", "time_position", "last_contact",
            "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
            "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
            "spi", "position_source"
        ]
        flights_df = pd.DataFrame(opensky_data["states"], columns=columns)

        # Filter flights for the selected airline
        filtered_flights = filter_by_airline(flights_df, selected_airline_code).dropna(subset=['latitude', 'longitude']).copy()

        # Handle empty DataFrame
        if filtered_flights.empty:
            return pd.DataFrame(columns=[
                "callsign", "departingFrom", "estimatedArrivalAt", "timePosition",
                "altitude(m)", "speedKmh", "longitude", "latitude", "icao24"
            ])

        # Define the classify_altitude function
        def classify_altitude(row):
            if row["baro_altitude"] == 0 or pd.isna(row["baro_altitude"]):  # Altitude is 0 or missing
                if row["velocity"] == 0:  # Speed is also 0
                    return "Grounded"
                else:
                    return "Arriving/Taking Off"
            return f"{row['baro_altitude']:.2f}"  # Otherwise, return the actual altitude as a string with units

        # Apply logic to determine altitude and nearest airport
        filtered_flights[["altitude(m)", "estimatedArrivalAt"]] = filtered_flights.apply(
            lambda row: (
                classify_altitude(row),
                find_nearest_airport(row["latitude"], row["longitude"], airports)[0]
                if row["baro_altitude"] < 1000 else "NotCloseToArrival"
            ),
            axis=1,
            result_type="expand"
        )

        # Convert timestamps to readable time
        filtered_flights["timePosition"] = filtered_flights["time_position"].apply(convert_timestamp_to_hour)

        # Convert speed from m/s to km/h
        filtered_flights["velocity"] = filtered_flights["velocity"].fillna(0)  # Fill missing speed with 0
        filtered_flights["speedKmh"] = filtered_flights["velocity"] * 3.6  # Convert to km/h

        # Rename other columns
        column_rename_map = {
            "origin_country": "departingFrom",
            "timePosition": "timePosition"
        }
        filtered_flights.rename(columns=column_rename_map, inplace=True)

        # Select specific columns for output
        display_columns = [
            "callsign", "departingFrom", "estimatedArrivalAt", "timePosition",
            "altitude(m)", "speedKmh", "longitude", "latitude", "icao24"
        ]
        return filtered_flights[display_columns].reset_index(drop=True)

    else:
        print("No flight data available.")
        return pd.DataFrame(columns=[
            "callsign", "departingFrom", "estimatedArrivalAt", "timePosition",
            "altitude(m)", "speedKmh", "longitude", "latitude", "icao24"
        ])


