

from emailrep import EmailRep
import pandas as pd
import re
import streamlit as st
emailrep = EmailRep(st.secrets['EMAIL_REP_API_KEY'])

import zipfile

def zip_files(files, zip_name="reports.zip"):
    """
    Zip multiple files into a single ZIP file.

    Parameters:
    - files: A list of file paths to be zipped.
    - zip_name: The name of the output ZIP file.
    
    Returns:
    - The path to the created ZIP file.
    """
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in files:
            # Add file to the zip file
            # The arcname argument ensures the file name in the zip file doesn't include the path
            zipf.write(file, arcname=file.split('/')[-1])
    return zip_name

def is_email_valid(email):
    # Simple regex for validating an email address
    pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    return re.match(pattern, email, re.IGNORECASE)

def lead_from_email(email) : 
    data=emailrep.query(email)
    print('mounim')
    print(data)
    

    # Data dictionary
    # Metadata dictionary
    metadata = {
        'email': 'Email address of the user',
        'reputation': 'Reputation level associated with the email',
        'suspicious': 'Whether the email is flagged as suspicious',
        'references': 'Number of references to the email',
        'details': 'Detailed information about the email',
        'blacklisted': 'Whether the email is blacklisted',
        'malicious_activity': 'Whether the email has been involved in malicious activity',
        'malicious_activity_recent': 'Whether recent malicious activity has been observed',
        'credentials_leaked': 'Whether email credentials have been leaked',
        'credentials_leaked_recent': 'Whether recent credentials leakage has been observed',
        'data_breach': 'Whether the email has been involved in a data breach',
        'first_seen': 'Date when the email was first observed',
        'last_seen': 'Date when the email was last observed',
        'domain_exists': 'Whether the domain of the email exists',
        'domain_reputation': 'Reputation level of the domain',
        'new_domain': 'Whether the domain is newly created',
        'days_since_domain_creation': 'Number of days since domain creation',
        'suspicious_tld': 'Whether the top-level domain of the email is suspicious',
        'spam': 'Whether the email is associated with spam',
        'free_provider': 'Whether the email provider is free',
        'disposable': 'Whether the email is disposable',
        'deliverable': 'Whether the email is deliverable',
        'accept_all': 'Whether the email server accepts all emails',
        'valid_mx': 'Whether the email has a valid mail exchange record',
        'primary_mx': 'Primary mail exchange server of the email',
        'spoofable': 'Whether the email is spoofable',
        'spf_strict': 'Whether SPF (Sender Policy Framework) is strictly enforced',
        'dmarc_enforced': 'Whether DMARC (Domain-based Message Authentication, Reporting, and Conformance) is enforced',
        'profiles': 'Social media profiles associated with the email'
    }

    flat_data = {**data, **data['details']}
    del flat_data['details']

    # Convert the flat dictionary to a DataFrame for the data
    df = pd.DataFrame([flat_data])

    # Save data to its own .xlsx file
    data_excel_file = 'email_data.xlsx'
    df.to_excel(data_excel_file, index=False)

    # Create a DataFrame for metadata
    metadata_df = pd.DataFrame(list(metadata.items()), columns=['Field', 'Explanation'])

    # Save metadata to its own .xlsx file
    metadata_excel_file = 'email_metadata.xlsx'
    metadata_df.to_excel(metadata_excel_file, index=False)

    print("Data has been written to", data_excel_file)
    print("Metadata has been written to", metadata_excel_file)
    return data_excel_file, metadata_excel_file


def create_download_buttons(data_file_path, metadata_file_path):
    """
    Create download buttons for the data and metadata Excel files.

    Parameters:
    - data_file_path: The file path to the email data Excel file.
    - metadata_file_path: The file path to the email metadata Excel file.
    """
    with open(data_file_path, "rb") as file:
        st.download_button(
            label="Download Email Data Report",
            data=file,
            file_name="Email Threat Detected.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with open(metadata_file_path, "rb") as file:
        st.download_button(
            label="Download Detected Threat and Leads ingested",
            data=file,
            file_name="Threats_metadata.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        

def create_download_buttons2(data_file_path, metadata_file_path):
    zip_file_name = zip_files([data_file_path, metadata_file_path])
    
    # Create a download button for the ZIP file
    with open(zip_file_name, "rb") as file:
        st.download_button(
            label="Download Reports as ZIP",
            data=file,
            file_name=zip_file_name,
            mime="application/zip"
        )
