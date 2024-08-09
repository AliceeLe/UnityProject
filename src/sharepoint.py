import msal
import requests
import os
from dotenv import load_dotenv
import multiprocessing
import pandas as pd

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
FOLDER_PATHS = ["General/Dataset/Unity", "General/Dataset/Unity/old"]

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
            for folder_path in FOLDER_PATHS:
                get_folder_id(site_id, headers, folder_path)

def get_folder_id(site_id, headers, folder_path):
    # Get the folder ID
    try:
        folder_response = requests.get(
            f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}",
            headers=headers
        )
        folder_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving folder ID for {folder_path}: {e}")
    else:
        folder_id = folder_response.json().get('id')
        if not folder_id:
            print(f"Could not retrieve folder ID for {folder_path}. Check the folder path.")
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
        with open(f"data/raw/{file_name}", 'wb') as local_file:
            local_file.write(file_content_response.content)
            print(f"{file_name} successfully saved to local computer")

def find_csv_files(site_id, items_folder, headers):
    # for item in items_folder:
        # if item['name'].endswith('.xlsx'):
        #     # Convert to csv
        #     xlsx_file_name = item['name']
        #     csv_file_name = xlsx_file_name.replace('.xlsx', '.csv')
        #     xlsx_file_path = os.path.join("data/raw", xlsx_file_name)
        #     csv_file_path = os.path.join("data/raw", csv_file_name)
            
        #     # Download the xlsx file
        #     save_file_to_computer(site_id, item['id'], xlsx_file_name, headers)
            
        #     # Convert xlsx to csv
        #     excel_data = pd.read_excel(xlsx_file_path)
        #     excel_data.to_csv(csv_file_path, index=False)
            
        #     # Optionally, remove the xlsx file if not needed
        #     os.remove(xlsx_file_path)

    # List and download all CSV files
    csv_files = [item for item in items_folder if item['name'].endswith('.csv') or item['name'].endswith('.xlsx')]
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
            for folder_path in FOLDER_PATHS:
                get_folder_id(site_id, headers, folder_path)


if __name__ == '__main__':
    try:
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
            # Define arguments for the get_site function
            args = [(SHAREPOINT_SITE, SHAREPOINT_SITE_PATH, headers) for _ in range(4)]  # Example arguments

            # Create a Pool of workers and use map to apply the function in parallel
            with multiprocessing.Pool(processes=4) as pool:
                pool.starmap(get_site, args)  # Use starmap for multiple arguments

            # convert country_master to csv
            excel_data = pd.read_excel("data/raw/Country_Master_202406.xlsx")
            excel_data.to_csv("data/raw/Country_Master_202406.csv", index=False)

        # run convert csv to xlsx
        else:
            print("No token found.")
            print(result.get("error"))
            print(result.get("error_description"))

    except Exception as e:
        print(f"An error occurred in main: {e}")
