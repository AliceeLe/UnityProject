import requests
import json
from msal import ConfidentialClientApplication

# Define your Azure AD app credentials
client_id = 'da81afd5-3ed6-4f89-8036-812067cc4183'
client_secret = 'gdj8Q~Upi5pSnLs5E2tAV6fvxcSRHiMrMJMvIcIn'
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
    print(result.get('error'))

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
                    "address": "lhcanh@zuelligpharma.com"
                }
            }
        ]
    }
}

# Send the email using Microsoft Graph API
graph_api_endpoint = 'https://graph.microsoft.com/v1.0/users/me/sendMail'
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

response = requests.post(graph_api_endpoint, headers=headers, data=json.dumps(email))

if response.status_code == 202:
    print("Email sent successfully.")
else:
    print("Failed to send email. Status code:", response.status_code)
