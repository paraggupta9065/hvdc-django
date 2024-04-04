# Generated by Django 5.0.2 on 2024-04-03 03:19

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_pathology_not_working_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathology',
            name='not_working_dates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateTimeField(auto_now_add=True), default=[datetime.datetime(2024, 4, 3, 3, 19, 37, 609172)], size=None),
        ),
    ]
