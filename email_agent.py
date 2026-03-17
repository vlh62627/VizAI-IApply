import smtplib
from email.message import EmailMessage
import os

def send_application(to_email, user_email, cover, cv):
    """
    Sends an application email immediately with a BCC to the user.
    """
    msg = EmailMessage()
    msg["Subject"] = "Application for Open Position"
    msg["From"] = user_email
    msg["To"] = to_email
    msg["Bcc"] = user_email  # User receives a blind copy for tracking

    msg.set_content(cover)

    if cv:
        # Ensure we read from the start of the file if it's a Streamlit UploadedFile
        cv.seek(0) 
        msg.add_attachment(
            cv.read(),
            maintype="application",
            subtype="octet-stream",
            filename=cv.name
        )

    # When using BCC, the SMTP send_message or sendmail needs the full list of recipients
    # including the BCC address, even though it's hidden in the headers.
    recipients = [to_email, user_email]

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            # Note: Ensure you use an App Password, not your regular password
            smtp.login(user_email, st.secrets["EMAIL_PASSWORD"]) 
            smtp.send_message(msg, to_addrs=recipients)
        
        print(f"✅ Email sent to {to_email} (BCC'd to you)")
        return True
    except Exception as e:
        print(f"❌ Failed to send to {to_email}: {e}")
        return False
