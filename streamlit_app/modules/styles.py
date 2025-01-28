import streamlit as st

def set_background_image(image_url):
    import streamlit as st
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )



def apply_global_styles():
    st.markdown(
        """
        <style>

        /* Set the top horizontal bar (header) to black */
        [data-testid="stHeader"] {
            background-color: #f1e4f5 !important;  /* Black background */
            border-bottom: 2px solid #f1e4f5 !important;  /* Black border for seamless look */
        }

        /* Disable the blinking text cursor in dropdown input */
        input {
            caret-color: transparent !important;
        }

        /* Style for the alert box - PURE BLACK, NO OVERLAY */
        div.stAlert {
            background-color: black !important;  /* Pure black */
            border-radius: 10px !important;
            padding: 15px !important;
            color: white !important; /* White text */
            font-weight: bold !important;
            font-size: 18px !important;
            text-align: center !important;
            box-shadow: none !important; /* REMOVE extra background shadow */
            border: 2px solid rgba(255, 255, 255, 0.2); /* Subtle white border */
        }

        /* Ensure text inside the alert box is fully visible */
        div.stAlert p {
            margin: 10px 0 !important;
            line-height: 1.5 !important;
            color: white !important; /* Force white text */
        }

        /* Keep important elements in bright white */
        div.stAlert strong {
            font-size: 20px !important;
            color: white !important; /* Pure white */
        }

        /* REMOVE TRANSPARENCY ISSUES */
        div[data-testid="stNotification"] {
            background: none !important;
            box-shadow: none !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

# Apply custom CSS to fix the white space below the map
def apply_map_styles():
    st.markdown(
        """
        <style>
        /* Fix white space under the map */
        iframe[title="streamlit_folium.st_folium"] {
            height: 800px !important; /* Adjust height as needed */
            margin-bottom: 0px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )