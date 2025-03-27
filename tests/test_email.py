from src.settings import Settings

from email.message import EmailMessage
import smtplib

from apscheduler.schedulers.background import BackgroundScheduler

import atexit

def send_email():
    settings = Settings()

    email_message = EmailMessage()
    email_message["Subject"] = "Teste - Email Automático"
    email_message["From"] = settings.email.email_email
    email_message["To"] = ""

    email_message.set_content("Apenas um teste de email!")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(user=settings.email.email_email, password=settings.email.email_password.get_secret_value())
        smtp.send_message(email_message)

scheduler = BackgroundScheduler()
scheduler.add_job(func=send_email, trigger="cron", day_of_week="sat", hour=23, minute=59)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

while True:
    pass
