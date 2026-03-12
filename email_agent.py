import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import pytz
import os


START_DATE_FILE = "agent_start_date.txt"


def get_start_date():

    if os.path.exists(START_DATE_FILE):
        with open(START_DATE_FILE, "r") as f:
            return datetime.fromisoformat(f.read())

    start = datetime.now()
    with open(START_DATE_FILE, "w") as f:
        f.write(start.isoformat())

    return start


def business_days_since(start_date):

    today = datetime.now()
    count = 0
    current = start_date

    while current.date() <= today.date():

        if current.weekday() < 5:  # Mon–Fri
            count += 1

        current += timedelta(days=1)

    return count


def is_allowed_time():

    tz = pytz.timezone("US/Central")
    now = datetime.now(tz)

    return now.hour == 10


def send_application(to_email, user_email, cover, cv):

    start_date = get_start_date()

    if business_days_since(start_date) > 3:
        print("❌ Email sending window expired (3 business days limit).")
        return

    if not is_allowed_time():
        print("⏰ Emails are sent only at 10 AM CST.")
        return

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

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(
            user_email,
            "YOUR_APP_PASSWORD"
        )

        smtp.send_message(msg)

    print(f"✅ Email sent to {to_email}")
