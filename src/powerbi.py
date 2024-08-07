import requests
from msal import ConfidentialClientApplication
import os
import requests
from dotenv import load_dotenv
import json 
import base64
# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
tenant_id = os.getenv('TENANT_ID')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
scope = os.getenv('SCOPE')
authority = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    response = requests.post(authority, headers=headers, data=data)
    response.raise_for_status()
    print(response.json())
    return response.json()['access_token']

def get_datasets(workspace_id, access_token):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/datasets"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        datasets = response.json()

        return datasets['value']
    except requests.exceptions.RequestException as re:
        print(f"RequestException get_datasets: {re}")
        print("Response content:", re.response.content)
        raise
    except ValueError as ve:
        print(f"ValueError get_datasets: {ve}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while fetching the datasets: {e}")
        raise

def main():
    try:
        access_token = get_access_token()
        print(f"Access Token: {access_token}")

        # Debugging: Decode the token to inspect its contents
        token_parts = access_token.split('.')
        token_header = json.loads(base64.urlsafe_b64decode(token_parts[0] + '=='))
        token_payload = json.loads(base64.urlsafe_b64decode(token_parts[1] + '=='))
        print("Token Header:", json.dumps(token_header, indent=2))
        print("Token Payload:", json.dumps(token_payload, indent=2))

        workspace_id = '6477fb4e-5d49-4bcc-9a94-8029845ed541'  # Your workspace ID
        datasets = get_datasets(workspace_id, access_token)

        for dataset in datasets:
            print(f"Dataset ID: {dataset['id']}, Dataset Name: {dataset['name']}")
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()
