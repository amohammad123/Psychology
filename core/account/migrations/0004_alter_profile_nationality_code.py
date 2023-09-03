# Generated by Django 3.2.20 on 2023-09-03 12:14

import account.models.profile
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20230903_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nationality_code',
            field=models.IntegerField(blank=True, null=True, validators=[account.models.profile.validate_iranian_national_code], verbose_name='کد ملی'),
        ),
    ]
