import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SCOPE = os.getenv('SCOPE')
AUTHORITY_URL = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'

def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPE
    }
    response = requests.post(AUTHORITY_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def get_datasets(access_token):
    try:
        POWER_BI_API_URL = 'https://api.powerbi.com/v1.0/myorg/datasets'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(POWER_BI_API_URL, headers=headers)
        
        # Print detailed response information for debugging
        print("Response Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Text:", response.text)
        
        if response.status_code == 401:
            print("Authorization failed. Please check your access token and API permissions.")
        
        response.raise_for_status()
        datasets = response.json()['value']
        return datasets
    except:
        print("Error here")

access_token = get_access_token()
print("Access Token:", access_token)

datasets = get_datasets(access_token)
print("Datasets:", datasets)
