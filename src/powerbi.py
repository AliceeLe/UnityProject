import requests
from msal import ConfidentialClientApplication
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
tenant_id = os.getenv('TENANT_ID')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
scope = os.getenv('SCOPE')
authority = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'


def get_access_token():
    try:
        app = ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
        token_response = app.acquire_token_for_client(scopes=scope)
        if 'access_token' in token_response:
            return token_response['access_token']
        else:
            raise ValueError("Failed to acquire access token: " + str(token_response.get("error_description", "Unknown error")))
    except ValueError as ve:
        print(f"ValueError get_access_token: {ve}")
        raise
    except ClientApplicationError as cae:
        print(f"ClientApplicationError get_access_token: {cae}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while acquiring the access token: {e}")
        raise

def get_reports(workspace_id, access_token):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        reports = response.json()

        return reports['value']
    except requests.exceptions.RequestException as re:
        print(f"RequestException get_reports: {re}")
        raise
    except ValueError as ve:
        print(f"ValueError get_reports: {ve}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while fetching the reports: {e}")
        raise

def main():
    try:
        access_token = get_access_token()
        workspace_id = '6477fb4e-5d49-4bcc-9a94-8029845ed541'  # Your workspace ID
        reports = get_reports(workspace_id, access_token)

        for report in reports:
            print(f"Report ID: {report['id']}, Report Name: {report['name']}")
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()

