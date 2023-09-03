# Generated by Django 3.2.20 on 2023-09-03 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_profile_nationality_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='license_umber',
            new_name='license_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='invitor_code',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_code',
        ),
        migrations.AddField(
            model_name='profile',
            name='invitor_code',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='کد معرف'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='کد معرفی'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='type',
            field=models.CharField(blank=True, choices=[('client', 'مراحع'), ('trappist', 'درمانگر')], default='client', max_length=20, null=True, verbose_name='نوع کاربر'),
        ),
    ]
