# Generated by Django 5.0.2 on 2024-03-24 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_notification_invited_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='invited_by',
            new_name='user',
        ),
    ]
