# Generated by Django 4.2.4 on 2023-09-17 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0005_package_user_alter_package_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='index',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='اولویت'),
        ),
    ]