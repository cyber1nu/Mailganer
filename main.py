# coding=utf-8

import smtplib
import os

from dotenv import load_dotenv
from email.mime.text import MIMEText
from string import Template
from celery import Celery


app = Celery()

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

email_address = 'ВАШ-ЕМЕЙЛ-АДРЕС@gmail.com'  # your email address
email_password = os.getenv('EMAIL_PASSWORD')  # your password
receivers_list = ['ПОЛУЧАТЕЛЬ-1@mail.ru', 'ПОЛУЧАТЕЛЬ-2@mail.ru']  # list with e-mail addresses


your_theme = 'This is EMAIL SUBJECT'
with open(os.path.join(BASE_DIR, 'TestMailGaner\\templates\\email_templates.html'), 'r') as file:
    message = file.read()


@app.task  # decorator to delay message sending
def send_email(your_theme, message, receiver):

    send_from = email_address
    password = email_password

    server = smtplib.SMTP('smtp.gmail.com', 587)  # server address + server port
    server.starttls()

    try:
        server.login(send_from, password)
        server.sendmail(
            send_from,
            receiver,
            'Subject: {your_theme}\n{message}'.format(your_theme=your_theme, message=message))

        return 'Message was sent successfuly.'
    except Exception as exc:
        return '{exc}\nCheck your login or password'.format(exc=exc)
    finally:
        server.quit()


def main():
    for receiver in receivers_list:
        msg = Template(message).safe_substitute(user_name=receiver)  # here you can change user_name in template
        msg = MIMEText(msg, 'html')
        print(send_email(your_theme, msg, receiver))


if __name__ == '__main__':
    main()


