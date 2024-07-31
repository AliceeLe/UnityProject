import requests
import json
from msal import ConfidentialClientApplication

# Define your Azure AD app credentials
client_id = 'b5adbe1f-c2cd-4c97-80ce-a27fbe7474b8'
client_secret = 'pfC8Q~au.u1m3fD6yT_f_j_Lwe_ffzPsgtXxMdzi'
tenant_id = '19cff0af-7bfb-4dfc-8fdc-ecd1a242439b'

# Define the scopes for the Microsoft Graph API
scopes = ['https://graph.microsoft.com/.default']

# Create a ConfidentialClientApplication instance
app = ConfidentialClientApplication(client_id, client_secret, authority=f'https://login.microsoftonline.com/{tenant_id}')

# Acquire a token using client credentials flow
result = app.acquire_token_for_client(scopes=scopes)

if 'access_token' in result:
    access_token = result['access_token']
    print("Token Acquired Successfully")
else:
    print(result)
    exit()

recipients = ["lhcanh@zuelligpharma.com", "vtvinh@zuelligpharma.com"]

# Define the email message
for recipient in recipients:
    # Define the email message
    email = {
        "message": {
            "subject": "Test Email",
            "body": {
                "contentType": "Text",
                "content": "This is a test email sent from Python using Microsoft Graph API."
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient
                    }
                }
            ]
        }
    }

# Send the email using Microsoft Graph API
    user_id = 'zptunity@zuelligpharma.com'  # Replace with the actual user ID or email address
    graph_api_endpoint = f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    response = requests.post(graph_api_endpoint, headers=headers, json=email)

    try:
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        # Attempt to parse the JSON response
        try:
            response_json = response.json()
            print(f"Email sent successfully to {recipient}.")
            print(response_json)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON response for recipient {recipient}. Response content: {response.text}")
    except requests.exceptions.HTTPError as err:
        print(f"Failed to send email to {recipient}. Status code:", response.status_code)
        print("Error details:", response.text)
