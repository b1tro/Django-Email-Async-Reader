# Generated by Django 4.2.16 on 2024-10-29 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_reader', '0002_alter_emailmessage_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='uid',
            field=models.PositiveIntegerField(),
        ),
    ]
