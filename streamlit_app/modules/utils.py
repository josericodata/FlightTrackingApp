import folium
import requests
import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from datetime import datetime, timezone
from folium.plugins import MarkerCluster
# OpenSky API Base URL
BASE_URL = "https://opensky-network.org/api/states/all"
# OpenFlights URL
OPENFLIGHTS_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat"

@st.cache_data
def load_airports():
    """
    Loads airport data from a local CSV file stored in Streamlit Cloud.
    The function is cached to improve performance and reduce repeated file reads.
    """

    # Read the CSV file
    airports = pd.read_csv("assets/data/airports.csv")

    # Select relevant columns
    airports = airports[['ident', 'name', 'latitude_deg', 'longitude_deg', 'type']]

    # Filter only large airports
    airports = airports[airports['type'] == 'large_airport']

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

# Fetch flight data from OpenSky API with robust error handling
def fetch_flight_data():
    try:
        response = requests.get(BASE_URL)

        if response.status_code == 200:
            return response.json()

        else:
            # Store error message in session state
            st.session_state["api_error"] = (
                f"🚨 OpenSky API Error: **{response.status_code}** - {response.reason}.\n"
                "The OpenSky Network API is currently unavailable or experiencing issues.\n"
                "🔄 **Please try again later.**"
            )
            return None

    except requests.exceptions.RequestException as e:
        st.session_state["api_error"] = (
            f"❌ **Network Error:** Unable to connect to OpenSky API.\n"
            f"Details: {str(e)}\n"
            "Please check your internet connection and try again."
        )
        return None

    except Exception as e:
        st.session_state["api_error"] = (
            f"⚠️ **Unexpected Error:** {str(e)}\n"
            "Something went wrong. Please refresh the page or try again later."
        )
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

def generate_flight_map(filtered_flights):
    if filtered_flights.empty:
        return folium.Map(location=[0, 0], zoom_start=2)

    center_lat = filtered_flights['latitude'].mean()
    center_lon = filtered_flights['longitude'].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(m)

    plane_icon_url = "https://raw.githubusercontent.com/josericodata/FlightTrackingApp/main/assets/images/airplane.png"

    def format_float(value):
        """ Convert value to float and format to 2 decimal places, handle non-numeric cases """
        try:
            return f"{float(value):.2f}"
        except ValueError:
            return value  # Return the original string if it's not a number

    for _, flight in filtered_flights.iterrows():
        if pd.notna(flight['latitude']) and pd.notna(flight['longitude']):
            popup_info = f"""
                <b>Callsign:</b> {flight['callsign']}<br>
                <b>Departing From:</b> {flight['departingFrom']}<br>
                <b>Speed(Km/h):</b> {format_float(flight['speed(Kmh)'])}<br>
                <b>Altitude(m):</b> {format_float(flight['altitude(m)'])}<br>
                <b>Arriving at:</b> {flight['estimatedArrivalAt']}<br>
            """
            icon = folium.CustomIcon(icon_image=plane_icon_url, icon_size=(40, 40))
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
                "altitude(m)", "speed(Kmh)", "longitude", "latitude", "icao24"
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
        filtered_flights["speed(Kmh)"] = filtered_flights["velocity"] * 3.6  # Convert to km/h

        # Rename other columns
        column_rename_map = {
            "origin_country": "departingFrom",
            "timePosition": "timePosition"
        }
        filtered_flights.rename(columns=column_rename_map, inplace=True)

        # Select specific columns for output
        display_columns = [
            "callsign", "departingFrom", "estimatedArrivalAt", "timePosition",
            "altitude(m)", "speed(Kmh)", "longitude", "latitude", "icao24"
        ]
        return filtered_flights[display_columns].reset_index(drop=True)

    else:
        print("No flight data available.")
        return pd.DataFrame(columns=[
            "callsign", "departingFrom", "estimatedArrivalAt", "timePosition",
            "altitude(m)", "speed(Kmh)", "longitude", "latitude", "icao24"
        ])



