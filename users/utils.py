from datetime import datetime, time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from email import encoders
from email.mime.base import MIMEBase

def check_password(password):
    return True if len(password) >= 6 else False


def convert_str_to_time(time_str):
    try:
        parsed_time = datetime.strptime(time_str, '%H:%M:%S.%f').time()
    except ValueError:
        parsed_time = datetime.strptime(time_str, '%H:%M:%S').time()
    return time(parsed_time.hour, parsed_time.minute)


def send_email_via_outlook(subject, body, to_email, attachments=None):
    """
    Send an email via Outlook SMTP server.
    
    :param subject: Subject of the email
    :param body: Body of the email
    :param to_email: Recipient's email address
    :param from_email: Sender's email address
    :param password: Sender's email password
    """
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    from_email = os.getenv("OFFICE_OUTLOOK_EMAIL_ID")  # Use your default from email
    password = os.getenv("OFFICE_OUTLOOK_EMAIL_ID_PASSWORD")
    # Create the email message
    message = MIMEMultipart()
    message['From'] = from_email  # Even if this is a placeholder, SMTP servers typically require a valid email.
    message['To'] = to_email
    message['Subject'] = subject
    

    # Attach the body to the email
    message.attach(MIMEText(body, 'plain'))
    
    if attachments:
        for file_path in attachments:
            if os.path.isfile(file_path):
                # Create a MIMEBase object to attach the file
                attachment = MIMEBase('application', 'octet-stream')
                with open(file_path, 'rb') as file:
                    attachment.set_payload(file.read())
                
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                message.attach(attachment)
            else:
                print(f'File not found: {file_path}')

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(from_email, password)  # Log in to the server
            server.send_message(message)  # Send the email
        print(f'Email sent successfully to {to_email}')
        return True
    except Exception as e:
        print(f'Error sending email: {e}')
        return False
    
    
from datetime import timedelta

# Example timedelta object
def convert_time_str(delta):
    # delta = timedelta(seconds=26488)

    # Convert timedelta to total seconds
    total_seconds = int(delta.total_seconds())

    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the result
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    return formatted_time