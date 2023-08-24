# Generated by Django 3.2.20 on 2023-08-24 17:21

import conf.time
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('username', models.CharField(max_length=11, unique=True, verbose_name='تلفن همراه')),
                ('is_verified', models.BooleanField(default=False, verbose_name='فعال')),
                ('nationality_code', models.IntegerField(blank=True, null=True, verbose_name='کد ملی')),
                ('type', models.CharField(choices=[('client', 'مراحع'), ('trappist', 'درمانگر')], max_length=20, verbose_name='نوع کاربر')),
                ('date_of_birth', models.BigIntegerField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('gender', models.CharField(blank=True, choices=[('male', 'مرد'), ('female', 'زن')], max_length=10, null=True, verbose_name='جنسیت')),
                ('user_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='کد معرفی')),
                ('invitor_code', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='کد معرف')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PhoneCode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('phone', models.CharField(max_length=11, verbose_name='شماره تلفن')),
                ('code', models.CharField(editable=False, max_length=6, verbose_name='کد')),
                ('expire_date', models.BigIntegerField(verbose_name='تاریخ انقضا')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={
                'verbose_name': 'کد تایید',
                'verbose_name_plural': 'کدهای تایید',
                'db_table': 'phone_code',
            },
        ),
        migrations.CreateModel(
            name='Trappist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('first_name', models.CharField(max_length=40, verbose_name='نام')),
                ('last_name', models.CharField(max_length=40, verbose_name='نام خانوادگی')),
                ('level', models.CharField(blank=True, choices=[('کارشناسی', 'bachelors'), ('کارشناسی ارشد', 'master'), ('دکترا', 'doctor')], max_length=20, null=True, verbose_name='سطخ تحصیلات')),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images', verbose_name='تصویر')),
                ('about_me', models.TextField(blank=True, null=True, verbose_name='درباره من')),
                ('sheba', models.CharField(blank=True, max_length=24, null=True, verbose_name='شماره شبا')),
                ('card_number', models.CharField(blank=True, max_length=16, null=True, verbose_name='شماره کارت')),
                ('bank_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='نام بانک')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trappist', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'درمانگر',
                'verbose_name_plural': 'درمانگران',
                'db_table': 'trappist',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('first_name', models.CharField(max_length=40, verbose_name='نام')),
                ('last_name', models.CharField(max_length=40, verbose_name='نام خانوادگی')),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images', verbose_name='تصویر')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('sheba', models.CharField(blank=True, max_length=24, null=True, verbose_name='شماره شبا')),
                ('card_number', models.CharField(blank=True, max_length=16, null=True, verbose_name='شماره کارت')),
                ('bank_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='نام بانک')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مراحع',
                'verbose_name_plural': 'مراجعان',
                'db_table': 'client',
            },
        ),
    ]