# Generated by Django 3.2.20 on 2023-08-27 10:58

import conf.time
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('name', models.CharField(max_length=100, verbose_name='نام')),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images', verbose_name='تصویر')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('color', models.TextField(blank=True, null=True, verbose_name='رنگ')),
                ('index', models.IntegerField(default=0, verbose_name='مرتب سازی بر اساس عدد - هرچه کوچکتر مقدم تر')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.category', verbose_name='دسته بندی پدر')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='نام')),
                ('slug', models.SlugField(blank=True, default='no-slug', max_length=60, null=True, verbose_name='اسلاگ')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ ها',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='UserCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('is_valid', models.BooleanField(default=False, verbose_name='فعال')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.category', verbose_name='دسته بندی')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.choiceuser', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'دسته بندی کاربر',
                'verbose_name_plural': 'دسته بندی کاربر',
                'db_table': 'user_category',
            },
        ),
        migrations.CreateModel(
            name='TrappistCategoryPrice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('price', models.BigIntegerField(verbose_name='قیمت')),
                ('is_valid', models.BooleanField(default=False, verbose_name='فعال')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.category', verbose_name='دسته بندی')),
                ('trappist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.trappist', verbose_name='درمانگر')),
            ],
            options={
                'verbose_name': 'قیمت تخصص درمانگر',
                'verbose_name_plural': 'قیمت تخصص درمانگر',
                'db_table': 'trappist_category_price',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images', verbose_name='تصویر')),
                ('body', models.TextField(blank=True, null=True, verbose_name='محتوا')),
                ('published_date', models.BigIntegerField(blank=True, null=True, verbose_name='رمان انتشار')),
                ('status', models.CharField(blank=True, choices=[('draft', 'پیش نویس'), ('published', 'منتشر شده')], max_length=20, null=True, verbose_name='وضعیت')),
                ('comment_status', models.CharField(blank=True, choices=[('open', 'باز'), ('closure', 'بسته')], max_length=20, null=True, verbose_name='وضعیت کامنت')),
                ('views', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='تعداد بازدید کنندگان')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.choiceuser', verbose_name='کاربر')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.category', verbose_name='دسته بندی')),
                ('tags', models.ManyToManyField(to='post.Tag', verbose_name='تگ ها')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست ها',
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='شناسه')),
                ('is_deleted', models.BooleanField(blank=True, default=False, null=True, verbose_name='حذف شده')),
                ('create_date', models.BigIntegerField(default=conf.time.time_now, editable=False, verbose_name='تاریخ ایجاد')),
                ('update_date', models.BigIntegerField(default=conf.time.time_now, verbose_name='تاریخ ویرایش')),
                ('body', models.TextField(max_length=300, verbose_name='محتوا')),
                ('is_enable', models.BooleanField(default=False, verbose_name='فعال')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.comment', verbose_name='کامنت پدر')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='post.post', verbose_name='پست')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.choiceuser', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
                'db_table': 'comment',
            },
        ),
    ]
