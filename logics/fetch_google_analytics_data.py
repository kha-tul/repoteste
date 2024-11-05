from google.analytics.data_v1beta import BetaAnalyticsDataClient, GetMetadataRequest
from google.oauth2 import service_account
import pandas as pd
import os
from google.auth import exceptions, credentials
import streamlit as st



def initialize_ga4_client():
    try:
        # Load credentials from the service account file in Streamlit secrets
        credentials_info = {
            "type": st.secrets["google"]["type"],
            "project_id": st.secrets["google"]["project_id"],
            "private_key_id": st.secrets["google"]["private_key_id"],
            "private_key": st.secrets["google"]["private_key"],
            "client_email": st.secrets["google"]["client_email"],
            "client_id": st.secrets["google"]["client_id"],
            "auth_uri": st.secrets["google"]["auth_uri"],
            "token_uri": st.secrets["google"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"]
        }
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        
        # Initialize the GA4 client
        client = BetaAnalyticsDataClient(credentials=credentials)
        
        return client
    
    except Exception as e:
        st.write(f"Unexpected error: {e}")
        raise










# def initialize_ga4_client(key_path):
#     try:
#         # Check if the key_path is provided
#         if not key_path:
#             raise ValueError("Key path is not provided")

#         # Check if the file exists at the given key_path
#         if not os.path.exists(key_path):
#             raise FileNotFoundError(f"Service account file not found at {key_path}")
        
#         # Load credentials from the service account file
#         # credentials = credentials.Credentials.from_service_account_file(key_path)
#         credentials = service_account.Credentials.from_service_account_file(key_path)
        
#         # Initialize the GA4 client
#         client = BetaAnalyticsDataClient(credentials=credentials)
        
#         return client
    
#     except FileNotFoundError as e:
#         st.write(f"FileNotFoundError: {e}")
#         # Handle the error (e.g., logging, raising further, etc.)
#         raise
    
#     except ValueError as e:
#         st.write(f"ValueError: {e}")
#         # Handle the error (e.g., logging, raising further, etc.)
#         raise
    
#     except exceptions.GoogleAuthError as e:
#         st.write(f"GoogleAuthError: {e}")
#         # Handle the error (e.g., logging, raising further, etc.)
#         raise

#     except Exception as e:
#         st.write(f"Unexpected error: {e}")
#         # Handle the error (e.g., logging, raising further, etc.)
#         raise

# # Function to initialize the GA4 client
# def initialize_ga4_client(key_path):
#     credentials = service_account.Credentials.from_service_account_file(key_path)
#     client = BetaAnalyticsDataClient(credentials=credentials)
#     return client

# Function to get all available metrics and dimensions
def get_metadata(client, property_id):
    request = GetMetadataRequest(name=f'properties/{property_id}/metadata')
    response = client.get_metadata(request=request)
    
    dimensions = [dim.api_name for dim in response.dimensions]
    metrics = [met.api_name for met in response.metrics]
    
    return dimensions, metrics

# Function to fetch data from GA4
def fetch_data(client, property_id, selected_dimensions, selected_metrics, start_date, end_date):
    request = {
        'property': f'properties/{property_id}',
        'date_ranges': [{'start_date': start_date, 'end_date': end_date}],
        'dimensions': [{'name': dim} for dim in selected_dimensions],
        'metrics': [{'name': met} for met in selected_metrics]
    }
    response = client.run_report(request=request)
    rows = []
    for row in response.rows:
        row_data = {}
        for i, dim in enumerate(row.dimension_values):
            row_data[selected_dimensions[i]] = dim.value
        for i, met in enumerate(row.metric_values):
            row_data[selected_metrics[i]] = met.value
        rows.append(row_data)
    return pd.DataFrame(rows)

