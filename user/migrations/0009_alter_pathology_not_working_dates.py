# Generated by Django 4.2.3 on 2024-04-08 16:00

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_address_alter_pathology_not_working_dates_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathology',
            name='not_working_dates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateTimeField(auto_now_add=True), default=[datetime.datetime(2024, 4, 8, 16, 0, 22, 870953)], size=None),
        ),
    ]
