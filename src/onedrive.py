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
FOLDER_PATH = "General/Unity"  

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

        if not site_id:
            print("Could not retrieve site ID. Check the site URL and path.")
        else:
            # Get the folder ID
            folder_response = requests.get(
                f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{FOLDER_PATH}",
                headers=headers
            )

            if folder_response.status_code == 404:
                print("Folder not found. Check the folder path.")
            else:
                folder_response.raise_for_status()
                folder_id = folder_response.json().get('id')

                if not folder_id:
                    print("Could not retrieve folder ID. Check the folder path.")
                else:
                    # Get the items in the folder
                    items_response = requests.get(
                        f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}/children",
                        headers=headers
                    )
                    items_response.raise_for_status()
                    items = items_response.json().get('value', [])

                    # Find the first Excel file
                    file_id = None
                    for item in items:
                        if item['name'].endswith('.xlsx') and 'file' in item:
                            file_id = item['id']
                            file_name = item['name']
                            if file_name == "Unity_Expore_June24.xlsx": break

                    if not file_id:
                        print("No Excel files found in the folder.")
                    else:
                        print(f"Found Excel file: {file_name}")

                        # Download the file content
                        file_content_response = requests.get(
                            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}/content",
                            headers=headers
                        )
                        file_content_response.raise_for_status()

                        # Read the Excel file into a pandas DataFrame
                        excel_data = pd.read_excel(io.BytesIO(file_content_response.content))
                        excel_data.to_csv("data/Unity_Explore_June24.xlsx", index=False)
                        print(f"DataFrame successfully saved")

else:
    print("No token found.")
    print(result.get("error"))
    print(result.get("error_description"))
