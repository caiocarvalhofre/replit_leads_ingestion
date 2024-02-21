
import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #F0F2F6;
        }
        .upload-btn, .custom-btn {
            display: block;
            margin: 10px 0px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            cursor: pointer;
            text-align: center;
            background-color: #eee;
            color: #333;
        }
        .upload-btn:hover, .custom-btn:hover {
            background-color: #ddd;
        }
        /* Additional CSS for improvements */
        .stApp {
            background-color: #EFF3F6;
            color: #333;
        }
        .stButton>button {
            border: 1px solid #4CAF50;
            color: white;
            background-color: #4CAF50;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)
