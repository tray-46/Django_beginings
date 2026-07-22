from email.message import EmailMessage
import smtplib

# 1. Construct the email configuration
SMTP_SERVER = "smtp.yandex.ru"  # e.g., smtp.gmail.com or ://yahoo.com
SMTP_PORT = 456  # TLS port
SENDER_EMAIL = "atst-box@yandex.ru"
SENDER_PASSWORD = "jpysvuwvafywfeio"  # Use a secure App Password, NOT your main password
RECIPIENT_EMAIL = "atst-box@yandex.ru"

# 2. Build the message package
msg = EmailMessage()
msg["Subject"] = "Automated Test Email"
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL
msg.set_content("Hello! This email was successfully sent using a Python script.")

# 3. Securely connect to the server and transmit the mail
try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Upgrade connection to secure TLS encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
