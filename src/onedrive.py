import msal
import requests
import pandas as pd
import io
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# SharePoint site and folder details
SHAREPOINT_SITE = "zpssgpatientsolutions.sharepoint.com"
SHAREPOINT_SITE_PATH = "/sites/BusinessAnalytics"

# Create a confidential client application
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

# Acquire a token
result = app.acquire_token_for_client(scopes=SCOPES)

if "access_token" in result:
    access_token = result['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Get the site ID
    site_response = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_SITE}:{SHAREPOINT_SITE_PATH}",
        headers=headers
    )

    if site_response.status_code == 403:
        print("Access denied. Check the permissions granted to the application and ensure the user has access to the SharePoint site.")
    elif site_response.status_code == 404:
        print("Site not found. Check the site URL and path.")
    else:
        site_response.raise_for_status()
        site_id = site_response.json().get('id')
        print(f"Site ID: {site_id}")

        if site_id:
            # Function to list items in a specific folder
            def list_folder_items(site_id, folder_path, headers):
                if folder_path:
                    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}:/children"
                else:
                    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/children"
                print(f"Request URL: {url}")  # Debug print
                folder_response = requests.get(url, headers=headers)

                try:
                    folder_response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    print(f"HTTPError: {e}")
                    print(f"Response Content: {folder_response.content}")
                    return

                folder_items = folder_response.json().get('value', [])
                print(f"Items in folder '{folder_path}':")
                for item in folder_items:
                    print(f"Name: {item['name']}, Type: {'folder' if 'folder' in item else 'file'}")
                return folder_items

            # List items in the "General" folder
            general_items = list_folder_items(site_id, "General", headers)

            # Find and list items in the "Dataset" folder inside "General"
            if general_items:
                for item in general_items:
                    if item['name'] == "Dataset" and 'folder' in item:
                        dataset_path = "General/Dataset"
                        dataset_items = list_folder_items(site_id, dataset_path, headers)
                        break
                else:
                    print("Dataset folder not found in General.")
                    dataset_items = None

            # Find and list items in the "ezClaim" folder inside "Dataset"
            if dataset_items:
                for item in dataset_items:
                    if item['name'] == "ezClaim" and 'folder' in item:
                        ezclaim_path = "General/Dataset/ezClaim"
                        ezclaim_items = list_folder_items(site_id, ezclaim_path, headers)
                        break
                else:
                    print("ezClaim folder not found in Dataset.")
                    ezclaim_items = None

            # Find the first Excel file in the "ezClaim" folder and print its data
            if ezclaim_items:
                for item in ezclaim_items:
                    if item['name'].endswith('.xlsx') and 'file' in item:
                        file_id = item['id']
                        file_name = item['name']
                        print(f"Found Excel file: {file_name}")

                        # Download the file content
                        file_content_response = requests.get(
                            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}/content",
                            headers=headers
                        )
                        file_content_response.raise_for_status()

                        # Read the Excel file into a pandas DataFrame
                        excel_data = pd.read_excel(io.BytesIO(file_content_response.content))
                        print(excel_data)
                        break
                else:
                    print("No Excel files found in ezClaim folder.")

else:
    print("No token found.")
    print(result.get("error"))
    print(result.get("error_description"))
