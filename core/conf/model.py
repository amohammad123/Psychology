import uuid

from django.db import models

from .time import time_now


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name='شناسه')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده', blank=True, null=True)
    create_date = models.BigIntegerField(default=time_now, editable=False, verbose_name='تاریخ ایجاد')
    update_date = models.BigIntegerField(default=time_now, verbose_name='تاریخ ویرایش')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.update_date = time_now()
        return super(BaseModel, self).save(*args, **kwargs)
