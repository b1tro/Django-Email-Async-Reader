"""
Программа, которая заполняет электронную почту тестовыми сообщениями
"""

from django.core.mail import send_mail, get_connection
from django.conf import settings
from time import sleep

login = 'login'
password = 'password'
imap_server = 'imap_server'

settings.configure(
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_HOST='smtp.gmail.com',
    EMAIL_PORT=587,
    EMAIL_HOST_USER='user',
    EMAIL_HOST_PASSWORD="password",
    EMAIL_USE_TLS=True,
)

for i in range(0,1000):
    send_mail(
        from_email=settings.EMAIL_HOST_USER,
        subject = f"Test message #{i}",
        message = f"Hello! This is my test message #{i}",
        recipient_list=[settings.EMAIL_HOST_USER],
        connection=get_connection()
    )
    sleep(1)