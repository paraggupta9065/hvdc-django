# Generated by Django 5.0.2 on 2024-05-30 02:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_promocode_remove_cart_promo_code_cart_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.promocode'),
        ),
    ]
