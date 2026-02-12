import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(name, email, link, date):

    sender_email = "somasekhar.tammana2004@gmail.com"
    sender_password = "oyaygvujmonipgkn"   # Use Gmail App Password

    subject = "Interview Scheduled Successfully"

    body = f"""
Hello {name},

Your interview has been scheduled successfully.

📅 Interview Date: {date}

🔗 Interview Link:
{link}

Please join on time.

Best regards,
HR Team
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        print("Error sending email:", e)
