# Generated by Django 5.0.2 on 2024-04-13 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_order_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='date',
        ),
        migrations.AddField(
            model_name='slot',
            name='day',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30)], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slot',
            name='month',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slot',
            name='year',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
