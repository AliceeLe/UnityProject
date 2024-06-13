import os
from msal import ConfidentialClientApplication
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

client_id = 'da81afd5-3ed6-4f89-8036-812067cc4183'
client_secret = 'gdj8Q~Upi5pSnLs5E2tAV6fvxcSRHiMrMJMvIcIn'
tenant_id = '19cff0af-7bfb-4dfc-8fdc-ecd1a242439b'

authority = f'https://login.microsoftonline.com/{tenant_id}'
scope = ['https://graph.microsoft.com/.default']
token_url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(tenant_id)

app = ConfidentialClientApplication(client_id, 
                                    authority=authority, 
                                    client_credential=client_secret)
result = app.acquire_token_silent(scope, account=None)

if not result:
    result = app.acquire_token_for_client(scopes=scope)

access_token = result['access_token']

def send_email(subject, body, to_email, from_email):
    message = MIMEMultipart()
    message['to'] = to_email
    message['from'] = from_email
    message['subject'] = subject

    msg = MIMEText(body)
    message.attach(msg)

    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }

    send_mail_url = 'https://graph.microsoft.com/v1.0/me/sendMail'
    email = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': 'Text',
                'content': body
            },
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': to_email
                    }
                }
            ]
        }
    }

    response = requests.post(send_mail_url, headers=headers, json=email)
    if response.status_code == 202:
        print('Email sent successfully!')
    else:
        print('Failed to send email:', response.json())

if __name__ == '__main__':
    subject = "Test Email"
    body = "This is a test email sent from Python using OAuth2 for Outlook!"
    to_email = "lhcanh@zuelligpharma.com"
    from_email = "lhcanh@zuelligpharma.com"

    send_email(subject, body, to_email, from_email)
