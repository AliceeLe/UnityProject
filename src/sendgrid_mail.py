import os
import subprocess
import csv
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import base64
from datetime import datetime

# Function to encode image to Base64
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Load environment variables from .env file
load_dotenv()

# Get the SendGrid API key and email details from environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')

# Check if the API key is available
if not SENDGRID_API_KEY:
    raise ValueError("SendGrid API key not found in environment variables")

# Set up Jinja environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('src/email_template.html')

# Function to send email
def send_email(to_email, subject, html_content):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email}: {response.status_code}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")

country_call_rates = {
    "BN": 8.0,
    "HK": 8.0,
    "ID": 10.0,
    "KH": 10.0,
    "MY": 8.0,
    "PH": 10.0,
    "SG": 8.0,
    "TH": 10.0,
    "TW": 10.0,
    "VN": 11.0
    # Add more countries and their expected values as needed
}

# Read CSV file and send emails
csv_file_path = 'data/processed/sample.csv'
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Render the template with variables from the CSV row
        html_content = template.render(row=row, country_call_rates=country_call_rates)        
        # Write the rendered HTML to a file
        with open('src/email_final.html', 'w') as file:
            file.write(html_content)
        
        # Run the Node.js script to convert the HTML to PNG
        subprocess.run(['node', 'src/convert_html_to_png.js'], check=True)
        
        # Encode the generated PNG image to Base64
        image_png = encode_image_to_base64('src/email.png')
        
        # Create the email content with the embedded image
        email_html_content = f"""
            <html>
                <body>
                    <div style="position: relative; display: inline-block;">
                        <table width="100%" height="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">
                            <tr>
                                <td style="height: 20px;">&nbsp;</td> <!-- Spacer row with fixed height -->
                            </tr>
                            <tr>
                                <td align="center" valign="middle">
                                    <a href="https://app.powerbi.com/Redirect?action=OpenReport&appId=369b5f26-0412-45ce-9d2c-fc9f8ada85c3&reportObjectId=644b908b-822b-4c6b-b965-79d227f12678&ctid=19cff0af-7bfb-4dfc-8fdc-ecd1a242439b&reportPage=ReportSection1a5a24c959e2be1c04bc&pbi_source=appShareLink&portalSessionId=9ab5af7b-505d-4879-91ca-e788b400762d" style="font-size: 15px;">Click to Visit Central Point</a>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" valign="middle">
                                    <a href="https://app.powerbi.com/Redirect?action=OpenReport&appId=4b9f871b-24bd-4a16-861f-79f1d2ec66cb&reportObjectId=7a67aa2e-2a61-498b-8b93-b4ef2f972eeb&ctid=19cff0af-7bfb-4dfc-8fdc-ecd1a242439b&reportPage=ReportSectionb54baab67b043ae0b6bb&pbi_source=appShareLink&portalSessionId=9ab5af7b-505d-4879-91ca-e788b400762d" style="font-size: 15px;">Click to Visit Sales 360</a>
                                </td>
                            </tr>
                            <tr>
                                <td style="height: 20px;">&nbsp;</td> <!-- Spacer row with fixed height -->
                            </tr>
                            <tr>
                                <td align="center" valign="middle">
                                    <img src="data:image/png;base64,{image_png}" usemap="#image-map" alt="Email Image" />
                                </td>
                            </tr>
                        </table>
                    </div>
                </body>
            </html>
        """
        
        now = datetime.now()
        # Define the subject
        subject = f"Sales dashboard - {row['Name']} - {now.strftime('%Y/%m/%d')}"
        print("Email: " + subject)
        # Send the email
        # send_email(row['Email'], subject, email_html_content)


