# Generated by Django 4.2.4 on 2023-09-19 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_testrate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='question_count',
            field=models.IntegerField(default=0, verbose_name='تعداد سوالات'),
        ),
    ]
