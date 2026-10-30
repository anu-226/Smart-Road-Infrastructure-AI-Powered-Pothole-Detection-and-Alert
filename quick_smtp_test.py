import os, ssl, smtplib
from email.message import EmailMessage

smtp_host = os.environ.get("SMTP_HOST")
smtp_port = int(os.environ.get("SMTP_PORT", "465"))
smtp_user = os.environ.get("SMTP_USER")
smtp_pass = os.environ.get("SMTP_PASS")

if not all([smtp_host, smtp_user, smtp_pass]):
    print("Error: SMTP env vars not set. Run setx SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASS and restart terminal.")
    raise SystemExit(1)

msg = EmailMessage()
msg["Subject"] = "Pothole Detector test"
msg["From"] = smtp_user
msg["To"] = "prakyathgo43@gmail.com"
msg.set_content("This is a test email from Pothole Detector.")

ctx = ssl.create_default_context()
try:
    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=ctx) as s:
            s.login(smtp_user, smtp_pass)
            s.send_message(msg)
    else:
        with smtplib.SMTP(smtp_host, smtp_port) as s:
            s.starttls(context=ctx)
            s.login(smtp_user, smtp_pass)
            s.send_message(msg)
    print("Test email sent to prakyathgo43@gmail.com")
except Exception as e:
    print("Failed to send test email:", e)
    raise