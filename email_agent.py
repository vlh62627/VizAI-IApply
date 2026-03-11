import smtplib
from email.message import EmailMessage

def send_application(to_email, user_email, cover, cv):

    msg = EmailMessage()

    msg["Subject"] = "Application for Open Position"

    msg["From"] = user_email
    msg["To"] = to_email
    msg["Cc"] = user_email

    msg.set_content(cover)

    if cv:

        msg.add_attachment(
            cv.read(),
            maintype="application",
            subtype="octet-stream",
            filename=cv.name
        )

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:

        smtp.login(
            user_email,
            "YOUR_APP_PASSWORD"
        )

        smtp.send_message(msg)