import streamlit as st
from streamlit_folium import st_folium
from modules.styles import set_background_image, apply_global_styles, apply_map_styles
from modules.utils import (
    load_airports,
    get_airline_dropdown_data,
    process_flights,
    generate_flight_map
)

# Set the page configuration
st.set_page_config(
    page_title="Streamlit Flight Tracking App",  # Page title
    page_icon="✈️"  # Favicon
)

# Path to the background image
background_image_url = "https://raw.githubusercontent.com/josericodata/FlightTrackingApp/main/assets/images/flights.jpeg"

# Set the background image
set_background_image(background_image_url)
apply_global_styles()
apply_map_styles()

# Initialize session state
if "flights_data" not in st.session_state:
    st.session_state["flights_data"] = None  # Cache fetched flight data
    st.session_state["airports_data"] = load_airports()  # Load airport data once
    st.session_state["flight_map"] = None  # Cache the generated map
    st.session_state["filtered_flights"] = None  # Cache filtered flights
    st.session_state["selected_airline"] = None  # Cache selected airline
    st.session_state["cached_map"] = None  # Add cached_map for map caching

# Load airport data from session state
airports = st.session_state["airports_data"]

# Fetch airline dropdown data
airline_dropdown_data = get_airline_dropdown_data()

# App title
st.title("Flight Tracking App")

# Select an airline
selected_airline = st.selectbox(
    "Select Airline",
    options=["Select Airline"] + airline_dropdown_data["Airline"].tolist()
)

if selected_airline != "Select Airline":
    # Fetch the airline code
    airline_code = airline_dropdown_data.loc[airline_dropdown_data["Airline"] == selected_airline, "ShortName"].values[0]

    # Check if a new airline is selected or if the filtered flights have changed
    if st.session_state["selected_airline"] != airline_code:
        # Update session state
        st.session_state["selected_airline"] = airline_code
        st.session_state["filtered_flights"] = process_flights(airline_code)
        st.session_state["flight_map"] = generate_flight_map(st.session_state["filtered_flights"])

        # Cache the generated map
        st.session_state["cached_map"] = st.session_state["flight_map"]

    # Display the cached map
    if st.session_state["cached_map"]:
        st.subheader(f"Flights for {selected_airline}")
        st_folium(st.session_state["cached_map"], width=1000, height=800)

    # Display the filtered flight data
if st.session_state["filtered_flights"] is not None and not st.session_state["filtered_flights"].empty:
    st.subheader("Flight Data")
    st.dataframe(st.session_state["filtered_flights"], use_container_width=True)  # Enable full-width display
else:
    st.write("No flight data available for the selected airline.")

# Display API errors if any
if "api_error" in st.session_state and st.session_state["api_error"]:
    st.warning(st.session_state["api_error"])
