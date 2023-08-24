from django.db import models
from conf.model import BaseModel
from .user import CustomUser


class Client(BaseModel):
    user = models.OneToOneField(verbose_name='کاربر', to=CustomUser, on_delete=models.CASCADE, related_name='client',
                                null=True)
    first_name = models.CharField(verbose_name='نام', max_length=40)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=40)
    image = models.ImageField(verbose_name='تصویر', upload_to='user_images', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    sheba = models.CharField(verbose_name='شماره شبا', max_length=24, null=True, blank=True)
    card_number = models.CharField(verbose_name='شماره کارت', max_length=16, null=True, blank=True)
    bank_name = models.CharField(verbose_name='نام بانک', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = 'مراحع'
        verbose_name_plural = 'مراجعان'
        db_table = 'client'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Trappist(BaseModel):
    level_choices = (
        ('کارشناسی', 'bachelors'),
        ('کارشناسی ارشد', 'master'),
        ('دکترا', 'doctor')
    )
    user = models.OneToOneField(verbose_name='کاربر', to=CustomUser, on_delete=models.CASCADE, related_name='trappist',
                                null=True)
    first_name = models.CharField(verbose_name='نام', max_length=40)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=40)
    level = models.CharField(verbose_name='سطخ تحصیلات', max_length=20, choices=level_choices, blank=True, null=True)
    image = models.ImageField(verbose_name='تصویر', upload_to='user_images', null=True, blank=True)
    about_me = models.TextField(verbose_name='درباره من', blank=True, null=True)
    sheba = models.CharField(verbose_name='شماره شبا', max_length=24, null=True, blank=True)
    card_number = models.CharField(verbose_name='شماره کارت', max_length=16, null=True, blank=True)
    bank_name = models.CharField(verbose_name='نام بانک', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = 'درمانگر'
        verbose_name_plural = 'درمانگران'
        db_table = 'trappist'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
