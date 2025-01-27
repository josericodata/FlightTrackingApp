import os
import streamlit as st

def set_background_image(image_path):
    """
    Sets a background image for the Streamlit app.

    :param image_path: Path to the background image file.
    """
    import base64
    import streamlit as st

    if os.path.exists(image_path):
        # Read and encode the image to Base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()

        # Apply the background styling
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error(f"Error: The image at {image_path} was not found.")

def apply_global_styles():
    st.markdown(
        """
        <style>

        /* Set the top horizontal bar (header) to black */
        [data-testid="stHeader"] {
            background-color: #f1e4f5 !important;  /* Black background */
            border-bottom: 2px solid #f1e4f5 !important;  /* Black border for seamless look */
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