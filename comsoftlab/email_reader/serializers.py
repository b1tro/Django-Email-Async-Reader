from rest_framework import serializers
from .models import EmailMessage, EmailMessageFile

class EmailMessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMessageFile
        fields = ['id', 'message']


class EmailMessageSerializer(serializers.ModelSerializer):
    files = EmailMessageFileSerializer(many= True, read_only= True)
    class Meta:
        model = EmailMessage
        fields = ['uid', 'service', 'email_from', 'subject', 'text', 'date_sent', 'files']
