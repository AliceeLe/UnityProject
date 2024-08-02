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

def get_site_id(headers):
    # Get the site ID
    try:
        site_response = requests.get(
            f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_SITE}:{SHAREPOINT_SITE_PATH}",
            headers=headers
        )
        site_response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
    else:
        site_id = site_response.json().get('id')
        if not site_id:
            print("Could not retrieve site ID. Check the site URL and path.")
        else:
            get_folder_id(site_id, headers)

def get_folder_id(site_id, headers):
    # Get the folder ID
    try:
        folder_response = requests.get(
            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{FOLDER_PATH}",
            headers=headers
        )
        folder_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving folder ID: {e}")
    else:
        folder_id = folder_response.json().get('id')
        if not folder_id:
            print("Could not retrieve folder ID. Check the folder path.")
        else:
            get_folder(site_id, folder_id, headers)

def save_file_to_computer(site_id, file_id, file_name, headers):
    # Download the file content
    try:
        file_content_response = requests.get(
            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}/content",
            headers=headers
        )
        file_content_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file {file_name}: {e}")
    else:
        # Save the file to the local computer
        with open(f"test_data/{file_name}", 'wb') as local_file:
            local_file.write(file_content_response.content)
            print(f"{file_name} successfully saved to local computer")

def find_csv_files(site_id, items_folder, headers):
    # List and download all CSV files
    csv_files = [item for item in items_folder if item['name'].endswith('.csv')]
    if csv_files:
        print("CSV files in the folder:")
        for csv_file in csv_files:
            file_name = csv_file['name']
            file_id = csv_file['id']
            print(file_name)
            save_file_to_computer(site_id, file_id, file_name, headers)
    else:
        print("No CSV files found in the folder.")

def get_folder(site_id, folder_id, headers):
    # Get the items in the folder
    try:
        items_response = requests.get(
            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}/children",
            headers=headers
        )
        items_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving folder items: {e}")
    else:
        items_folder = items_response.json().get('value', [])
        find_csv_files(site_id, items_folder, headers)

def get_site(sharepoint_site, sharepoint_site_path, headers):
    # Get the site ID
    try:
        site_response = requests.get(
            f"https://graph.microsoft.com/v1.0/sites/{sharepoint_site}:{sharepoint_site_path}",
            headers=headers
        )
        site_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving site ID: {e}")
    else:
        site_id = site_response.json().get('id')
        if not site_id:
            print("Could not retrieve site ID. Check the site URL and path.")
        else:
            get_folder_id(site_id, headers)

if "access_token" in result:
    access_token = result['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    get_site(SHAREPOINT_SITE, SHAREPOINT_SITE_PATH, headers)
else:
    print("No token found.")
    print(result.get("error"))
    print(result.get("error_description"))
