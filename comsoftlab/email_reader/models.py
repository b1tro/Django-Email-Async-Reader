from django.db import models
from django.urls import reverse

SERVICE_CHOICES = (
    ('GM', 'Gmail'),
    ("YA", 'Yandex'),
    ('MA', 'Mail')
)
class EmailMessage(models.Model):
    uid = models.PositiveIntegerField()
    service = models.CharField(max_length=3, choices=SERVICE_CHOICES)
    email_from = models.EmailField()
    subject = models.CharField(max_length=255)
    text = models.TextField()
    date_sent = models.DateTimeField()
    date_received = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('uid', 'service'),)

    def __str__(self):
        return f"#{self.service}-{self.uid}. {self.subject} from {self.email_from}"


class EmailMessageFile(models.Model):
    message = models.ForeignKey(EmailMessage, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='attachments/%Y/%m/%d')

    def __str__(self):
        return f"{self.file} for {self.message}"

    def get_absolute_uri(self):
        return reverse('download', kwargs={"service": self.message.service,
                                           "message": self.message.uid,
                                           "file_id": self.id})

SERVER_CHOICES = (
        ('imap.gmail.com', 'Gmail'),
        ('imap.yandex.ru', 'Yandex'),
        ('imap.mail.ru', 'Mail'),
    )

class TargetEmail(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=30)
    server = models.CharField(max_length=20, choices=SERVER_CHOICES)