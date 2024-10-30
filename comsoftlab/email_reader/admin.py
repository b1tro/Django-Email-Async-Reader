from django.contrib import admin
from .models import EmailMessage, EmailMessageFile, TargetEmail

@admin.register(EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ['uid', 'subject', 'email_from', 'date_sent']
    ordering = ['-uid']

@admin.register(EmailMessageFile)
class EmailMessageFileAdmin(admin.ModelAdmin):
    list_display = ['id','message']

@admin.register(TargetEmail)
class TargetEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'server']


