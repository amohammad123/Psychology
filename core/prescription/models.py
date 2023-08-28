from django.db import models

from conf.model import BaseModel


# Create your models here.

class Prescription(BaseModel):
    trappist = models.ForeignKey('account.Trappist', verbose_name='درمانگر', on_delete=models.CASCADE,
                                 related_name='prescriptions')
    client = models.ForeignKey('account.Client', verbose_name='مراجع', on_delete=models.CASCADE,
                               related_name='prescriptions')
    name = models.CharField(verbose_name='نام', max_length=50)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'نسخه ها'
        verbose_name_plural = 'نسحه'
        db_table = 'prescription'

    def __str__(self):
        return f'{self.name} - {self.trappist} - {self.client}'


class Drug(BaseModel):
    prescription = models.ForeignKey(Prescription, verbose_name='نسخه', on_delete=models.CASCADE, related_name='drugs')
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
