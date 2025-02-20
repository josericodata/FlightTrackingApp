# ✈️ **Flight Tracking App**


**The Flight Tracking App is a real-time flight visualisation platform built with Python and Streamlit. It utilises live data from the OpenSky API to display current flight information and geographical positions on an interactive map. This app is designed for aviation enthusiasts, researchers, and professionals to monitor flights with ease.**

---

## 🧬 **Project Structure**
```bash
FlightTrackingApp
├── assets/         
│   ├── data/
│   │   └── airports.csv
│   ├── dataCleaning/
│   │   └── flightTrackingAppLogicFlow.ipynb
│   ├── gifs/
│   │   └── flights.gif
│   └── images/ 
│       ├── airplane.png
│       └── flights.png
├── streamlit_app/
│   ├── modules/
│   │   ├── styles.py
│   │   └── utils.py
│   └── app.py   
├── LICENSE                 
├── README.md               
└── requirements.txt        
```

---

## 🛠️ **How It's Built**

The Flight Tracking App is developed using the following tools and frameworks:

- **Streamlit** - To create a seamless and user-friendly web interface.
- **Folium** - To render an interactive map for visualising flight data.
- **Pandas** - To handle and process live flight and airport data.
- **OpenSky API** - To retrieve real-time flight information.
- **Geopy** - To compute distances and identify nearby airports.
- **GitHub** - To store assets like images and manage project files.
- **Custom Modules** - `styles.py` and `utils.py` for background styling and data processing.

---

## 📡 **Data Sources**

The Flight Tracking App leverages the following data sources:

1. **[OpenSky Network API](https://opensky-network.org/api/states/all):**
   - Provides real-time flight states (latitude, longitude, altitude, callsign, etc.) for active flights.
   - Supplies data used to filter and track flights based on the airline and location.

2. **[OurAirports Dataset](https://ourairports.com/data/):**
   - A static dataset containing details of global airports (latitude, longitude, names, and identifiers).
   - Enables nearest airport computation for flights.

3. **[OpenFlights Airline Database](https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat):**
   - A dataset containing airline names and ICAO codes.
   - Helps in identifying and filtering flights by airline callsigns.

---

## 🧑‍💻 **How It Works**

1. **Airline Selection**: Users select an airline from a dropdown menu populated with active airlines using their ICAO codes (e.g., RYR for Ryanair).
2. **Data Processing**:
   - Real-time flight data is fetched using the OpenSky API.
   - Flights are filtered based on the selected airline and geographical coordinates.
   - Nearest airports are computed using geopy for flights close to the ground.
3. **Visualisation**:
   - The filtered flights are displayed on an interactive Folium map.
   - A detailed table of flight data (callsign, altitude, speed, position, and estimated arrival) is presented below the map.
4. **Map Interaction**:
   - Users can hover, zoom, or pan the map to explore flight positions dynamically.
   - Each flight marker displays additional details like callsign and destination on hover.

---

## 🚀 **Getting Started**

### **Local Installation**

1. Clone the repository:
```bash
git clone https://github.com/josericodata/FlightTrackingApp.git
```
**Hint:** Replace `user` with `josericodata` in the URL above. I am deliberately asking you to pause here so you can support my work. If you appreciate it, please consider giving the repository a star or forking it. Your support means a lot—thank you! 😊

2. Navigate to the project directory:

```bash

cd FlightTrackingApp

```

3. Create a virtual environment:
```bash
python3 -m venv venvFlightTrackingApp
```

4. Activate the virtual environment:
```bash
source venvFlightTrackingApp/bin/activate
```

5. Install requirements:
```bash
pip install -r requirements.txt
```

6. Navigate to the app directory:
```bash
cd streamlit_app
```

7. Run the app:
```bash
streamlit run app.py
```

The app will be live at ```http://localhost:8501```

---

## 🎬 **Demo**
  
### Page 1: Flight Tracking App
![Flight Tracking App](https://raw.githubusercontent.com/josericodata/FlightTrackingApp/main/streamlit_app/assets/gifs/flights.gif)


---

### ▶️ Watch the YouTube Tutorial


[![Real-Time Flight Tracker with Python & Streamlit Live Flight Map Using OpenSky API](https://img.youtube.com/vi/ZjZRb15m5KQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=ZjZRb15m5KQ "Click to play")

Click the image above or [here](https://www.youtube.com/watch?v=ZjZRb15m5KQ) to watch the video on YouTube.

---


## 🔧 **Environment Setup**

The Flight Tracking App is built and tested using the following software environment:

- **Operating System**: Ubuntu 22.04.5 LTS (Jammy)
- **Python Version**: Python 3.10.12

Ensure your environment matches these specifications to deploy the app successfully.

---

## 📋 **Important Notes**

1. **API Keys**: Ensure that the OpenSky API is reachable and has sufficient capacity for data retrieval.
2. **Assets**: Background and map marker images are hosted on GitHub. The URLs must be valid and accessible in the deployment environment.

---

## 🔮 **Future Enhancements**

Planned improvements include:

- **Flight Path Prediction**: Integrate machine learning models to predict flight paths.
- **Custom Filters**: Allow users to filter by altitude, speed, or specific regions.
- **Historical Data Analysis**: Incorporate historical flight data for trend analysis.

---

## 📈 **Displayed Data**

### Data Table Columns:
1. **Callsign**: Unique identifier for the flight.
2. **Departing From**: Country of origin.
3. **Estimated Arrival**: Airport where the flight is heading (if close to descent).
4. **Time Position**: Time when the position was recorded (UTC).
5. **Altitude (m)**: Barometric altitude in meters.
6. **Speed (km/h)**: Current velocity of the aircraft.
7. **Longitude/Latitude**: Geographical position of the flight.
8. **ICAO24**: Unique identifier for the aircraft.

---

## 🧪 **Logic and Data Exploration**

To better understand the logic and data processing pipeline used in the Flight Tracking App, a Jupyter Notebook has been created. It provides a detailed walkthrough of the data cleaning, exploration, and preparation steps, ensuring transparency and reproducibility in the app's development.

You can explore the notebook here: [FlightTrackingAppLogicFlow.ipynb](https://github.com/josericodata/FlightTrackingApp/blob/main/streamlit_app/assets/dataCleaning/flightTrackingAppLogicFlow.ipynb)

This notebook covers:
- Loading and inspecting OpenSky Network data.
- Filtering flights based on airline codes (callsigns).
- Deriving attributes like departure and estimated arrival.
- Data transformation for real-time visualisation.

---

## ‼️ **Service Availability Warning**

The Flight Tracking App relies on real-time flight data from the **OpenSky Network API**. Occasionally, the OpenSky API may experience downtime, returning a **503 Service Temporarily Unavailable** error. 

If you encounter this issue, please wait a few minutes and try again. You can also check the OpenSky Network website:  
🔗 [https://opensky-network.org](https://opensky-network.org)  

We appreciate your patience! 🚀

---

## 🤝 **Open Pull Requests**

If you find any bug, feel free to contact me by opening a pull request on GitHub or via email at **maninastre@gmail.com**.

---
  
## ⚠️ **Disclaimer**

This app is a personal project designed to demonstrate data visualisation and real-time processing capabilities. It should not be used for operational flight tracking or aviation safety purposes.

---

Enjoy exploring the skies with the **Flight Tracking App**! ✈️