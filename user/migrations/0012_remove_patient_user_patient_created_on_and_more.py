# Generated by Django 5.0.2 on 2024-04-10 17:22

import datetime
import django.contrib.postgres.fields
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_address_created_on_address_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='user',
        ),
        migrations.AddField(
            model_name='patient',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='pathology',
            name='not_working_dates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateTimeField(auto_now_add=True), default=[datetime.datetime(2024, 4, 10, 17, 22, 37, 950642)], size=None),
        ),
    ]
