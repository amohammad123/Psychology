from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from account.models.profile import validate_is_not_trappist, validate_is_trappist
from conf.model import BaseModel
from rest_framework.exceptions import ValidationError


# Create your models here.

class Package(BaseModel):
    category = models.ManyToManyField('post.UserCategory', verbose_name='دسته بندی کاربر',
                                      related_name='packages')
    parent_package = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='پکیج پدر', blank=True, null=True,
                                       related_name='parents_package')
    name = models.CharField(verbose_name='نام', max_length=100)
    index = models.IntegerField(verbose_name='اولویت', blank=True, null=True)
    order = models.IntegerField(verbose_name='ترتیب', blank=True, null=True)
    summary = models.CharField(verbose_name='خلاصه', max_length=250, blank=True, null=True)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    prerequisite = models.TextField(verbose_name='پیش نیاز', blank=True, null=True)
    time = models.PositiveIntegerField(verbose_name='مدت زمان دوره', blank=True, null=True)
    views = models.PositiveIntegerField(verbose_name='تعداد بازدید کنندگان', default=0, blank=True, null=True)
    sell_count = models.PositiveIntegerField(verbose_name='تعداد فروش دوزه', default=0)
    tags = models.ManyToManyField('post.Tag', verbose_name='تگ ها', related_name='package')

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def sold(self):
        self.sell_count += 1
        self.save(update_fields=['sell_count'])

    class Meta:
        verbose_name = 'پکیج ها'
        verbose_name_plural = 'پکیج'
        db_table = 'package'

    def __str__(self):
        return f'{self.category} - {self.name}'


class PackageFile(BaseModel):
    package = models.ForeignKey(Package, verbose_name='پکیج', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(verbose_name='فایل', upload_to='package_files', blank=True, null=True)
    is_main = models.BooleanField(verbose_name='فایل اصلی', default=False)
    is_valid = models.BooleanField(verbose_name='معتبر', default=True)
    order = models.PositiveIntegerField(verbose_name='ترتیب', blank=True, null=True)

    class Meta:
        verbose_name = 'فایل های پکیج'
        verbose_name_plural = verbose_name
        db_table = 'package_file'

    def __str__(self):
        return f'{self.package} - {self.is_main} - {self.is_valid}'


class UserPackage(BaseModel):
    user = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name='packages', verbose_name='کاربر')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='user_package',
                                verbose_name='پکیج')
    is_payed = models.BooleanField(default=True, verbose_name='پرداخت شده')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'پکیج های کاربر'
        verbose_name_plural = verbose_name
        db_table = 'user_package'

    def __str__(self):
        return f'{self.user} - {self.package} - {self.is_active}'


class PackagePayment(BaseModel):
    package = models.ForeignKey(Package, verbose_name='پکیج', on_delete=models.CASCADE, related_name='payment')
    original_price = models.PositiveIntegerField(verbose_name='قیمت اصلی', blank=True, null=True)
    offer_price = models.PositiveIntegerField(verbose_name='قیمت با تخفیف', blank=True, null=True)

    def get_percent(self):
        off_price = (self.original_price - self.offer_price)
        percent = float(off_price / self.original_price) * 100
        return percent

    class Meta:
        verbose_name = 'قیمت پکیج'
        verbose_name_plural = verbose_name
        db_table = 'package_payment'

    def __str__(self):
        return self.package


class PackageRate(BaseModel):
    user = models.ForeignKey('account.Profile', on_delete=models.CASCADE, verbose_name='کاربر',
                             related_name='package_retes')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='پکیج', related_name='rates')
    comment = models.TextField(verbose_name='نظر', blank=True, null=True)
    rate = models.IntegerField(verbose_name='امتیاز', validators=[MinValueValidator(0), MaxValueValidator(5)],
                               blank=True, null=True)
    like = models.BooleanField(verbose_name='لایک', blank=True, null=True)

    class Meta:
        unique_together = ('user', 'package',)
        verbose_name = 'امتیاز پکیج'
        verbose_name_plural = verbose_name
        db_table = 'package_rate'

    def __str__(self):
        return f'{self.package} - {self.rate}'
