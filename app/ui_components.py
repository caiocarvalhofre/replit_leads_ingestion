# ui_components.py
import streamlit as st

def sidebar_navigation():
    """Handle sidebar navigation and content."""
    st.sidebar.title("Navigation")
    # About section in the sidebar
    with st.sidebar.expander("About"):
        st.write("""
            This app streamlines the lead management process for Counter-Insider Threat (C-InT) analysts by automating the ingestion, processing, and preliminary risk assessment of leads from various sources.
            It's designed to be intuitive and user-friendly, making it easier for analysts to manage leads efficiently and effectively.
        """)

    # Option selection
    upload_option = st.sidebar.radio("Choose an upload option:", 
                                     ('None', 'Enter Email Address', 'Upload Written Report (PDF)', 'Social Media Post', 'Upload Image', 'Upload Video'))
    return upload_option
