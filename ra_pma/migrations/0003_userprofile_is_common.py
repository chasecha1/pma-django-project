# Generated by Django 4.2.16 on 2024-12-03 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ra_pma', '0002_userprofile_background_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_common',
            field=models.BooleanField(default=False),
        ),
    ]
