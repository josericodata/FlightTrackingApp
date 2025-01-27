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