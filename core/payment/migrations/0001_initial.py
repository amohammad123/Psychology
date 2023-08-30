# Generated by Django 3.2.20 on 2023-08-27 11:39

import conf.time
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OffCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('code', models.CharField(max_length=50, verbose_name='کد')),
                ('limit', models.IntegerField(default=0, verbose_name='محدودیت')),
                ('usage', models.IntegerField(default=0, verbose_name='استفاده شده')),
                ('expire_date', models.BigIntegerField(blank=True, null=True, verbose_name='تاریخ انقضا')),
                ('type', models.CharField(blank=True, max_length=50, null=True, verbose_name='نوع')),
                ('amount', models.IntegerField(default=0, verbose_name='مقدار')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.test', verbose_name='تست')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.choiceuser', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کد تخفیف',
                'verbose_name_plural': 'کدهای تخفیف',
                'db_table': 'off_code',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('is_payed', models.BooleanField(default=False, verbose_name='پرداخت شده')),
                ('tracking_code', models.CharField(max_length=50, verbose_name='کد پیگیری')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('off_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.offcode', verbose_name='کد تخفیف')),
                ('test_payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.testpayment', verbose_name='پرداخت تست')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.choiceuser', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تراکنش',
                'verbose_name_plural': 'تراکنش ها',
                'db_table': 'transaction',
            },
        ),
    ]