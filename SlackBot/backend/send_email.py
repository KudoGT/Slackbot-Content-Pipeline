import os
import requests
from dotenv import load_dotenv

load_dotenv()

MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")

def send_email(to_email, subject, text, pdf_path):
    """
    Send a PDF email via Mailgun.

    Args:
        to_email (str): Recipient email.
        subject (str): Email subject.
        text (str): Email body.
        pdf_path (str): Path to the PDF file to attach.
    """
    if not os.path.exists(pdf_path):
        return f"PDF file not found at {pdf_path}"

    with open(pdf_path, "rb") as pdf_file:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            files={"attachment": pdf_file},
            data={
                "from": f"SlackBot <postmaster@{MAILGUN_DOMAIN}>",
                "to": to_email,
                "subject": subject,
                "text": text
            }
        )

    if response.status_code == 200:
        return f"Email sent successfully to {to_email}"
    else:
        return f"Failed to send email: {response.status_code} {response.text}"
