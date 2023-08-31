from django.db import models
from django.contrib.auth.models import AbstractUser

from conf.model import BaseModel
from conf.time import time_now
from rest_framework.exceptions import ValidationError


class CustomUser(AbstractUser, BaseModel):
    gender_choices = (
        ('male', 'مرد'),
        ('female', 'زن'),
        ('unknown', 'نامشخص')
    )
    type_choices = (
        ('client', 'مراحع'),
        ('trappist', 'درمانگر')
    )
    username = models.CharField(verbose_name='تلفن همراه', max_length=11, unique=True)
    is_verified = models.BooleanField(verbose_name='فعال', default=False)
    nationality_code = models.IntegerField(verbose_name='کد ملی', blank=True, null=True)
    type = models.CharField(verbose_name='نوع کاربر', max_length=20, choices=type_choices, blank=True, null=True)
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


class PhoneCodeManage(models.Manager):
    def create_code(self, phone):
        phone_code = self.filter(phone=phone)
        if phone_code.exists():
            if phone_code.last().expire_date > time_now() and phone_code.last().is_active == True:
                raise ValidationError({'message': 'کد قبلا ارسال شده'})
            phone_code.filter(is_active=True, expire_date__lt=time_now()).update(is_active=False)
        code = self.create(phone=phone)
        return code


class PhoneCode(BaseModel):
    phone = models.CharField(verbose_name='شماره تلفن', max_length=11)
    code = models.CharField(verbose_name='کد', max_length=6, editable=False)
    expire_date = models.BigIntegerField(verbose_name='تاریخ انقضا')
    is_active = models.BooleanField(verbose_name='فعال', default=True)
    objects = PhoneCodeManage()

    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کدهای تایید'
        db_table = 'phone_code'
        ordering = ('create_date',)

    def __str__(self):
        return f'{self.phone} - {self.code} - {self.is_active}'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.code_generator()
        if not self.expire_date:
            self.expire_date = time_now() + (60 * 2)
        return super(PhoneCode, self).save(*args, **kwargs)

    def code_generator(self):
        import random
        return str(random.randint(100000, 999999))
