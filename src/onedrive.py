import msal
import requests
import os
import requests
from dotenv import load_dotenv

# Replace these with your actual client ID, client secret, and tenant ID
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Microsoft Graph API endpoint
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# Initialize the MSAL confidential client application
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

    # Replace with the path to your OneDrive file
    file_path = '/path/to/your/file.txt'
    graph_endpoint = f'https://graph.microsoft.com/v1.0/me/drive/root:{file_path}:/content'

    # Make a request to download the file
    response = requests.get(graph_endpoint, headers=headers)

    if response.status_code == 200:
        # Save the content to a local file
        with open('downloaded_file.txt', 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file: {response.status_code}")
        print(response.json())
else:
    print("Failed to acquire token.")
    print(result.get("error"))
    print(result.get("error_description"))
