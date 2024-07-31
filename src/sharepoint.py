import msal
import requests
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
FOLDER_PATH = "General/Dataset/Unity/old"  

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

                    # List and download all CSV files
                    csv_files = [item for item in items if item['name'].endswith('.csv')]
                    if csv_files:
                        print("CSV files in the folder:")
                        for csv_file in csv_files:
                            file_name = csv_file['name']
                            file_id = csv_file['id']
                            print(file_name)

                            # Download the file content
                            file_content_response = requests.get(
                                f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}/content",
                                headers=headers
                            )
                            file_content_response.raise_for_status()

                            # Save the file to the local computer
                            with open(f"data/{file_name}", 'wb') as local_file:
                                local_file.write(file_content_response.content)
                                print(f"{file_name} successfully saved to local computer")

                    else:
                        print("No CSV files found in the folder.")

else:
    print("No token found.")
    print(result.get("error"))
    print(result.get("error_description"))
