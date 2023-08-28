from django.db import models
from django.conf import settings

from conf.model import BaseModel


# Create your models here.


class Test(BaseModel):
    category = models.ManyToManyField('post.Category', verbose_name='دسته بندی',
                                      related_name='tests')
    parent_test = models.ForeignKey('self', verbose_name='دسته بندی پدر', on_delete=models.CASCADE, blank=True,
                                    null=True, related_name='parents_test')
    name = models.CharField(verbose_name='نام', max_length=50)
    index = models.IntegerField(verbose_name='الویت', blank=True, null=True)
    time = models.IntegerField(verbose_name='زمان', blank=True, null=True)
    min_age = models.IntegerField(verbose_name='حداقل سن', blank=True, null=True)
    max_age = models.IntegerField(verbose_name='حداکثر سن', blank=True, null=True)
    explanation = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    question_count = models.IntegerField(verbose_name='تعداد سوالات', blank=True, null=True)

    class Meta:
        verbose_name = 'تست ها'
        verbose_name_plural = 'تست'
        db_table = 'test'

    def __str__(self):
        return f'{self.name} ,parent: {self.parent_test}'


class TestPayment(BaseModel):
    test = models.ForeignKey(Test, verbose_name='تست', on_delete=models.CASCADE, related_name='payment')
    original_price = models.IntegerField(verbose_name='قیمت اصلی', blank=True, null=True)
    offer_price = models.IntegerField(verbose_name='قیمت با تخفیف', blank=True, null=True)

    def get_percent(self):
        off_price = (self.original_price - self.offer_price)
        percent = float(off_price / self.original_price) * 100
        return percent

    class Meta:
        verbose_name = 'قیمت تست ها'
        verbose_name_plural = 'قیمت تست'
        db_table = 'test_payment'

    def __str__(self):
        return f'{self.test} {self.original_price}'


class UserTest(BaseModel):
    user = models.ForeignKey('account.ChoiceUser', on_delete=models.CASCADE,
                             verbose_name='کاربر', related_name='tests')
    test = models.ForeignKey(Test, verbose_name='تست', on_delete=models.CASCADE, related_name='user_test')
    score = models.IntegerField(verbose_name='امتیاز', blank=True, null=True)
    start_time = models.IntegerField(verbose_name='زمان شروع', blank=True, null=True)
    end_time = models.IntegerField(verbose_name='زمان پایان', blank=True, null=True)
    description = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    is_valid = models.BooleanField(verbose_name='معتبر', default=False)
    is_done = models.BooleanField(verbose_name='انجام شده', default=False)

    class Meta:
        verbose_name = 'تست های کاربران'
        verbose_name_plural = 'تست کاربر'
        db_table = 'user_test'

    def __str__(self):
        return f'{self.test.name} {self.user}'


class Question(BaseModel):
    type_choices = (
        ('text', 'متن'),
        ('image', 'عکس')
    )
    test = models.ForeignKey(Test, verbose_name='تست', on_delete=models.CASCADE, related_name='questions')
    answer = models.ManyToManyField('exam.Answer', verbose_name='سوال', related_name='question')
    body = models.TextField(verbose_name='محتوا', blank=True, null=True)
    file = models.FileField(verbose_name='قایل', upload_to='question_files', blank=True, null=True)
    index = models.IntegerField(verbose_name='اولویت', blank=True, null=True)
    type = models.CharField(verbose_name='نوع تست', max_length=15, choices=type_choices, blank=True, null=True)
    explanation = models.TextField(verbose_name='توضیحات', blank=True, null=True)

    class Meta:
        verbose_name = 'سوالات'
        verbose_name_plural = 'سوال'
        db_table = 'question'

    def __str__(self):
        return f'{self.test.name} {self.index}'


class Answer(BaseModel):
    answer_choices = (
        ('multiple choice', 'چند گزینه ای'),
        ('likert', 'لیکرت'),
        ('yes or no', 'بله یا خیر'),
        ('descriptive', 'تشریحی')
    )
    test = models.ForeignKey(Test, verbose_name='تست', on_delete=models.CASCADE, related_name='answers')
    body = models.TextField(verbose_name='محتوا', blank=True, null=True)
    file = models.FileField(verbose_name='فایل', upload_to='answer_files', blank=True, null=True)
    type = models.CharField(verbose_name='نوع', max_length=15, choices=answer_choices, blank=True, null=True)
    index = models.IntegerField(verbose_name='اولویت', blank=True, null=True)
    score = models.IntegerField(verbose_name='امتیاز', blank=True, null=True)

    class Meta:
        verbose_name = 'پاسخ ها'
        verbose_name_plural = 'پاسخ'
        db_table = 'answer'

    def __str__(self):
        return f'{self.question} {self.index}'


class UserAnswer(BaseModel):
    user_test = models.ForeignKey(UserTest, verbose_name='تست کاربر', on_delete=models.CASCADE,
                                  related_name='answers')
    question = models.ForeignKey(Question, verbose_name='سوال', on_delete=models.CASCADE, related_name='user_answer')
    choices = models.ForeignKey(Answer, verbose_name='جواب کاربر', on_delete=models.CASCADE, blank=True, null=True,
                                related_name='choice_answer')
    body = models.TextField(verbose_name='محتوا پاسخ', blank=True, null=True)
    score = models.IntegerField(verbose_name='امتیاز', blank=True, null=True)

    class Meta:
        verbose_name = 'جواب کاربر'
        verbose_name_plural = verbose_name
        db_table = 'user_answer'

    def __str__(self):
        return f'{self.user_test}'
