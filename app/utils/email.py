import os
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))  # Using SSL port
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your-email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-app-password")
SMTP_FROM = os.getenv("SMTP_FROM", "library@example.com")

template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(template_dir))

async def send_email(to_email: str, subject: str, template_name: str, template_data: Dict):
    template = env.get_template(f"email/{template_name}.html")
    html_content = template.render(**template_data)
    
    message = MIMEMultipart("alternative")
    message["From"] = SMTP_FROM
    message["To"] = to_email
    message["Subject"] = subject
    
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)
    
    try:
        smtp = aiosmtplib.SMTP(hostname=SMTP_HOST, port=SMTP_PORT, use_tls=True)
        await smtp.connect()
        await smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        await smtp.send_message(message)
        await smtp.quit()
        print(f"Successfully sent email to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
