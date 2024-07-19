import msal
import requests
import os
import requests
from dotenv import load_dotenv

# Replace these with your actual client ID, client secret, and tenant ID
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

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
    
    # Get the sharing token from the shared folder link
    sharing_link_response = requests.post(
        'https://graph.microsoft.com/v1.0/shares',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'grant': 'anonymous', 'scope': 'anonymous', 'type': 'view'}
    )
    
    sharing_link = sharing_link_response.json().get('id')
    
    if not sharing_link:
        print("Failed to get sharing link")
        exit(1)
    
    # Get the shared folder ID
    shared_folder_id_response = requests.get(
        f'https://graph.microsoft.com/v1.0/shares/{sharing_link}/root',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    shared_folder_id = shared_folder_id_response.json().get('id')
    
    if not shared_folder_id:
        print("Failed to get shared folder ID")
        exit(1)
    
    # Get the items in the shared folder
    shared_folder_items_response = requests.get(
        f'https://graph.microsoft.com/v1.0/me/drive/items/{shared_folder_id}/children',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    items = shared_folder_items_response.json().get('value', [])
    
    for item in items:
        print(f'Found item: {item["name"]}')
        
    # Assuming you know the name of the file you want to access
    file_name = 'your_file.xlsx'
    file_id = None
    for item in items:
        if item['name'] == file_name:
            file_id = item['id']
            break
    
    if not file_id:
        print(f"File '{file_name}' not found in the shared folder.")
        exit(1)
    
    # Download the file content
    file_content_response = requests.get(
        f'https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    # Save the file to disk
    with open(file_name, 'wb') as file:
        file.write(file_content_response.content)
    
    print(f"File '{file_name}' has been downloaded successfully.")
else:
    print("No token found.")
    print(result.get("error"))
    print(result.get("error_description"))
