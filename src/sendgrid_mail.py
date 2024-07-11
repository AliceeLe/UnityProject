import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')

def load_email_template(html_file, css_file):
    with open(html_file, 'r') as html_f:
        html_content = html_f.read()
    
    with open(css_file, 'r') as css_f:
        css_content = css_f.read()
    
    # Inline CSS into HTML
    html_content = html_content.replace('{{styles}}', css_content)
    return html_content

def send_email(subject, html_content):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject=subject,
        html_content=html_content
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent successfully!")
        print(f"Status Code: {response.status_code}")
        print(f"Body: {response.body}")
        print(f"Headers: {response.headers}")
    except Exception as e:
        print("Error sending email:", e)

# Example usage
subject = "Test Email from SendGrid"
html_content = load_email_template('src/content.html', 'src/styles.css')

send_email(subject, html_content)
