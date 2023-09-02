from django.db import models

from conf.model import BaseModel
from account.models.profile import validate_is_not_trappist, validate_is_trappist


# Create your models here.

class Prescription(BaseModel):
    category = models.ForeignKey('post.Category', on_delete=models.CASCADE, verbose_name='دسته بندی', blank=True,
                                 null=True, related_name='prescriptions')
    trappist = models.ForeignKey('account.Profile', verbose_name='درمانگر', on_delete=models.CASCADE,
                                 related_name='trappist_prescriptions', validators=[validate_is_trappist])
    client = models.ForeignKey('account.Profile', verbose_name='مراجع', on_delete=models.CASCADE,
                               related_name='client_prescriptions', validators=[validate_is_not_trappist])
    name = models.CharField(verbose_name='نام', max_length=50)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'نسخه ها'
        verbose_name_plural = 'نسحه'
        db_table = 'prescription'

    def __str__(self):
        return f'{self.name} - {self.trappist} - {self.client}'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Medicine(BaseModel):
    prescription = models.ForeignKey(Prescription, verbose_name='نسخه', on_delete=models.CASCADE,
                                     related_name='medicines')
    name = models.CharField(verbose_name='نام', max_length=50)
    dosage = models.FloatField(verbose_name='میزان دوز مصرفی')
    count = models.IntegerField(verbose_name='تعداد')
    intake = models.TextField(verbose_name='نحوه مصرف')
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'داروها'
        verbose_name_plural = 'دارو'
        db_table = 'drug'

    def __str__(self):
        return f'{self.name} - {self.prescription}'
