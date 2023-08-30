from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from conf.model import BaseModel, validate_is_not_trappist, validate_is_trappist
from .user import CustomUser


# class Client(BaseModel):
#     user = models.OneToOneField(verbose_name='کاربر', to=CustomUser, on_delete=models.CASCADE, related_name='client',
#                                 null=True)
#     first_name = models.CharField(verbose_name='نام', max_length=40)
#     last_name = models.CharField(verbose_name='نام خانوادگی', max_length=40)
#     image = models.ImageField(verbose_name='تصویر', upload_to='client_images', null=True, blank=True)
#     description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
#     sheba = models.CharField(verbose_name='شماره شبا', max_length=24, null=True, blank=True)
#     card_number = models.CharField(verbose_name='شماره کارت', max_length=16, null=True, blank=True)
#     bank_name = models.CharField(verbose_name='نام بانک', max_length=64, null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'مراحع'
#         verbose_name_plural = 'مراجعان'
#         db_table = 'client'
#
#     def get_full_name(self):
#         return f'{self.first_name} {self.last_name}'
#
#     def __str__(self):
#         return self.get_full_name()


class Profile(BaseModel):
    level_choices = (
        ('bachelors', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('doctor', 'دکترا')
    )
    user = models.OneToOneField(verbose_name='کاربر', to=CustomUser, on_delete=models.CASCADE, related_name='profile',
                                null=True)
    is_trappist = models.BooleanField(verbose_name='درمانگر', default=False)
    first_name = models.CharField(verbose_name='نام', max_length=40)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=40)
    specialized_field = models.CharField(verbose_name='رشته تخصصی', max_length=50, blank=True, null=True)
    system_code = models.IntegerField(verbose_name='کد نظام', blank=True, null=True)
    level = models.CharField(verbose_name='سطخ تحصیلات', max_length=20, choices=level_choices, blank=True, null=True)
    image = models.ImageField(verbose_name='تصویر', upload_to='profile_images', null=True, blank=True)
    file = models.FileField(verbose_name='فایل', upload_to='profile_files', null=True, blank=True)
    about_me = models.TextField(verbose_name='درباره من', blank=True, null=True)
    sheba = models.CharField(verbose_name='شماره شبا', max_length=24, null=True, blank=True)
    card_number = models.CharField(verbose_name='شماره کارت', max_length=16, null=True, blank=True)
    bank_name = models.CharField(verbose_name='نام بانک', max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = verbose_name
        db_table = 'profile'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()


class TrappistRate(BaseModel):
    trappist = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='trappist_rate',
                                 verbose_name='درمانگر', validators=[validate_is_trappist])
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client_rate', verbose_name='مراجع',
                               validators=[validate_is_not_trappist])
    rate = models.PositiveIntegerField(verbose_name='امتیاز درمانگر',
                                       validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(verbose_name='نظر', blank=True, null=True)
    is_valid = models.BooleanField(verbose_name='معتبر', default=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'امتیاز درمانگر'
        verbose_name_plural = verbose_name
        db_table = 'trappist_rate'

    def __str__(self):
        return f'{self.trappist} - {self.client} - {self.rate}'




# class ChoiceUser(BaseModel):
#     user_choices = (
#         ('client', 'مراجع'),
#         ('trappist', 'درمانگر')
#     )
#     client = models.ForeignKey(Client, on_delete=models.CASCADE,
#                                verbose_name='مراحع', blank=True, null=True, related_name='choice_client')
#     trappist = models.ForeignKey(Trappist, on_delete=models.CASCADE,
#                                  verbose_name='درمانگر', blank=True, null=True, related_name='choice_trappist')
#     user_type = models.CharField(verbose_name='نوع کاربر', max_length=15, choices=user_choices)
#     user_id = models.IntegerField(verbose_name='شناسه کاربر', blank=True, null=True)
#
#     def __str__(self):
#         if self.trappist is not None:
#             user = self.trappist
#         else:
#             user = self.client
#         return self.user_choices + ' - ' + user
#
#     class Meta:
#         verbose_name = 'کاربر انتخابی'
#         verbose_name_plural = verbose_name
#         db_table = 'choice_user'


# class ClinicalHistory(BaseModel):


class MedicalDocument(BaseModel):
    client = models.ForeignKey(Profile, verbose_name='مراجع', on_delete=models.CASCADE,
                               related_name='medical_documents', validators=[validate_is_not_trappist])
    name = models.CharField(verbose_name='نام', max_length=50)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'مدارک پزشکی'
        verbose_name_plural = verbose_name
        db_table = 'medical_document'

    def __str__(self):
        return f'{self.name} - {self.client}'


class SpecializedDocuments(BaseModel):
    # trappist = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='درمانگر')
    name = models.CharField(verbose_name='نام', max_length=50)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    category = models.ForeignKey('post.UserCategory', verbose_name='دسته بندی کاربر', on_delete=models.CASCADE,
                                 related_name='documents')

    class Meta:
        verbose_name = 'مدارک تخصصی'
        verbose_name_plural = verbose_name
        db_table = 'specialized_document'

    def __str__(self):
        return f'{self.name} - {self.category}'


class DocumentField(BaseModel):
    specialized_documents = models.ForeignKey(SpecializedDocuments, verbose_name='مدارک تخصصی',
                                              on_delete=models.CASCADE, blank=True, null=True,
                                              related_name='fields')
    medical_document = models.ForeignKey(MedicalDocument, verbose_name='مدارک پزشکی', on_delete=models.CASCADE,
                                         blank=True, null=True, related_name='fields')
    name = models.CharField(verbose_name='نام', max_length=50)
    file = models.FileField(verbose_name='فایل', upload_to='document_files', blank=True, null=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)

    class Meta:
        verbose_name = 'مدرک'
        verbose_name_plural = verbose_name
        db_table = 'document_field'

    def __str__(self):
        return f'{self.document} - {self.name}'


class Notification(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='کاربر', related_name='notifications')

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = verbose_name
        db_table = 'notification'

    def __str__(self):
        return f'{self.user}'


class NotificationFields(BaseModel):
    test_choices = (
        ('bought', 'خریداری شده'),
        ('done', 'انجام شده'),
        ('get_result', 'دریافت نتیجه'),
    )
    counseling_choices = (
        ('b', 'a'),
        ('d', 'c'),
    )
    post_choices = (
        ('creation', 'ساخته شده'),
        ('published', 'منتشر شده'),
        ('deleted', 'حذف شده'),
        ('get_comment', 'دریافت کامنت'),
        ('get_like', 'دریافت لایک'),
        ('get_dislike', 'دریافت دیسلاک'),
    )
    off_code_choices = (
        ('test', 'تست'),
        ('package', 'پکیج'),
        ('counseling', 'مشاوره'),
    )
    notification = models.ForeignKey(Notification, verbose_name='اعلان', on_delete=models.CASCADE,
                                     related_name='fields')
    test = models.ForeignKey('exam.Test', on_delete=models.CASCADE, verbose_name='تست', related_name='notifications',
                             blank=True, null=True)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, verbose_name='پست', related_name='notifications',
                             blank=True, null=True)
    off_code = models.ForeignKey('payment.OffCode', on_delete=models.CASCADE, verbose_name='تخفیف خرید',
                                 related_name='notifications', blank=True, null=True)
    test_status = models.CharField(max_length=40, verbose_name='وضعیت تست', choices=test_choices, blank=True, null=True)
    counseling_status = models.CharField(max_length=40, verbose_name='وضعیت جلسه مشاوره', choices=counseling_choices,
                                         blank=True, null=True)
    post_status = models.CharField(max_length=40, verbose_name='وضعیت پست', choices=post_choices, blank=True, null=True)
    off_code_status = models.CharField(max_length=40, verbose_name='وضعیت کد تخفیف', choices=off_code_choices,
                                       blank=True, null=True)

    class Meta:
        verbose_name = 'اعلان ها'
        verbose_name_plural = verbose_name
        db_table = 'notification_fields'

    def __str__(self):
        return f'{self.notification}'
