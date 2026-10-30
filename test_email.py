import os
import smtplib
import ssl
from email.message import EmailMessage

def test_smtp():
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "465"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    
    print(f"Testing connection to {smtp_host}:{smtp_port}")
    print(f"Using account: {smtp_user}")
    
    msg = EmailMessage()
    msg["Subject"] = "Test Email"
    msg["From"] = smtp_user
    msg["To"] = "prakyathgo43@gmail.com"
    msg.set_content("Test email from Pothole Detector")
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    test_smtp()