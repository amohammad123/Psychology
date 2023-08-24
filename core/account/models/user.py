from django.db import models
from django.contrib.auth.models import AbstractUser

from conf.model import BaseModel
from conf.time import time_now


class CustomUser(AbstractUser, BaseModel):
    gender_choices = (
        ('male', 'مرد'),
        ('female', 'زن')
    )
    type_choices = (
        ('client', 'مراحع'),
        ('trappist', 'درمانگر')
    )
    username = models.CharField(verbose_name='تلفن همراه', max_length=11, unique=True)
    is_verified = models.BooleanField(verbose_name='فعال', default=False)
    nationality_code = models.IntegerField(verbose_name='کد ملی', blank=True, null=True)
    type = models.CharField(verbose_name='نوع کاربر', max_length=20, choices=type_choices)
    date_of_birth = models.BigIntegerField(verbose_name='تاریخ تولد', blank=True, null=True)
    gender = models.CharField(verbose_name='جنسیت', max_length=10, choices=gender_choices, blank=True, null=True)
    user_code = models.CharField(verbose_name='کد معرفی', max_length=20, null=True, blank=True)
    invitor_code = models.CharField(verbose_name='کد معرف', max_length=20, null=True, blank=True, editable=False)
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        db_table = 'user'

    def __str__(self):
        return self.username


class PhoneCode(BaseModel):
    phone = models.CharField(verbose_name='شماره تلفن', max_length=11)
    code = models.CharField(verbose_name='کد', max_length=6, editable=False)
    expire_date = models.BigIntegerField(verbose_name='تاریخ انقضا')
    is_active = models.BooleanField(verbose_name='فعال', default=True)

    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کدهای تایید'
        db_table = 'phone_code'

    def __str__(self):
        return f'کد تایید آموزا\n\nکد: {self.code}'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.code_generator()
        if not self.expire_date:
            self.expire_date = time_now() + (60 * 2)
        return super(PhoneCode, self).save(*args, **kwargs)

    def code_generator(self):
        import random
        return str(random.randint(100000, 999999))
