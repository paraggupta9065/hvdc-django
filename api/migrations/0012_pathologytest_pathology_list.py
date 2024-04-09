# Generated by Django 4.2.3 on 2024-04-09 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_pathology_not_working_dates'),
        ('api', '0011_pathologypackagetest_alter_pathologypackage_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathologytest',
            name='pathology_list',
            field=models.ManyToManyField(blank=True, null=True, related_name='test_pathology_list', to='user.pathology'),
        ),
    ]
