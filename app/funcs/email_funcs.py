from flask import Flask
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from app import app
import os

def send_email_with_attachment(smtp_host, smtp_port, username, password, subject, body, recipient, attachment_path):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = subject

    # Add body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Open the file to be sent and attach it to the email
    with open(attachment_path, 'rb') as attachment_file:
        part = MIMEApplication(attachment_file.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    # Establish a secure session with the server and send the email
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(username, password)
        server.send_message(msg)

    print("Email sent successfully!")


def convert_url_to_file_path(url):
    # Extract the relative path from the URL
    parts = url.split('/static/')
    relative_path = parts[-1] if len(parts) > 1 else ''

    # Construct the file system path
    file_path = os.path.join('app', 'static', relative_path)
    return file_path
