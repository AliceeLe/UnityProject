import os
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the SendGrid API key from environment variable
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')

# Check if the API key is available
if not SENDGRID_API_KEY:
    raise ValueError("SendGrid API key not found in environment variables")

# Set up Jinja environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('src/email_template.html')

# Render the template with variables
subject = "Your Subject Here"
body = "This is the body of the email."

html_content = template.render(subject=subject, body=body)

# Create the email
message = Mail(
    from_email=FROM_EMAIL,
    to_emails=TO_EMAIL,
    subject=subject,
    html_content=html_content
)

# Send the email using SendGrid
try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
