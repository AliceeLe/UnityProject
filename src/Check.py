import os
import subprocess
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=r'T:\VTV\Apps\Unity Project\UnityProject\.env')

print(r'T:\VTV\Apps\Unity Project\UnityProject\.env')
print("Read env")
# Get the SendGrid API key and email details from environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
print(SENDGRID_API_KEY)
print(FROM_EMAIL)
print("Can read")