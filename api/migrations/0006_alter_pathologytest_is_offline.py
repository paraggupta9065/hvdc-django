# Generated by Django 5.0.2 on 2024-03-28 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_pathologytest_regular_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathologytest',
            name='is_offline',
            field=models.BooleanField(default=False),
        ),
    ]
