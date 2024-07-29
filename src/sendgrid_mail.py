import os
import subprocess
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import base64

# Function to encode image to Base64
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Path to the Node.js script
node_script_path = os.path.join('src', 'convert_html_to_png.js')

# Run the Node.js script to convert HTML to PNG
subprocess.run(['node', node_script_path], check=True)

# Encode the PNG image to Base64
image_png = encode_image_to_base64('src/email.png')

# Load environment variables from .env file
load_dotenv()

# Get the SendGrid API key and email details from environment variables
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
subject = "Sales dashboard sample - Vinh"

# Create the email content with the embedded image
html_content = f"""
<html>
  <body>
    <img src="data:image/png;base64,{image_png}" alt="Email Image" />
  </body>
</html>
"""

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
    print(e)
