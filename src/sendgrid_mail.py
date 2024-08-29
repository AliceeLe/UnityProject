import os
import subprocess
import csv
from jinja2 import Environment, FileSystemLoader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import base64
from datetime import datetime
import pandas as pd
import uuid  # To generate unique filenames
from concurrent.futures import ThreadPoolExecutor
import math 
import imgkit

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
}

def load_csv():
    # Paths to the CSV files
    hcp_csv = 'data/processed/hcp_processed.csv'
    general_csv = 'data/output/general.csv'
    sample_csv = 'data/output/sample.csv'
    product_csv = 'data/processed/Product_List_Unity_Processed.csv'
    customer_csv = 'data/processed/Customer_List_Unity_Processed.csv'

    # Reading the CSV files
    hcp_dataset = pd.read_csv(hcp_csv).to_dict(orient='records')
    general_dataset = pd.read_csv(general_csv).to_dict(orient='records')
    sample_dataset = pd.read_csv(sample_csv).to_dict(orient='records')
    product_dataset = pd.read_csv(product_csv).to_dict(orient='records')
    customer_dataset = pd.read_csv(customer_csv).to_dict(orient='records')

    return hcp_dataset, general_dataset, sample_dataset, product_dataset, customer_dataset

# Function to encode image to Base64
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    # print(encoded_string)
    return encoded_string

def format_to_thousands(number):
    """Converts a string, float, or integer to a string with commas as thousand separators, rounding to the nearest integer.
       If the number is NaN, returns NaN."""
    try:        
        # Check if the number is already a float or int
        if isinstance(number, (float, int)):
            rounded_number = round(number)
            return "{:,.0f}".format(rounded_number)
        # If it's a string that represents a number, including negative numbers, convert it
        elif isinstance(number, str):
            # Remove commas and check if the remaining string is a valid number
            clean_number = number.replace(',', '')
            if clean_number.replace('.', '', 1).replace('-', '', 1).isdigit():
                rounded_number = round(float(clean_number))
                return "{:,.0f}".format(rounded_number)
            else:
                return ""
        else:
            # If it's not a number or cannot be converted, return an empty string
            return ""
    except (ValueError, TypeError) as e:
        print(f"Error formatting number {number}: {e}")
        return number  # Return the original value if conversion fails

# Function to format a number as a percentage
def format_percent(number):
    """Converts a string or float representing a decimal to a percentage string, rounded to the nearest integer, with a '%' sign."""
    try:
        # Check for NaN
        if isinstance(number, float) and math.isnan(number):
            return float('nan')

        # Check if the number is already a float
        if isinstance(number, float):
            return f"{int(round(number * 100))}%"
        # If it's a string that represents a number, convert it
        elif isinstance(number, str) and number.replace('.', '', 1).isdigit():
            return f"{int(round(float(number) * 100))}%"
        else:
            # If it's not a number or cannot be converted, return an empty string
            return ""
    except (ValueError, TypeError) as e:
        print(f"Error formatting number {number}: {e}")
        return number  # Return the original value if conversion fails

def round_to_one_decimal(number):
    """Rounds a number to 1 decimal place."""
    try:
        # Check if the number is a float or an int
        if isinstance(number, (float, int)):
            return round(number, 1)
        # If it's a string that represents a number, convert it and then round
        elif isinstance(number, str) and number.replace(',', '').replace('.', '', 1).isdigit():
            return round(float(number), 1)
        else:
            # If it's not a number or cannot be converted, return the original value
            return number
    except (ValueError, TypeError) as e:
        print(f"Error rounding number {number}: {e}")
        return number  # Return the original value if conversion fails

def format_decimal_percent(number):
    """Converts a string or float representing a decimal to a percentage string, rounded to one decimal place, with a '%' sign."""
    try:
        # Check if the number is already a float
        if isinstance(number, float):
            return f"{round(number * 100, 1)}%"
        # If it's a string that represents a number, convert it
        elif isinstance(number, str) and number.replace('.', '', 1).isdigit():
            return f"{round(float(number) * 100, 1)}%"
        else:
            # If it's not a number or cannot be converted, return an empty string
            return ""
    except (ValueError, TypeError) as e:
        print(f"Error formatting number {number}: {e}")
        return number  # Return the original value if conversion fails

def round_down_to_integer(number):
    return math.floor(number)

# Load environment variables from .env file
load_dotenv(dotenv_path=r'T:\VTV\Apps\Unity Project\UnityProject\.env')

# print("Read env")
# Get the SendGrid API key and email details from environment variables
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
# print(SENDGRID_API_KEY)
# print(FROM_EMAIL)
# print("Can read")

# Check if the API key is available
if not SENDGRID_API_KEY:
    print("No key")
    raise ValueError("SendGrid API key not found in environment variables")

# print("Yes key")

# Set up Jinja environment
env = Environment(loader=FileSystemLoader('.'))
# print(env)

# Register custom filters with the Jinja2 environment
env.filters['format_thousands'] = format_to_thousands
env.filters['format_percent'] = format_percent
env.filters['format_one_decimal'] = round_to_one_decimal
env.filters['format_decimal_percent'] = format_decimal_percent
env.filters['format_integer'] = round_down_to_integer

template = env.get_template('src/email_template.html')
template_flm = env.get_template('src/email_template_flm.html')

# print(template)

# Function to send email
def send_email(to_email, subject, html_content):
    # print("Send_email")
    # print(FROM_EMAIL)
    # print(to_email)
    # print(subject)
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    # print("Functioning")
    try:
        # print("Try")
        print(SENDGRID_API_KEY)
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        print(sg)
        response = sg.send(message)
        print(response.status_code)
        if response.status_code == 202:
            print(f"Email successfully sent to {to_email}.")
        else:
            print(f"Failed to send email to {to_email}. Status code: {response.status_code}")
            print(f"Response body: {response.body}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")

def process_email(row):
    # print(row)
    hcp_dataset, general_dataset, sample_dataset, product_dataset, customer_dataset = load_csv()
    name = row['Owner_Name']
    user_key = row['UserKey_4Map']

    # print(name, user_key)
    # print("Wait 5s")
    # print(row['Owner_Email'])
    # print("Wait 5s")

    hcp_filtered = [d for d in hcp_dataset if d['Owner_Name'] == name]
    product_filtered  = [d for d in product_dataset if d['UserKey_4Map'] == user_key]
    customer_filtered  = [d for d in customer_dataset if d['UserKey_4Map'] == user_key]

    # Limit the number of rows to 50 and 4
    hcp_filtered = hcp_filtered[:50]
    product_filtered = product_filtered[:4]
    customer_filtered = customer_filtered[:20]

    # Generate a unique identifier for this thread/process
    unique_id = uuid.uuid4().hex

    print(unique_id)

    html_filename = f'src/email_final_{unique_id}.html'
    png_filename = f'src/email_{unique_id}.png'
    # Render the template with variables from the CSV row and additional data
    html_content = template.render(row=row, country_call_rates=country_call_rates, hcp_filtered=hcp_filtered, product_filtered=product_filtered,customer_filtered=customer_filtered)        

    print(html_content[:10])
    # Write the rendered HTML to a unique file in the src/ directory
    with open(html_filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    # Run the Node.js script to convert the HTML to PNG
    # imgkit.from_string(html_content, png_filename)
    subprocess.run(['node', 'src/convert_html_to_png.js', html_filename, png_filename], check=True)
    
    # Encode the generated PNG image to Base64
    image_png = encode_image_to_base64(png_filename)

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
    subject = f"Unity - Rep: {row['Owner_Name']} - {now.strftime('%Y/%m/%d')}"
    print("Email: " + subject)
    # Send the email
    # send_email(row['Email'], subject, email_html_content)
    send_email(row['Owner_Email'], subject, email_html_content)
    print("OMG no")
    # Clean up files if necessary
    # os.remove(html_filename)
    # os.remove(png_filename)

def process_email_flm(row):
    hcp_dataset, general_dataset, sample_dataset, product_dataset, customer_dataset = load_csv()
    manager_id = row['Manager_Id']

    hcp_filtered = [d for d in hcp_dataset if d['Manager_Id'] == manager_id]
    product_filtered  = [d for d in product_dataset if d['Manager_Id'] == manager_id]
    customer_filtered  = [d for d in customer_dataset if d['Manager_Id'] == manager_id]

    # Limit the number of rows to 50 and 4
    hcp_filtered = hcp_filtered[:50]
    product_filtered = product_filtered[:4]
    customer_filtered = customer_filtered[:20]

    # Generate a unique identifier for this thread/process
    unique_id = uuid.uuid4().hex
    html_filename = f'src/email_final_{unique_id}.html'
    png_filename = f'src/email_{unique_id}.png'
    # Render the template with variables from the CSV row and additional data
    html_content = template_flm.render(row=row, country_call_rates=country_call_rates, hcp_filtered=hcp_filtered, product_filtered=product_filtered,customer_filtered=customer_filtered)        

    # Write the rendered HTML to a unique file in the src/ directory
    with open(html_filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    # Run the Node.js script to convert the HTML to PNG
    subprocess.run(['node', 'T:\\VTV\\Apps\\Unity Project\\UnityProject\\src\\convert_html_to_png.js', html_filename, png_filename], check=True)

    # Encode the generated PNG image to Base64
    image_png = encode_image_to_base64(png_filename)
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
    subject = f"Unity - FLM: {row['Owner_Name']} - {now.strftime('%Y/%m/%d')}"
    print("Email: " + subject)
    # Send the email
    send_email(row['Email'], subject, email_html_content)
    
    # Clean up files if necessary
    # os.remove(html_filename)
    # os.remove(png_filename)


# Run the process in parallel
def final_send():
    hcp_dataset, general_dataset, sample_dataset, product_dataset, customer_dataset = load_csv()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_email, general_dataset)

def final_send_test():
    hcp_dataset, general_dataset, sample_dataset, product_dataset, customer_dataset = load_csv()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_email, sample_dataset)

final_send_test()
