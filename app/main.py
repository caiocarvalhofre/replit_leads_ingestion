import streamlit as st
from PIL import Image
import streamlit as st
# Assuming you have the following imports as well
from email_handler import is_email_valid, lead_from_email  # Adjust according to your actual import paths
from email_handler import create_download_buttons
from email_handler import create_download_buttons2
from ui_components import sidebar_navigation
from style import load_custom_css
from written_reports import process_text_openai_llm , pdf_to_text_ocr

API_KEY = st.secrets['OPENAI_API_KEY']
categories = """
Violence and Hate: Prohibited are plans or encouragement of violence, expressions of hate, or discrimination. Allowed are discussions on violence, discrimination, and historical events.
Sexual Content: Prohibited are sexually explicit conversations and encouragement of sexual activities. Allowed are discussions on sexuality, sexual education, and sexual health.
Criminal Planning: Prohibited are assistance or encouragement in criminal activities. Allowed are explanations of crimes without providing a roadmap for criminal actions.
Guns and Illegal Weapons: Prohibited are assistance or encouragement in crimes related to firearms or illegal weapons. Allowed are discussions on firearms and ownership debates.
Regulated or Controlled Substances: Prohibited are trafficking, consumption, or creation of illegal substances. Allowed are discussions on the effects and general information of such substances.
Self-Harm: Prohibited are encouragement, romanticization, or detailed methods of self-harm or suicide. Required are directions towards appropriate health resources for those expressing desires to harm themselves.
"""

def main():
    load_custom_css()
    
    st.title("Lead Ingestion and Risk Assessment App")

    # Sidebar
    st.sidebar.title("Navigation")

    # About section in the sidebar
    upload_option = sidebar_navigation()
    # Implement the rest of your app logic here
    # Handle the selected option
    if upload_option == 'Enter Email Address':
        email_address = st.sidebar.text_input("Enter your email address")

        if st.sidebar.button("Analyze Email"):
            if is_email_valid(email_address):
                # Process the email and get file paths for the reports
                data_file, metadata_file = lead_from_email(email_address)

                # Display success message
                st.sidebar.success("Email analyzed successfully. Download the reports below.")

                # Call to create download buttons for the generated Excel files
                create_download_buttons2(data_file, metadata_file)
            else:
                st.sidebar.error("Please enter a valid email address.")

    
    # Reset option
    if st.sidebar.button('Reset Selection'):
        # This resets the selected option to 'None'
        st.session_state.upload_option = 'None'
    
    # Conditional display based on selection
    if upload_option == 'Upload Written Report (PDF)':
        pdf_file = st.sidebar.file_uploader("Upload PDF", type=['pdf'])
        if pdf_file:
            st.success("PDF uploaded successfully!")
            text = pdf_to_text_ocr(pdf_file)
            response=process_text_openai_llm(api_key=API_KEY,extracted_text=text,categories=categories)
            # PDF processing logic here
            st.text_area("Response", response, height=300)
            
    elif upload_option == 'Social Media Post':
        social_media_post = st.sidebar.text_area("Paste your social media post", height=100)
        if social_media_post:
            st.success("Social media post captured!")
            # Social media post processing logic here
            
    elif upload_option == 'Upload Image':
        image_file = st.sidebar.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
        if image_file:
            image = Image.open(image_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.success("Image uploaded successfully!")
            # Image processing logic here
            
    elif upload_option == 'Upload Video':
        video_file = st.sidebar.file_uploader("Upload Video", type=['mp4', 'mov', 'avi', 'mpeg'])
        if video_file:
            file_details = {"FileName": video_file.name, "FileType": video_file.type, "FileSize": video_file.size}
            st.write(file_details)
            st.success("Video uploaded successfully!")
            # Video processing logic here

    # Ensure that the upload_option is stored in session state for reset functionality
    if upload_option != 'None':
        st.session_state.upload_option = upload_option

    # Analyze Risk and Generate Report buttons remain the same

if __name__ == "__main__":
    main()
