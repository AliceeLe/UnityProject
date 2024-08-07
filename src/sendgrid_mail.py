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

# Read CSV file and send emails
csv_file_path = 'data/processed/sample.csv'
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Render the template with variables from the CSV row
        html_content = template.render(row=row)
        
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

                <table width="100%" height="100%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td align="center" valign="middle">
                        <img src="data:image/png;base64,{image_png}" usemap="#image-map" alt="Email Image" />
                                                    <map name="image-map">
<map name="image-map">
    <area target="" alt="Link Sales 360" title="Link Sales 360" href="https://www.cs.cmu.edu/~akohlbre/" coords="813,93,701,17" shape="rect">
    <area target="" alt="Link Central Point" title="Link Central Point" href="https://boldaugust.com/blog/how-to-make-a-logo-white-canva" coords="953,92,817,22" shape="rect">
</map>                        </td>
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


