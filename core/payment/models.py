from django.db import models
from django.conf import settings

from conf.model import BaseModel
from conf.time import time_now


# Create your models here.


# Create your models here.
class Transaction(BaseModel):
    user = models.ForeignKey('account.ChoiceUser', on_delete=models.CASCADE,
                             verbose_name='کاربر', related_name='transactions')
    test_payment = models.ForeignKey('exam.TestPayment', on_delete=models.CASCADE,
                                     verbose_name='تست', blank=True, null=True, related_name='transactions')
    package_payment = models.ForeignKey('package.PackagePayment', on_delete=models.CASCADE, verbose_name='پکیج', blank=True, null=True, related_name='transactions')
    off_code = models.ForeignKey('payment.OffCode', on_delete=models.CASCADE,
                                 verbose_name='کد تخفیف', null=True, blank=True, related_name='transaction')
    is_payed = models.BooleanField(verbose_name='پرداخت شده', default=False)
    tracking_code = models.CharField(max_length=50, verbose_name='کد پیگیری')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش ها'
        db_table = 'transaction'

    def __str__(self):
        return self.user_type + ' - ' + self.client


class OffCode(BaseModel):
    user = models.ForeignKey('account.ChoiceUser', on_delete=models.CASCADE,
                             verbose_name='کاربر', related_name='off_codes')
    test = models.ForeignKey('exam.Test', verbose_name='تست', on_delete=models.CASCADE, blank=True, null=True,
                             related_name='off_codes')
    package = models.ForeignKey('package.Package', verbose_name='پکیج', on_delete=models.CASCADE, blank=True, null=True,
                                related_name='off_code')
    code = models.CharField(max_length=50, verbose_name='کد')
    limit = models.IntegerField(verbose_name='محدودیت', default=0)
    usage = models.IntegerField(verbose_name='استفاده شده', default=0)
    expire_date = models.BigIntegerField(verbose_name='تاریخ انقضا', blank=True, null=True)
    type = models.CharField(max_length=50, verbose_name='نوع', blank=True, null=True)
    amount = models.IntegerField(verbose_name='مقدار', default=0)

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'
        db_table = 'off_code'

    def __str__(self):
        return self.user_type

    def is_valid(self, user, test, package):
        if self.expire_date < time_now():
            return False
        if self.usage >= self.limit:
            return False
        if self.user != user and self.user is not None:
            return False
        if test is not None and self.test is not None and self.test != test:
            return False
        if package is not None and self.package is not None and self.package != package:
            return False
        return True
